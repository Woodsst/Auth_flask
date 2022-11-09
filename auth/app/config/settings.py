from pydantic import BaseSettings, Field


class Redis(BaseSettings):
    host: str = Field("localhost")
    port: int = Field(6379)

    class Config:
        env_prefix = "REDIS_"


class JWT(BaseSettings):
    access_key: str = Field("access_key")
    refresh_key: str = Field("refresh_key")

    algorithm = Field("HS256")
    refresh_time = 1209600
    access_time = 3600

    class Config:
        env_prefix = "JWT"
        env_nested_delimiter = "_"


class Jaeger(BaseSettings):
    host: str = Field("localhost")
    port: int = Field(6831)

    class Config:
        env_prefix = "JAEGER_"


class Yandex(BaseSettings):
    client_id: str = Field("5bdb6d7a8bbc4fd9beae90ab0741f54a")
    client_secret: str = Field("99863bf05fab4deea5f5c2a7df890c02")
    baseurl: str = "https://oauth.yandex.ru/"
    oauth_authorize: str = (
        "https://oauth.yandex.ru/authorize?"
        "response_type=code"
        "&client_id=5bdb6d7a8bbc4fd9beae90ab0741f54a"
        "&redirect_uri=http://localhost:5000/api/v1/oauth"
        "&scope=login:email login:info"
    )

    class Config:
        env_prefix = "YANDEX"
        env_nested_delimiter = "_"


class Settings(BaseSettings):
    """Настройки для запуска приложения"""

    postgres: str = Field("postgresql://app:123qwe@localhost/clients_database")
    redis: Redis = Redis()
    JWT: JWT = JWT()
    jaeger: Jaeger = Jaeger()
    yandex: Yandex = Yandex()


settings = Settings()
