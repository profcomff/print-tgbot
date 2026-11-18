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
    PROXY_URL: str | None = None

    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="allow")

    @property
    def db_url(self) -> str:
        url = str(self.DB_DSN)
        if self.DB_DSN.scheme == 'postgresql':
            return url.replace('postgresql://', 'postgresql+psycopg2://', 1)
        return url
