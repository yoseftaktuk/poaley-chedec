from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit import log_audit
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    verify_password,
)
from app.models import User
from app.schemas import LoginRequest, TokenResponse, UserResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    result = await db.execute(select(User).where(User.username == payload.username))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="שם משתמש או סיסמה שגויים")

    access_token = create_access_token(user.id, user.username, user.token_version)
    refresh_token = create_refresh_token(user.id, user.token_version)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
    )

    await log_audit(db, user_id=user.id, action="login", entity_type="user", entity_id=user.id)
    await db.commit()

    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(response: Response, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Use cookie refresh via middleware")


@router.post("/logout")
async def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("refresh_token")
    return {"message": "התנתקת בהצלחה"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
