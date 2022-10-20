from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Настройки для запуска приложения"""

    postgres: str = Field(
        "postgresql://app:123qwe@localhost/clients_database", env="POSTGRES"
    )
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: str = Field(6739, env="REDIS_PORT")

    JWT_key: str = Field("key", env="JWT_KEY")
