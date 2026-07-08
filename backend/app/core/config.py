"""Application settings loaded from environment variables (see .env.example)."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def normalize_database_url(url: str) -> str:
    """Ensure Render-style postgres URLs use the asyncpg SQLAlchemy driver."""
    if url.startswith("postgres://"):
        return "postgresql+asyncpg://" + url[len("postgres://") :]
    if url.startswith("postgresql://"):
        return "postgresql+asyncpg://" + url[len("postgresql://") :]
    return url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # DATABASE_URL
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/poaley_chedec"
    # TEST_DATABASE_URL
    test_database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/poaley_chedec_test"

    # SECRET_KEY
    secret_key: str = "change-me"
    # ENVIRONMENT
    environment: str = "development"
    # CORS_ORIGINS (comma-separated)
    cors_origins: str = "http://localhost:5173"
    # TIMEZONE
    timezone: str = "Asia/Jerusalem"

    # ZMANIM_LATITUDE, ZMANIM_LONGITUDE, ZMANIM_TZID
    zmanim_latitude: float = 31.669
    zmanim_longitude: float = 34.571
    zmanim_tzid: str = "Asia/Jerusalem"

    # ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expire_minutes: int = 480
    # REFRESH_TOKEN_EXPIRE_DAYS
    refresh_token_expire_days: int = 7

    # ADMIN_USERS (JSON array)
    admin_users: str = '[{"username":"admin","password":"changeme123"}]'

    # SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@poaleitzedek.org"
    # CONTACT_RECIPIENT_EMAIL
    contact_recipient_email: str = "taktuk01@gmail.com"

    # CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""

    @field_validator("database_url", "test_database_url", mode="before")
    @classmethod
    def ensure_async_postgres_driver(cls, value: object) -> object:
        if isinstance(value, str):
            return normalize_database_url(value)
        return value

    @property
    def cors_origin_list(self) -> list[str]:
        origins = [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        if not self.is_production:
            expanded: list[str] = []
            for origin in origins:
                if "://localhost" in origin:
                    expanded.append(origin.replace("://localhost", "://127.0.0.1"))
                if "://127.0.0.1" in origin:
                    expanded.append(origin.replace("://127.0.0.1", "://localhost"))
            for origin in expanded:
                if origin not in origins:
                    origins.append(origin)
        return origins

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


settings = Settings()
