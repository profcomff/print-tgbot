from pydantic import BaseSettings, PostgresDsn, AnyUrl, DirectoryPath
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    BOT_TOKEN: str
    PDF_PATH: DirectoryPath
    MARKETING_URL: AnyUrl
    PRINT_URL: AnyUrl
    DB_DSN: PostgresDsn

    class Config:
        """Pydantic BaseSettings config"""
        case_sensitive = True
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
