import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Tuple, Dict, Optional, Union

import aioredis
from aiohttp import ClientSession, ContentTypeError
from aiohttp.web_exceptions import HTTPUnauthorized

from vtb_http_interaction.errors import MaxRetryError
from vtb_http_interaction.keycloak_gateway import KeycloakGateway, KeycloakConfig


class OnErrorResult(Enum):
    """
    SILENT - проигнорировать ошибку
    THROW - возбудить ошибку
    REFRESH - при ошибке выполнить действие повторно
    """
    SILENT = 1
    THROW = 2
    REFRESH = 3


class BaseService(ABC):
    """
    Abstract service
    """

    def __init__(self, max_retry: Optional[int] = 5):
        self.logger = logging.getLogger(__name__)
        self.current_step = 0
        self.max_retry = max_retry

    @abstractmethod
    async def _send(self, *args, **kwargs) -> Any:
        """
        Abstract _send
        """
        raise NotImplementedError("Not implemented _send method")

    async def send_request(self, *args, **kwargs) -> Any:
        """
        Вызов внешнего сервиса
        """

        try:
            self.logger.debug("Send request %s: %s; %s", self.current_step, args, kwargs)
            args, kwargs = await self._before_send(*args, **kwargs)
            response = await self._send(*args, **kwargs)
            self.logger.debug("Response %s: %s", self.current_step, response)

            return response
        except Exception as ex:
            self.logger.exception(ex)

            on_error_result = await self._on_error(ex, *args, **kwargs)

            if on_error_result == OnErrorResult.THROW:
                raise ex
            elif on_error_result == OnErrorResult.SILENT:
                return None
            elif on_error_result == OnErrorResult.REFRESH:
                return await self._resend_request(*args, **kwargs)
            else:
                raise NotImplementedError(f"on_error_result \"{on_error_result}\" not implemented") from ex

    async def _before_send(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        """
        Действие перед вызовом
        """
        return args, kwargs

    async def _on_error(self, ex: Exception, *args, **kwargs) -> OnErrorResult:
        """
        Действие на возникновение ошибки.
        SILENT - продолжить работу без возникновения ошибки
        THROW - выкинуть исключение дальше
        REFRESH - сделать повторный вызов сервиса
        """
        return OnErrorResult.THROW

    async def _resend_request(self, *args, **kwargs) -> Any:
        """ Повторная отправка запроса """
        self.current_step += 1

        if self.current_step > self.max_retry:
            raise MaxRetryError(f'Exceeded the maximum number of attempts {self.max_retry}')

        return await self.send_request(*args, **kwargs)


class HttpService(BaseService):
    """
    Вызов по протоколу http
    """

    async def _send(self, *args, **kwargs) -> Any:
        method = kwargs.get('method', 'get')

        url = kwargs.get('url', None)
        if url is None:
            raise ValueError("Url is none")

        cfg = kwargs.get('cfg', {})
        assert isinstance(cfg, dict)

        async with ClientSession() as session:
            async with session.request(method, url, **cfg) as response:
                status = response.status
                if status == 401:
                    raise HTTPUnauthorized()

                # ContentTypeError
                try:
                    response_data = await response.json()
                except ContentTypeError:
                    response_data = await response.text()

                return status, response_data


class RestService(HttpService):
    """
    Вызов rest сервисов
    """

    def __init__(self, url: str, item_url_postfix: Optional[str] = ''):
        super().__init__()
        if url is None:
            raise ValueError("url is none.")

        self.url = url
        self.item_url_postfix = item_url_postfix

    async def post(self, *args, **kwargs) -> Tuple[int, Any]:
        """
        Perform HTTP POST request.
        """
        kwargs['method'] = "POST"
        kwargs['url'] = self.url

        return await self.send_request(*args, **kwargs)

    async def get(self, *args, **kwargs) -> Tuple[int, Any]:
        """
        Perform HTTP GET request.
        """

        kwargs['method'] = "GET"
        kwargs['url'] = self._prepare_item_url(kwargs['item_id']) if 'item_id' in kwargs else self.url

        return await self.send_request(*args, **kwargs)

    async def put(self, *args, **kwargs) -> Tuple[int, Any]:
        """
        Perform HTTP PUT request.
        """

        kwargs['method'] = "PUT"
        kwargs['url'] = self._prepare_item_url(kwargs.get('item_id', None))

        return await self.send_request(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> Tuple[int, Any]:
        """
        Perform HTTP DELETE request.
        """

        kwargs['method'] = "DELETE"
        kwargs['url'] = self._prepare_item_url(kwargs.get('item_id', None))

        return await self.send_request(*args, **kwargs)

    def _prepare_item_url(self, item_id: str) -> str:
        if item_id is None:
            raise ValueError('Request must contain an id.')

        item_id = str(item_id)

        if item_id.startswith('/'):
            item_id = item_id[1:]

        url = self.url
        if url.endswith('/'):
            url = url[:-1]

        return f"{url}/{item_id}{self.item_url_postfix}"


class AuthorizationService(RestService):
    """
    Вызов rest сервисов под УЗ пользователя Key cloak
    """

    def __init__(self,
                 url: str,
                 keycloak_config: KeycloakConfig,
                 redis_connection_string: str,
                 item_url_postfix: Optional[str] = ''):
        super().__init__(url, item_url_postfix)

        self.refresh_token = None
        self.redis_connection_string = redis_connection_string
        self.keycloak_config = keycloak_config
        self.cache_key = f"{keycloak_config.realm_name}_{keycloak_config.client_id}"

    async def _before_send(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        """
        Действие перед вызовом:
        0. Получение токена выполнять тольк, если его нет в заголовке
        1. Получаем refresh_token и access_token из Redis
        2. Если их нет, то запрашиваем их на основе логина/пароля. Кладем их в Redis
        3. Формируем заголовок к запросу 'Authorization': "Bearer {access_token}"
        """
        if not _authorization_header_exist(**kwargs):
            redis_pool = await aioredis.create_redis_pool(self.redis_connection_string)

            try:
                access_token, self.refresh_token = await _get_token_from_cache(redis_pool, self.cache_key)

                if self.refresh_token is None or access_token is None:
                    with KeycloakGateway(self.keycloak_config) as gateway:
                        access_token, self.refresh_token = gateway.obtain_token()

                    await _set_token_into_cache(redis_pool, self.cache_key,
                                                {'access_token': access_token, 'refresh_token': self.refresh_token})
            finally:
                redis_pool.close()
                await redis_pool.wait_closed()

            if 'cfg' not in kwargs:
                kwargs['cfg'] = {}

            if 'headers' not in kwargs['cfg']:
                kwargs['cfg']['headers'] = {}

            if 'Authorization' not in kwargs['cfg']['headers']:
                kwargs['cfg']['headers']['Authorization'] = f'Bearer {access_token}'

        return args, kwargs

    async def _on_error(self, ex: Exception, *args, **kwargs) -> OnErrorResult:
        """
        Действие на возникновение ошибки KeycloakInvalidTokenError:
        1. Обновляем access_token на основе refresh_token
        2. Кладем новые access_token и refresh_token в Redis
        3. Возвращаем OnErrorResult.REFRESH для повторного вызова сервиса с новым заголовком

        На все остальные ошибки вернуть OnErrorResult.THROW
        """
        if isinstance(ex, HTTPUnauthorized) and self.refresh_token:
            with KeycloakGateway(self.keycloak_config) as gateway:
                access_token, self.refresh_token = gateway.obtain_new_token(self.refresh_token)

            redis_pool = await aioredis.create_redis_pool(self.redis_connection_string)
            try:
                await _set_token_into_cache(redis_pool, self.cache_key,
                                            {'access_token': access_token, 'refresh_token': self.refresh_token})

                if 'Authorization' in kwargs['cfg']['headers']:
                    del kwargs['cfg']['headers']['Authorization']

                return OnErrorResult.REFRESH
            finally:
                redis_pool.close()
                await redis_pool.wait_closed()

        return OnErrorResult.THROW


async def _get_token_from_cache(redis_pool: aioredis.Redis, cache_key: str) -> \
        Tuple[Union[None, str], Union[None, str]]:
    """
    Получаем refresh_token и access_token из Redis
    """
    key_exist = await redis_pool.exists(cache_key)
    if key_exist:
        result = await redis_pool.hgetall(cache_key, encoding='utf-8')
        return result.get('access_token', None), result.get('refresh_token', None)

    return None, None


async def _set_token_into_cache(redis_pool: aioredis.Redis, cache_key: str,
                                cache_value: Dict[str, str]) -> None:
    """
    Кладем refresh_token и access_token в Redis
    """
    key_exist = await redis_pool.exists(cache_key)
    if key_exist:
        await redis_pool.delete(cache_key)

    await redis_pool.hmset_dict(cache_key, **cache_value)


def _authorization_header_exist(**kwargs):
    """ Проверка наличия заголовка Authorization в запросе """
    if 'cfg' not in kwargs or 'headers' not in kwargs['cfg']:
        return False

    authorization = kwargs['cfg']['headers'].get('Authorization', None)

    return authorization is not None and str(authorization).startswith('Bearer')
