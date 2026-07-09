"""Application settings loaded from environment variables (see .env.example)."""

import json
import ssl
import sys
import time
from urllib.parse import urlparse
from uuid import uuid4

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_DEBUG_LOG_PATH = "/Users/natankatz/poaley-chedec/.cursor/debug-1545be.log"


def _agent_debug_log(
    location: str,
    message: str,
    data: dict,
    hypothesis_id: str,
    run_id: str = "pre-fix",
) -> None:
    # #region agent log
    payload = {
        "sessionId": "1545be",
        "timestamp": int(time.time() * 1000),
        "location": location,
        "message": message,
        "data": data,
        "runId": run_id,
        "hypothesisId": hypothesis_id,
    }
    line = json.dumps(payload) + "\n"
    try:
        with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError:
        pass
    sys.stderr.write(f"[agent-debug] {line}")
    # #endregion


def normalize_database_url(url: str) -> str:
    """Ensure postgres URLs use the asyncpg SQLAlchemy driver."""
    if url.startswith("postgres://"):
        return "postgresql+asyncpg://" + url[len("postgres://") :]
    if url.startswith("postgresql://"):
        return "postgresql+asyncpg://" + url[len("postgresql://") :]
    return url


def classify_database_host(hostname: str | None) -> str:
    """Classify DB host for safe logging (no credentials)."""
    if not hostname:
        return "missing"
    if hostname in {"localhost", "127.0.0.1", "db"}:
        return "local"
    if "supabase.co" in hostname or "supabase.com" in hostname:
        return "supabase"
    if hostname.startswith("dpg-") and ".render.com" not in hostname:
        return "render_internal"
    if hostname.endswith(".render.com") or "postgres.render.com" in hostname:
        return "render_external"
    return "other"


def is_supabase_pooler(url: str) -> bool:
    """True when the URL targets Supabase's PgBouncer pooler (transaction mode)."""
    parsed = urlparse(url)
    if classify_database_host(parsed.hostname) != "supabase":
        return False
    port = parsed.port or 5432
    return port == 6543 or "pooler" in (parsed.hostname or "")


def database_connect_args(url: str) -> dict:
    """asyncpg connect_args based on database host (Supabase, Render, local, etc.)."""
    parsed = urlparse(url)
    host_kind = classify_database_host(parsed.hostname)
    port = parsed.port or 5432
    pooler = is_supabase_pooler(url)

    # #region agent log
    _agent_debug_log(
        "config.py:database_connect_args",
        "computed db connect profile",
        {
            "hostKind": host_kind,
            "port": port,
            "hostnameSuffix": (parsed.hostname or "")[-40:],
            "isPooler": pooler,
        },
        hypothesis_id="A",
    )
    # #endregion

    if host_kind in {"local", "missing"}:
        return {}

    if host_kind == "render_internal":
        return {"ssl": False}

    if host_kind == "supabase":
        connect_args: dict = {"ssl": "require"}
        if pooler:
            connect_args["statement_cache_size"] = 0
            connect_args["prepared_statement_cache_size"] = 0
            connect_args["prepared_statement_name_func"] = lambda: f"__asyncpg_{uuid4()}__"
        # #region agent log
        _agent_debug_log(
            "config.py:database_connect_args",
            "supabase connect_args keys",
            {
                "keys": sorted(connect_args.keys()),
                "hasStatementCacheZero": connect_args.get("statement_cache_size") == 0,
                "hasPreparedCacheZero": connect_args.get("prepared_statement_cache_size") == 0,
                "hasUniqueNameFunc": "prepared_statement_name_func" in connect_args,
            },
            hypothesis_id="B",
        )
        # #endregion
        return connect_args

    return {"ssl": ssl.create_default_context()}


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
