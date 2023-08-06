from typing import Dict, Any, Optional, Tuple, NamedTuple

from keycloak import KeycloakOpenID


class KeycloakConfig(NamedTuple):
    """ Конфигурация  KeycloakOpenID """
    server_url: str
    realm_name: str
    client_id: str
    client_secret_key: Optional[str] = None
    verify: Optional[bool] = True
    custom_headers: Optional[Dict[str, Any]] = None


class UserCredentials(NamedTuple):
    """ Комбинация логин/пароль """
    username: Optional[str] = ""
    password: Optional[str] = ""


class KeycloakGateway:
    """
    Интеграционный модуль с Keycloak
    """

    def __init__(self, keycloak_config: KeycloakConfig):
        self.keycloak_config = keycloak_config

        self.keycloak_openid = None
        self.token = None
        self.keycloak_openid = None

    def __enter__(self):
        """
        Создаем Keycloak Open Id
        """
        self.keycloak_openid = KeycloakOpenID(server_url=self.keycloak_config.server_url,
                                              realm_name=self.keycloak_config.realm_name,
                                              client_id=self.keycloak_config.client_id,
                                              client_secret_key=self.keycloak_config.client_secret_key,
                                              verify=self.keycloak_config.verify,
                                              custom_headers=self.keycloak_config.custom_headers)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрываем подключение
        """
        if self.keycloak_openid is not None and self.token is not None:
            self.keycloak_openid.logout(self.refresh_token)

    def obtain_token(self, user_credentials: Optional[UserCredentials] = None,
                     grant_type: Optional[Tuple[str]] = ("client_credentials",), ) -> Tuple[str, str]:
        """
        Получение токена на основе логина/пароля
        """
        self.token = self.keycloak_openid.token(
            username=user_credentials.username if user_credentials and user_credentials.username else '',
            password=user_credentials.password if user_credentials and user_credentials.password else '',
            grant_type=grant_type)

        return self.access_token, self.refresh_token

    def obtain_new_token(self, refresh_token: Optional[str] = None,
                         grant_type: Optional[Tuple[str]] = ("client_credentials",), ) -> Tuple[str, str]:
        """
        Обновление token на основе refresh token
        """

        self.token = self.keycloak_openid.refresh_token(refresh_token or self.refresh_token, grant_type)

        return self.access_token, self.refresh_token

    def decode_token(self, token: str,
                     key: str,
                     algorithms: Optional[Tuple[str]] = ('RS256',)) -> Dict[str, Any]:
        """
        Декодирование токена, который был закодирован на основе алгоритма RS256
        """
        options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}

        token_info = self.keycloak_openid.decode_token(token, key, algorithms=algorithms, options=options)

        return token_info

    @property
    def remote_info(self) -> Dict[str, Any]:
        """
        Информация о конфигурации
        """
        well_know = self.keycloak_openid.well_know()

        return well_know

    @property
    def access_token(self) -> str:
        """
        Access token
        """
        if self.token is None:
            raise ValueError("First you need to get a token")
        return self.token['access_token']

    @property
    def refresh_token(self) -> str:
        """
        Refresh token
        """
        if self.token is None:
            raise ValueError("First you need to get a token")
        return self.token['refresh_token']

    @property
    def user_info(self) -> Dict[str, Any]:
        """
        Информация о пользователе
        """
        user_info = self.keycloak_openid.userinfo(self.access_token)
        return user_info

    @property
    def public_key(self) -> str:
        """
        Получение публичного ключа
        """
        key = f"-----BEGIN PUBLIC KEY-----\n{self.keycloak_openid.public_key()}\n-----END PUBLIC KEY-----"

        return key
