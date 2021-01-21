import os
import secrets
from typing import List

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator, Json


class Settings(BaseSettings):
    API_PREFIX: str = "/api"

    API_V1_PREFIX: str = None
    @validator("API_V1_PREFIX", pre=True, always=True)
    def build_api_v1_prefix(cls, v, values):
        base = values.get("API_PREFIX")
        prefix = "/v1"
        if isinstance(v, str):
            prefix = v
        return base + prefix

    API_V2_PREFIX: str = None
    @validator("API_V2_PREFIX", pre=True, always=True)
    def build_api_v2_prefix(cls, v, values):
        base = values.get("API_PREFIX")
        prefix = "/v2"
        if isinstance(v, str):
            prefix = v
        return base + prefix

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

    AGGREGATOR_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_POOL_SIZE: int = 10
    SQLALCHEMY_MAX_OVERFLOW: int = 15
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
            return values["AGGREGATOR_NAME"]
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
    EMAIL_TESTING: bool = False

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
    AGGREGATOR_ALERT_NEW_FARMS: bool = False
    AGGREGATOR_ALERT_ALL_ERRORS: bool = False
    AGGREGATOR_ALERT_PING_FARMS_ERRORS: bool = True

    AGGREGATOR_OAUTH_CLIENT_ID: str
    AGGREGATOR_OAUTH_CLIENT_SECRET: str = None
    AGGREGATOR_OAUTH_INSECURE_TRANSPORT: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
