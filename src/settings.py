from functools import lru_cache
from typing import List, Optional

import requests
from pydantic import ConfigDict, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings - DATA ONLY"""

    BOT_TOKEN: str
    DB_DSN: PostgresDsn
    MARKETING_URL: str
    PRINT_URL: str
    PRINT_URL_QR: str
    MAX_PDF_SIZE_MB: int
    MAX_PAGE_COUNT: int
    CONTENT_TYPES: List[str]

    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="allow")


sync_settings: Optional[Settings]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    global sync_settings
    if sync_settings is not None:
        return sync_settings
    return Settings()


async def sync_from_server():
    """Syncs the settings with server"""
    settings = get_settings()
    response = requests.get(
        "app.profcomff.com/admin/settings", # Вот тут не уверен с адресом...
        headers={"Authorization": f"Bearer {settings.BOT_TOKEN}"},
        timeout=10,
    )

    if response.status_code == 200:
        server_data = response.json()
        current_data = get_settings().model_dump()
        updated_data = {**current_data, **server_data}

        sync_settings = Settings(**updated_data)
        get_settings.cache_clear()
