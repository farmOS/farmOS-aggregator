import os
import secrets
from typing import List

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator
from celery.schedules import crontab

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins.
    # e.g: '["http://localhost", "http://localhost:4200"]'

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    PROJECT_NAME: str

    SENTRY_DSN: HttpUrl = None
    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v):
        if len(v) == 0:
            return None
        return v

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v, values):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SMTP_TLS: bool = True
    SMTP_PORT: int = None
    SMTP_HOST: str = None
    SMTP_USER: str = None
    SMTP_PASSWORD: str = None
    EMAILS_FROM_EMAIL: EmailStr = None
    EMAILS_FROM_NAME: str = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v, values):
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v, values):
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    USERS_OPEN_REGISTRATION: bool = False

    TEST_FARM_NAME: str = "farmOS-test-instance"
    TEST_FARM_URL: HttpUrl = None
    TEST_FARM_USERNAME: str = None
    TEST_FARM_PASSWORD: str = None

    AGGREGATOR_OPEN_FARM_REGISTRATION: bool = False
    AGGREGATOR_INVITE_FARM_REGISTRATION: bool = False
    FARM_ACTIVE_AFTER_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


CELERY_WORKER_PING_INTERVAL = crontab(minute='0', hour='0,12')

settings = Settings()
