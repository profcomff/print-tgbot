from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    """Application settings"""

    BOT_TOKEN: str
    DB_DSN: PostgresDsn
    MARKETING_URL: str
    PRINT_URL: str
    PRINT_URL_QR: str
    MAX_PDF_SIZE_MB: float

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"
