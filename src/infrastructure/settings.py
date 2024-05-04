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
