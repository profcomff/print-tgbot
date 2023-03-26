from pydantic import AnyUrl, BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """Application settings"""

    BOT_TOKEN: str
    DB_DSN: PostgresDsn
    MARKETING_URL: AnyUrl
    PRINT_URL: AnyUrl
    PRINT_URL_QR: AnyUrl
    MAX_PDF_SIZE_MB: float

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"
