# Cервис Auth

#### Cервис Auth реализовывает авторизацию пользователей и управление доспупом для этоих пользователей.
При аутентификации пользователь получает два токена
access token и refresh token. Access token который передается в заголовке Autorization и содержит
информацию об уровне доступа пользователя и его id, по нему сервис понимает, к каким эндпоинтам у пользователя есть доступ.
Refresh token необходим для обновления access токена, время действия которого ограничено.
У пользователя может быть одна из трех ролей: user, admin и subscriber. Admin может упралвять ролями
пользователей: удалять, добавлять, изменять роли. Subscriber - пользователь с премиум правами 
имеет доступ к большим страницам, чем User.

#### Сервис использующий авторизацию
https://github.com/Sarmash/FastAPI-solution

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
3. Осуществить вход в **[OpenAPI](http://localhost/apidoc/swagger/)** для просмотра всех доступных эндпоинтов

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
#### Регистрация | Логин через yandex:
```commandline
    http://localhost/api/v1/login/yandex_oauth
    
    Регистрирует пользователя если он ещё не был зарегистрирован и выдает refresh и access токены,
    либо аутентифицирует пользователя и выдает токены.
```

#### Для регистрации администратора:
```commandline
    $ flask createadmin
```
Администратор имеет доступ к управлению ролями по которым организовывается доступ к контенту кинотеатра.

### Авторы проекта
* [**Шебуняев Иван - тимлид проекта**](https://github.com/Woodsst)
* [**Останин Алексей**](https://github.com/A1exit)
