from typing import Tuple, Any, Dict, Union

import aioredis

from vtb_http_interaction.keycloak_gateway import KeycloakGateway, KeycloakConfig


class ProcessAuthorizationHeader:
    """
    Обработка заголовка Authorization
    """

    def __init__(self,
                 keycloak_config: KeycloakConfig,
                 redis_connection_string: str):
        self.refresh_token = None
        self.redis_connection_string = redis_connection_string
        self.keycloak_config = keycloak_config
        self.cache_key = f"{keycloak_config.realm_name}_{keycloak_config.client_id}"

    async def prepare_header(self, **kwargs) -> Dict[Any, Any]:
        """
        Обработка заголовка Authorization перед вызовом session.request
        Алгоритм:
        0. Получение токена выполнять только, если его нет в заголовке
        1. Получаем refresh_token и access_token из Redis
        2. Если их нет, то запрашиваем их на основе логина/пароля. Кладем их в Redis
        3. Формируем заголовок к запросу 'Authorization': "Bearer {access_token}"
        :param kwargs: параметры запроса
        :return: обработанные параметры запроса
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

        return kwargs

    async def obtain_token(self, **kwargs) -> Dict[Any, Any]:
        """
        Обновление access_token
        Алгоритм:
        1. Обновляем access_token на основе refresh_token
        2. Кладем новые access_token и refresh_token в Redis
        :param kwargs: параметры запроса
        :return: обработанные параметры запроса
        """
        if self.refresh_token is None:
            raise ValueError('refresh_token is none')

        with KeycloakGateway(self.keycloak_config) as gateway:
            access_token, self.refresh_token = gateway.obtain_new_token(self.refresh_token)

        redis_pool = await aioredis.create_redis_pool(self.redis_connection_string)
        try:
            await _set_token_into_cache(redis_pool, self.cache_key,
                                        {'access_token': access_token, 'refresh_token': self.refresh_token})

            if _authorization_header_exist(**kwargs):
                del kwargs['cfg']['headers']['Authorization']
        finally:
            redis_pool.close()
            await redis_pool.wait_closed()

        return kwargs


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
