from ..settings import default_settings

USERS = [
    {
        "login": "user1",
        "password": "pupaaaaaaa",
        "email": "lupa@gmail.com",
    },
    {
        "login": "user2",
        "password": "pupa22222",
        "email": "lupa2@gmail.com",
    },
    {
        "login": "user3",
        "password": "pupa33333",
        "email": "lupa3@gmail.com",
    },
]

LOGIN = {"login": "user1", "password": "pupaaaaaaa"}

ADMIN_LOGIN = {"login": "admin", "password": "admin111"}

CHANGE_EMAIL = {"new_email": "dfjkg@gmail.com"}

ADD_ROLE = {"role": "new_role", "description": "new description"}

USER_AGENT = {"user-agent": "python"}

CONTENT_TYPE = {"Content-Type": "application/json"}

REGISTRATION_URL = (
    f"http://{default_settings.host_app}:"
    f"{default_settings.port_app}/api/v1/registration"
)

PROFILE_URL = (
    f"http://{default_settings.host_app}:"
    f"{default_settings.port_app}/api/v1/profile/"
)

CRUD_URL = (
    f"http://{default_settings.host_app}:"
    f"{default_settings.port_app}/api/v1/crud/"
)

LOGIN_URL = (
    f"http://{default_settings.host_app}:"
    f"{default_settings.port_app}/api/v1/login"
)

LOGOUT_URL = (
    f"http://{default_settings.host_app}:"
    f"{default_settings.port_app}/api/v1/logout"
)

TOKEN_URL = (
    f"http://{default_settings.host_app}:"
    f"{default_settings.port_app}/api/v1/"
)

OUT_TIME_TOKEN = (
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjFlZj"
    "hjNDI3LTExMDAtNDczNi04Y2IxLWRlMDlmZGUzNDMzNiIsInJvbGUiOiIy"
    "IiwicmVjZWlwdF90aW1lIjoiMjAyMi0xMC0yNyAwOTo0ODoxNy4yMDg1NT"
    "IiLCJlbmRfdGltZSI6IjIwMjItMTAtMjcgMTA6NDg6MTcuMjA4NTUyIiwi"
    "YWNjZXNzIjoiYWNjZXNzIn0.7FBltHK7JzNh3MQ4lNlRtQ-T_GieVyv9PJ"
    "l2BYq3WoA"
)

ACCESS_TOKEN_LIFE_TIME = 3600
REFRESH_TOKEN_LIFE_TIME = 1210000

NEW_ROLE = "new_role"
DESCRIPTION = "description"
