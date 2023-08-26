from typing import Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "booking-system"
    VERSION: str = "0.2.0"
    POSTGRES_SERVER: str = "booking-db"
    POSTGRES_USER: str = "dev"
    POSTGRES_PASSWORD: str = "dev"
    POSTGRES_DB: str = "dev"

    POSTGRES_MAIN_DB: str = "postgres"
    POSTGRES_MAIN_USER: str = "dev"
    POSTGRES_MAIN_PASSWORD: str = "dev"

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn]

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def database_uri(cls, val, values):
        if isinstance(val, str):
            return val
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()