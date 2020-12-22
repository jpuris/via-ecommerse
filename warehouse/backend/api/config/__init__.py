from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "app"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000


class DatabaseSettings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DB_NAME: str


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
