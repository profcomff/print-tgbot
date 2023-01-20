from pydantic import BaseSettings, PostgresDsn, AnyUrl
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    BOT_TOKEN: str
    DB_DSN: PostgresDsn
    MARKETING_URL: str
    PRINT_URL: AnyUrl
    PDF_PATH: str = 'userdata'
    MAX_PDF_SIZE_MB: float

    class Config:
        """Pydantic BaseSettings config"""
        case_sensitive = True
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
