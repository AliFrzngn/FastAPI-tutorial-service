from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseException):
    SQLALCHEMY_DATABASE_URL : str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()