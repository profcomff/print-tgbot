from pydantic import ConfigDict, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    BOT_TOKEN: str
    DB_DSN: PostgresDsn
    MARKETING_URL: str
    PRINT_URL: str
    PRINT_URL_QR: str
    MAX_PDF_SIZE_MB: float

    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="allow")
