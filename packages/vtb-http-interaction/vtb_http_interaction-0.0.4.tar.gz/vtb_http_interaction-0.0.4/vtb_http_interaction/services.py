import logging
import warnings
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Tuple, Dict, Optional

from aiohttp import ClientSession, ContentTypeError
from aiohttp.web_exceptions import HTTPUnauthorized

from vtb_http_interaction.errors import MaxRetryError
from vtb_http_interaction.keycloak_gateway import KeycloakConfig
from vtb_http_interaction.process_authorization_header import ProcessAuthorizationHeader


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


class PrepareHeaderMixin:
    """Обработка заголовка Authorization"""
    process_authorization_header = None

    async def prepare_header(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        """ Действие перед вызовом """
        kwargs = await self.process_authorization_header.prepare_header(**kwargs)

        return args, kwargs

    async def obtain_token(self, ex: Exception, **kwargs) -> OnErrorResult:
        """
        Действие на возникновение ошибки HTTPUnauthorized
        В случае обновления токена возвращаем OnErrorResult.REFRESH для повторного вызова сервиса с новым заголовком
        На все остальные ошибки вернуть OnErrorResult.THROW
        """
        if isinstance(ex, HTTPUnauthorized) and self.process_authorization_header.refresh_token:
            await self.process_authorization_header.obtain_token(**kwargs)
            return OnErrorResult.REFRESH

        return OnErrorResult.THROW


class AuthorizationHttpService(HttpService, PrepareHeaderMixin):
    """ Вызов http сервисов под УЗ пользователя Keycloak """

    def __init__(self,
                 keycloak_config: KeycloakConfig,
                 redis_connection_string: str):
        super().__init__()
        self.process_authorization_header = ProcessAuthorizationHeader(keycloak_config, redis_connection_string)

    async def _before_send(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        return await self.prepare_header(*args, **kwargs)

    async def _on_error(self, ex: Exception, *args, **kwargs) -> OnErrorResult:
        return await self.obtain_token(ex, **kwargs)


class AuthorizationService(RestService, PrepareHeaderMixin):
    """ Вызов rest сервисов под УЗ пользователя Keycloak """

    def __init__(self,
                 url: str,
                 keycloak_config: KeycloakConfig,
                 redis_connection_string: str,
                 item_url_postfix: Optional[str] = ''):
        # TODO: Удалить класс в версии 1.0.0
        warnings.warn(
            "class AuthorizationService is deprecated, use AuthorizationRestService instead. "
            "The class will be removed in version 1.0.0.",
            DeprecationWarning, stacklevel=2
        )
        super().__init__(url, item_url_postfix)
        self.process_authorization_header = ProcessAuthorizationHeader(keycloak_config, redis_connection_string)

    async def _before_send(self, *args, **kwargs) -> Tuple[Tuple[Any, ...], Dict[Any, Any]]:
        return await self.prepare_header(*args, **kwargs)

    async def _on_error(self, ex: Exception, *args, **kwargs) -> OnErrorResult:
        return await self.obtain_token(ex, **kwargs)


AuthorizationRestService = AuthorizationService
