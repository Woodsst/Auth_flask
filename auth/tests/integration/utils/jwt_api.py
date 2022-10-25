import jwt

from auth.tests.integration.settings import default_settings


def decode_access_token(token: str):
    return jwt.decode(
        token,
        key=default_settings.JWT_access_key,
        algorithms=default_settings.JWT_algorithm,
    )


def decode_refresh_token(token: str):
    return jwt.decode(
        token,
        key=default_settings.JWT_refresh_key,
        algorithms=default_settings.JWT_algorithm,
    )
