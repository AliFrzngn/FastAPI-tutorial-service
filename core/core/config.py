from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    SQLALCHEMY_DATABASE_URL: str 
    JWT_SECRET_KEY: str 
    REDIS_URL: str 

    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "no_reply@gmail.com"
    MAIL_PORT: int = 25
    MAIL_SERVER: str = "smtp4dev"
    MAIL_FROM_NAME: str = "admin"
    MAIL_SSL_TLS: bool = False
    MAIL_STARTTLS: bool = False
    USE_CREDENTIALS: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
