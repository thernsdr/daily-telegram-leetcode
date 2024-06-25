import pathlib

from pydantic import SecretStr
from pydantic_settings import (BaseSettings,
                               SettingsConfigDict)


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: SecretStr
    CHAT_ID: int

    TIMEZONE: str

    API_URL: str

    model_config = SettingsConfigDict(env_file=f"{pathlib.Path(__file__).parent.resolve()}/.env",
                                      env_file_encoding="utf-8",
                                      extra="ignore")


config = Settings()
