from enum import Enum
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationMode(Enum):
    DEBUG = "debug"
    PRODUCTION = "production"


class Config(BaseSettings):
    """
    Class for loading the necessary env variables
    """

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    MODE: ApplicationMode = Field(default=ApplicationMode.DEBUG)

    @property
    def is_debug(self) -> bool:
        """
        Gets true if application in debug mode else false
        """
        return self.MODE == ApplicationMode.DEBUG

    @property
    def db_url(self) -> str:
        """
        Gets DSN for asyncpg
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


app_config = Config()
