from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "store"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8100
    WH_API_HOST: str = "127.0.0.1"
    WH_API_PORT: int = 8000


class DatabaseSettings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DB_NAME: str


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
