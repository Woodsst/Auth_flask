from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Настройки для запуска приложения"""

    postgres: str = Field(
        "postgresql://app:123qwe@localhost/clients_database", env="POSTGRES"
    )
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    JWT_access_key: str = Field("access_key", env="JWT_ACCESS_KEY")
    JWT_refresh_key: str = Field("refresh_key", env="JWT_REFRESH_KEY")

    JWT_algorithm = Field("HS256", env="JWT_ACCESS_ALGORITHM")
    JWT_refresh_time = 1209600
    JWT_access_time = 3600

    debug: bool = Field(False, env="DEBUG")
    host_app: str = Field("0.0.0.0", env="HOST_APP")

    jaeger_host: str = Field("localhost")
    jaeger_port: int = Field(6831)

    yandex_client_id: str = "5bdb6d7a8bbc4fd9beae90ab0741f54a"
    yandex_client_secret: str = "99863bf05fab4deea5f5c2a7df890c02"
    yandex_baseurl: str = "https://oauth.yandex.ru/"
    yandex_oauth_authorize: str = (
        "https://oauth.yandex.ru/authorize?"
        "response_type=code"
        "&client_id=5bdb6d7a8bbc4fd9beae90ab0741f54a"
        "&redirect_uri=http://localhost:5000/api/v1/oauth"
        "&scope=login:email login:info"
    )
    get_ip: str = "http://httpbin.org/ip"


settings = Settings()
