from app.core.config import Settings, normalize_database_url


def test_normalize_database_url_adds_asyncpg_for_render_style():
    assert normalize_database_url("postgresql://user:pass@host/db").startswith(
        "postgresql+asyncpg://"
    )
    assert normalize_database_url("postgres://user:pass@host/db").startswith("postgresql+asyncpg://")


def test_normalize_database_url_keeps_asyncpg():
    url = "postgresql+asyncpg://user:pass@host/db"
    assert normalize_database_url(url) == url


def test_settings_normalizes_database_url_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host:5432/db")
    monkeypatch.setenv("TEST_DATABASE_URL", "postgres://user:pass@host:5432/db")
    settings = Settings(_env_file=None)
    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert settings.test_database_url.startswith("postgresql+asyncpg://")
