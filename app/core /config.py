from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str 
    DEBUG: bool 

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str

    # Application settings
    APP_NAME: str = "Lc-Hub"
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()