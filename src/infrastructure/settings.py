from typing import Optional

import dotenv
from pydantic_settings import BaseSettings

dotenv.load_dotenv('.env')


class BotSettings(BaseSettings):
    BOT_TOKEN: str


class DatabaseSettings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str


class InfrastructureSettings(BaseSettings):
    FRONTEND_HOST: Optional[str] = None
    BACKEND_API_HOST: str = "http://localhost:8000"


class SMTPSettings(BaseSettings):
    SMTP_EMAIL: str
    SMTP_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: str
