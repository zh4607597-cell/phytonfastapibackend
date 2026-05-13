import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

class Settings(BaseSettings):
    # Database URL – expects postgresql+psycopg2://user:pass@host/dbname
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost/erpdb"

    # JWT settings
    JWT_SECRET_KEY: str = "change-me-to-a-long-random-string"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # File storage
    FILE_STORAGE_PATH: str = "public/storage"
    # Cloud storage placeholders (e.g., AWS S3)
    CLOUD_BUCKET_NAME: str = ""
    CLOUD_REGION: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
