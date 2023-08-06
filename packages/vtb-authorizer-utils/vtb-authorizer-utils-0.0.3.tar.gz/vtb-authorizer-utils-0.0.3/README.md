# Authorizer

## Описание

Утилитарный пакет, содержащий в себе интеграционный модуль с сервисом Authorizer.

## Установка библиотеки

```
pip install vtb-authorizer-utils
```

с инструментами тестирования и проверки качества кода

```
pip install vtb-authorizer-utils[test]
```

## Быстрый старт

### AuthorizerGateway

Создание объекта AuthorizerGateway от имени сервисной учетной записи. Некоторые сервисы требуют вызов от имени учетной
записи портала.

```python
from dotenv import load_dotenv
from envparse import env
from vtb_authorizer_utils.gateway import AuthorizerGateway
from vtb_http_interaction.keycloak_gateway import KeycloakConfig

load_dotenv()

keycloak_config = KeycloakConfig(
    server_url=env.str('KEY_CLOAK_SERVER_URL'),
    client_id=env.str('KEY_CLOAK_CLIENT_ID'),
    realm_name=env.str('KEY_REALM_NAME'),
    client_secret_key=env.str('KEY_CLOAK_CLIENT_SECRET_KEY')
)

authorizer_base_url = env.str('AUTHORIZER_BASE_URL')
redis_url = env.str('REDIS_URL')

gateway = AuthorizerGateway(authorizer_base_url, keycloak_config, redis_url)
```

Создание объекта AuthorizerGateway от имени учетной записи портала (требуется access_token от keycloak)

```python
from dotenv import load_dotenv
from envparse import env
from vtb_authorizer_utils.gateway import AuthorizerGateway
from vtb_http_interaction.keycloak_gateway import KeycloakConfig, KeycloakGateway, UserCredentials

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

authorizer_base_url = env.str('AUTHORIZER_BASE_URL')
redis_url = env.str('REDIS_URL')

with KeycloakGateway(keycloak_config) as gateway:
    gateway.obtain_token(user_credentials, grant_type=("password",))
    access_token = gateway.access_token

gateway = AuthorizerGateway(authorizer_base_url, access_token=access_token)
```

### Работа с организациями

Получение списка организаций

```
organizations = await gateway.get_organizations()
```

Получение организации по name

```
organization = await gateway.get_organization(name)
```

Получение проектов организации

```
projects = await user_gateway.get_organization_projects(name)
```

Получение потомков организации
```
children = await user_gateway.get_organization_children(name)
```

### Работа с папками

Получение папки
```
folder = await user_gateway.get_folder(name)
```

### Работа с проектами

Получение проекта по name
```
project = await user_gateway.get_project(name)
```

### Работа с пользователями

Получение списка пользователей
```
users = await gateway.get_users(page=1, per_page=10, firstname="иванов", lastname="иванов")
```

Получение пользователя по его идентификатору
```
user = await gateway.get_user(users[0].remote_id)
```