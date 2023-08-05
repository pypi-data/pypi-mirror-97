# Межсервисное взаимодействие на основе протокола HTTP

## Описание

Утилитарный пакет, содержащий в себе интеграционный модуль с Keycloak и инструменты для организации межсервисного
взаимодействия на основе протокола HTTP.

## Предусловие
Сервис, который выступает источником данных должен быть зарегистрирован в Kong.  
Сервис, который выступает в роли инициатора запроса должен иметь системуную УЗ, которая регистрируется в Keycloak.  
[Подробности](http://wiki.corp.dev.vtb/pages/viewpage.action?pageId=204909264)

## Установка библиотеки

```
pip install vtb_http_interaction
```

с инструментами тестирования и проверки качества кода

```
pip install vtb_http_interaction[test]
```

## Тестирование

Запуск процесса тестирования
```
pytest
```
Внимание! Тесты test_access_token_lifespan и test_access_token_lifespan_with_portal_token выполняют проверку процесса 
обновления токена после его устаревания. Время выполнения > 2 мин. Для исключения "долгих" тестов используй команду

```
pytest -m "not slow"
```

## Быстрый старт

### Интеграционный модуль с Keycloak

Получение токена сервисной УЗ

```python
from dotenv import load_dotenv
from envparse import env

from vtb_http_interaction.keycloak_gateway import KeycloakGateway, KeycloakConfig

load_dotenv()

keycloak_config = KeycloakConfig(
    server_url=env.str('KEY_CLOAK_SERVER_URL'),
    client_id=env.str('KEY_CLOAK_CLIENT_ID'),
    realm_name=env.str('KEY_REALM_NAME'),
    client_secret_key=env.str('KEY_CLOAK_CLIENT_SECRET_KEY')
)

with KeycloakGateway(keycloak_config) as gateway:
    token = gateway.obtain_token()
```

Получение токена пользователя из кейклок

```python
from dotenv import load_dotenv
from envparse import env

from vtb_http_interaction.keycloak_gateway import KeycloakGateway, KeycloakConfig, UserCredentials

load_dotenv()

keycloak_config = KeycloakConfig(
    server_url=env.str('KEY_CLOAK_SERVER_URL'),
    client_id=env.str('KEY_CLOAK_CLIENT_ID'),
    realm_name=env.str('KEY_REALM_NAME'),
    client_secret_key=env.str('KEY_CLOAK_CLIENT_SECRET_KEY')
)

user_credentials = UserCredentials(
    username=env.str('KEY_CLOAK_TEST_USER_NAME'),
    password=env.str('KEY_CLOAK_TEST_USER_PASSWORD')
)

with KeycloakGateway(keycloak_config) as gateway:
    token = gateway.obtain_token(user_credentials,
                                 grant_type=("password",))
```

### Пример реализации межсервисного взаимодействия через Kong

```python
from dotenv import load_dotenv
from envparse import env

from vtb_http_interaction.keycloak_gateway import KeycloakConfig

from vtb_http_interaction.services import AuthorizationService

load_dotenv()

authorizer_ser_list_url = env.str('AUTHORIZER_USER_LIST_URL')
redis_url = env.str('REDIS_URL')

keycloak_config = KeycloakConfig(
    server_url=env.str('KEY_CLOAK_SERVER_URL'),
    client_id=env.str('KEY_CLOAK_CLIENT_ID'),
    realm_name=env.str('KEY_REALM_NAME'),
    client_secret_key=env.str('KEY_CLOAK_CLIENT_SECRET_KEY')
)

service = AuthorizationService(authorizer_ser_list_url,
                               keycloak_config,
                               redis_url)
params = {
    "page": 1,
    "per_page": 20
}

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

status, response = await service.get(cfg={'params': params, 'headers': headers})

```

### Инструменты для организации межсервисного взаимодействия на основе протокола HTTP

Вызов удаленного HTTP метода

```python
from vtb_http_interaction.services import HttpService

service = HttpService()

status, response = await service.send_request(
    method="GET",
    url="http://example.com/api/v1/comments?boardId=6b681e1558384da3a5d4b22a33417181")
```

Вызов удаленного REST API метода для списка комментариев с использованием фильра по boardId

```python
from vtb_http_interaction.services import RestService

service = RestService("http://example.com/api/v1/comments")

status, response = await service.get(cfg={'params': {"boardId": "6b681e1558384da3a5d4b22a33417181"}})
```

Вызов удаленного REST API метода для получения комментария с ID=1

```python
from vtb_http_interaction.services import RestService

service = RestService("http://example.com/api/v1/comments")

status, response = await service.get(item_id=1)
```

Вызов удаленного REST API метода для создания комментария

```python
from vtb_http_interaction.services import RestService

service = RestService("http://example.com/api/v1/comments")

data = {
    "content": "Привет медвед!",
    "boardId": "6b681e1558384da3a5d4b22a33417181",
    "userName": "User 1"
}

status, response = await service.post(cfg={'json': data})
```

Вызов удаленного REST API метода для обновления комментария с ID=1

```python
from vtb_http_interaction.services import RestService

service = RestService("http://example.com/api/v1/comments")

update_data = {
    "content": "Привет медвед new!",
}

status, response = await service.put(item_id=1, cfg={'json': update_data})
```

Вызов удаленного REST API метода для удаления комментария с ID=1

```python
from vtb_http_interaction.services import RestService

service = RestService("http://example.com/api/v1/comments")

status, response = await service.delete(item_id=1)
```