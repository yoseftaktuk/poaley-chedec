import pytest
from jose import jwt

from app.core.config import settings
from app.core.security import (
    ALGORITHM,
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_hash_and_verify_password():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed)
    assert not verify_password("wrong", hashed)


def test_verify_password_accepts_legacy_bcrypt_hash():
    legacy_hash = "$2b$12$9fFTTEaYzxFtz7GK8TwVxOMGaVczkR0HWbPD/oMf64S5YlMS43vZu"
    assert verify_password("secret123", legacy_hash)
    assert not verify_password("wrong", legacy_hash)


def test_create_and_decode_access_token():
    import uuid

    user_id = uuid.uuid4()
    token = create_access_token(user_id, "admin", 0)
    payload = decode_token(token)
    assert payload["sub"] == str(user_id)
    assert payload["username"] == "admin"
    assert payload["type"] == "access"


def test_decode_invalid_token_raises():
    import pytest
    from jose import JWTError

    with pytest.raises(JWTError):
        decode_token("invalid.token.here")


def test_expired_token_raises():
    from datetime import UTC, datetime, timedelta

    import pytest
    from jose import JWTError

    expired_payload = {
        "sub": "00000000-0000-0000-0000-000000000001",
        "username": "admin",
        "token_version": 0,
        "type": "access",
        "exp": datetime.now(UTC) - timedelta(hours=1),
    }
    token = jwt.encode(expired_payload, settings.secret_key, algorithm=ALGORITHM)
    with pytest.raises(JWTError):
        decode_token(token)
