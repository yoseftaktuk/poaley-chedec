from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/poaley_chedec"
    secret_key: str = "change-me"
    environment: str = "development"
    cors_origins: str = "http://localhost:5173"
    timezone: str = "Asia/Jerusalem"

    access_token_expire_minutes: int = 480
    refresh_token_expire_days: int = 7

    admin_users: str = '[{"username":"admin","password":"changeme123"}]'

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@poaleitzedek.org"
    contact_recipient_email: str = "taktuk01@gmail.com"

    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""

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
