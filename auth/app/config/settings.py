from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Настройки для запуска приложения"""

    postgres: str = Field(
        "postgresql://app:123qwe@localhost/clients_database", env="POSTGRES"
    )
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6739, env="REDIS_PORT")

    JWT_key: str = Field("key", env="JWT_KEY")

    debug: bool = Field(False, env="DEBUG")
    host_app: str = Field('0.0.0.0', env="HOST_APP")


default_settings = Settings()
