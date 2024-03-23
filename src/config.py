from enum import Enum
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationMode(Enum):
    DEBUG = "debug"
    PRODUCTION = "production"
    TEST = "test"


class Config(BaseSettings):
    """
    Class for loading the necessary env variables
    """

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    REDIS_URL: str

    TEST_DB_HOST: str = Field(default="")
    TEST_DB_PORT: str = Field(default="")
    TEST_DB_USER: str = Field(default="")
    TEST_DB_PASSWORD: str = Field(default="")
    TEST_DB_NAME: str = Field(default="")
    TEST_CACHE_HOST: str = Field(default="")
    TEST_CACHE_PORT: str = Field(default="")

    MODE: ApplicationMode = Field(default=ApplicationMode.DEBUG)

    @property
    def is_debug(self) -> bool:
        """
        Gets true if application in debug mode else false
        """
        return self.MODE == ApplicationMode.DEBUG

    @staticmethod
    def __generate_asyncpg_db_url(user: str, password: str, host, port: str, database_name: str) -> str:
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database_name}"

    @property
    def db_url(self) -> str:
        """
        Gets DSN for real database
        """
        return self.__generate_asyncpg_db_url(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT, self.DB_NAME)

    @property
    def test_db_url(self) -> str:
        """
        Gets DSN for testing database
        """
        return self.__generate_asyncpg_db_url(
            self.TEST_DB_USER, self.TEST_DB_PASSWORD, self.TEST_DB_HOST, self.TEST_DB_PORT, self.TEST_DB_NAME
        )

    model_config = SettingsConfigDict(env_file=".env")


app_config = Config()
