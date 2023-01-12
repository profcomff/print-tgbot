from pydantic import BaseSettings, PostgresDsn, SecretStr
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    BOT_TOKEN: SecretStr
    DB_DSN: PostgresDsn
    PDF_PATH = 'userdata'
    MARKETING_URL = 'https://marketing.api.test.profcomff.com/'
    PRINT_URL = 'https://printer.api.test.profcomff.com'

    class Config:
        """Pydantic BaseSettings config"""
        case_sensitive = True
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
