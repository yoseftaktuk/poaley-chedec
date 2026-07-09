from app.core.config import Settings, classify_database_host, database_connect_args, is_supabase_pooler, normalize_database_url
import ssl

SUPABASE_DIRECT_URL = (
    "postgresql+asyncpg://postgres:pass@db.eyagbvsdxbfpvrgdkbbs.supabase.co:5432/postgres"
)


def test_normalize_database_url_adds_asyncpg_for_render_style():
    assert normalize_database_url("postgresql://user:pass@host/db").startswith(
        "postgresql+asyncpg://"
    )
    assert normalize_database_url("postgres://user:pass@host/db").startswith("postgresql+asyncpg://")


def test_normalize_database_url_keeps_asyncpg():
    url = "postgresql+asyncpg://user:pass@host/db"
    assert normalize_database_url(url) == url


def test_classify_database_host():
    assert classify_database_host("localhost") == "local"
    assert classify_database_host("dpg-abc123-a") == "render_internal"
    assert classify_database_host("dpg-abc123-a.oregon-postgres.render.com") == "render_external"
    assert classify_database_host("db.abcdefgh.supabase.co") == "supabase"
    assert classify_database_host("db.eyagbvsdxbfpvrgdkbbs.supabase.co") == "supabase"
    assert classify_database_host("aws-0-eu-central-1.pooler.supabase.com") == "supabase"


def test_database_connect_args_local_empty():
    assert database_connect_args("postgresql+asyncpg://user:pass@localhost/db") == {}


def test_database_connect_args_render_internal_disables_ssl():
    url = "postgresql+asyncpg://user:pass@dpg-abc123-a:5432/db"
    assert database_connect_args(url) == {"ssl": False}


def test_database_connect_args_supabase_uses_ssl_require():
    url = "postgresql+asyncpg://user:pass@db.abcdefgh.supabase.co:5432/postgres"
    args = database_connect_args(url)
    assert args["ssl"] == "require"
    assert "statement_cache_size" not in args


def test_database_connect_args_supabase_direct_host_uses_ssl_require():
    args = database_connect_args(SUPABASE_DIRECT_URL)
    assert args["ssl"] == "require"
    assert "statement_cache_size" not in args


def test_database_connect_args_supabase_pooler_disables_statement_cache():
    url = "postgresql+asyncpg://user:pass@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
    args = database_connect_args(url)
    assert args["ssl"] == "require"
    assert args["statement_cache_size"] == 0
    assert args["prepared_statement_cache_size"] == 0
    assert "prepared_statement_name_func" in args
    name_a = args["prepared_statement_name_func"]()
    name_b = args["prepared_statement_name_func"]()
    assert name_a != name_b
    assert name_a.startswith("__asyncpg_")


def test_is_supabase_pooler_detects_pooler_host_and_port():
    pooler_url = "postgresql+asyncpg://user:pass@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
    direct_url = "postgresql+asyncpg://user:pass@db.abcdefgh.supabase.co:5432/postgres"
    assert is_supabase_pooler(pooler_url) is True
    assert is_supabase_pooler(direct_url) is False


def test_database_connect_args_render_external_requires_ssl():
    url = "postgresql+asyncpg://user:pass@dpg-abc123-a.oregon-postgres.render.com:5432/db"
    args = database_connect_args(url)
    assert isinstance(args["ssl"], ssl.SSLContext)


def test_settings_normalizes_database_url_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host:5432/db")
    monkeypatch.setenv("TEST_DATABASE_URL", "postgres://user:pass@host:5432/db")
    settings = Settings(_env_file=None)
    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert settings.test_database_url.startswith("postgresql+asyncpg://")
