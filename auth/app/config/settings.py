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


default_settings = Settings()
