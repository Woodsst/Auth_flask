# Cервис Auth

#### Cервис Auth реализовывает авторизацию пользователей и управление доспупом для этоих пользователей.
В сервисе предусмотрена регистрация пользователей, вход в аккаунт пользователя,
который осуществляется по JWT токену. При аутентификации пользователь получает два токена
access token и refresh token. Access token который передается в заголовке Autorization и содержит
информацию о пользователе, по нему сервис понимает, к каким эндпоинтам у пользователя есть доступ.
Refresh token необходим для обновления access токена, время действия которого ограничено.
У пользователя может быть одна из трех ролей: user, admin и subscriber. Admin может упралвять ролями
пользователей: удалять, добавлять, изменять роли. Subscriber - пользователь с премиум правами 
имеет доступ к большим страницам, чем User.

#### Использованные технологии:
1. Python
2. Flask
3. Flask-SQLAlchemy
4. SQLAlchemy
5. Postgres
6. UWSGI
7. Redis
8. Pydantic
9. PyJWT
10. Pytest
11. Gevent

#### Чтобы развернуть проект локально необходимо:
1. Склонировать репозитрий **[Auth_sprint_1](https://github.com/Woodsst/Auth_sprint_1)**:
   ```commandline
   git clone git@github.com:Woodsst/Auth_sprint_1.git
   ```
2. В репозитарии **[Auth_sprint_1](https://github.com/Woodsst/Auth_sprint_1)** запустить сборку контейнеров:
   ```commandline
    docker compose up --build -d
   ```
3. Осуществить вход в **[flasagger](http://localhost/apidocs/)** для просмотра всех доступных эндпоинтов

#### Проект покрыт тестами, для их запуска необходимо перейти в auth/app/tests/integration и выполнить:
```commandline
    docker compose up --build -d
   ```
Будут запущены те же контейнеры + контейнер tests, в котором можно посмотреть результат
выполнения тестов

#### Основные эндпоинты:
```commandline
    http://localhost/api/v1/registration
    
    Регистрирует нового пользователя. Принимает POST запрос с телом запроса

    {
        "login": "login",
        "password": "pass",
        "email": "email@email.com"
    }
   ```
```commandline
    http://localhost/api/v1/login
    
    Выдает два токена access и refresh. Принимает POST запрос с телом запроса
    
    {
        "login": "login",
        "password": "pass",
    }
   ```

### Авторы проекта
* [**Шебуняев Иван - тимлид проекта**](https://github.com/Woodsst)
* [**Останин Алексей**](https://github.com/A1exit)