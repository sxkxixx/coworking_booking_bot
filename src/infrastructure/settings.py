from typing import Optional, Literal

import dotenv
from pydantic_settings import BaseSettings

dotenv.load_dotenv('.env')


class BotSettings(BaseSettings):
    BOT_TOKEN: str
    LOG_LEVEL: Literal[
        "CRITICAL",
        "FATAL",
        "ERROR",
        "WARN",
        "WARNING",
        "INFO",
        "DEBUG",
        "NOTSET",
    ] = "INFO"


class DatabaseSettings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str


class InfrastructureSettings(BaseSettings):
    FRONTEND_HOST: Optional[str] = "http://158.160.122.132:80"
    BACKEND_API_HOST: str = "http://158.160.122.132:8000"
    TECHNICAL_SUPPORT_EMAIL: str = "Alexander.Kornilov@urfu.me"


class SMTPSettings(BaseSettings):
    SMTP_EMAIL: str
    SMTP_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: str
