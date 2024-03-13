# Сервис авторизации проекта "PastaBean"

## Функицональные требования

__Для анонимного пользователя доступно:__
- регистрация аккаунта (email, login, password) - учесть уникальность email
- вход в аккаунт через email и password
- сброс пароля

__Для авторизированно пользователя доступно:__
- изменение пароля
- изменение логина
- просмотр активных сессий (время входа, User Agent)
- выход из системы

## Нефункциональные требования
- безопасность
- скорость ответа


## Детали реализации

### Инфраструктура
Для сервиса потребуются два хранилища:
- __PostgreSQL__ - для хранения информации о пользователях и всех сессиях
- __Redis__ - для хранения активных сессий и кодов для двухфакторной аутентификации

### Модель данных

```mermaid
erDiagram
    users {
        serial id
        varchar name
        varchar email
        timestamp created_at
    }
    users ||--|| secure_user_infos : has
    secure_user_infos{
        serial id
        varchar hashed_password
        varchar salt
        timestamp updated_at
    }
    users ||--|| sign_ins : has
    sign_ins{
        serial id
        varchar user_agent
        varchar auth_token
        timestamp created_at
        bool is_logout
        timestamp logout_at
    }
```