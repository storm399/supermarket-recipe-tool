from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "Supermarkt Recepten Tool"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str = "sqlite:///./app.db"

    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_PROVIDER: str = "openai"

    OPENFOODFACTS_USER_AGENT: str = "SupermarktReceptenTool/0.1 (contact@example.com)"
    OPENFOODFACTS_BASE_URL: str = "https://world.openfoodfacts.org"

    SCRAPER_INTERVAL_HOURS: int = 24
    SCRAPER_USER_AGENT: str = "SupermarktReceptenTool/0.1 (+https://example.com)"
    SCRAPER_TIMEOUT: int = 20
    USE_MOCK_SCRAPERS: bool = True

    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
