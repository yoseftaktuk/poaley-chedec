import uuid
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit import log_audit
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import BannerMessage, User
from app.schemas import BannerMessageCreate, BannerMessageResponse, BannerMessageUpdate
from app.services.days_utils import is_active_on_weekday
from app.services.utils import get_by_id

router = APIRouter()


def _filter_active_banners(banners: list[BannerMessage], now: datetime) -> list[BannerMessage]:
    result = []
    for banner in banners:
        if banner.starts_at and banner.starts_at > now:
            continue
        if banner.ends_at and banner.ends_at < now:
            continue
        if not is_active_on_weekday(banner.days_of_week or []):
            continue
        result.append(banner)
    return result


@router.get("/active", response_model=list[BannerMessageResponse])
async def list_active_banners(db: AsyncSession = Depends(get_db)) -> list[BannerMessage]:
    now = datetime.now(UTC)
    result = await db.execute(
        select(BannerMessage).where(BannerMessage.is_active.is_(True)).order_by(BannerMessage.priority.desc())
    )
    banners = _filter_active_banners(list(result.scalars().all()), now)
    return banners


@router.get("", response_model=list[BannerMessageResponse])
async def list_banners(
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> list[BannerMessage]:
    result = await db.execute(select(BannerMessage).order_by(BannerMessage.priority.desc()))
    return list(result.scalars().all())


@router.post("", response_model=BannerMessageResponse, status_code=status.HTTP_201_CREATED)
async def create_banner(
    payload: BannerMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> BannerMessage:
    item = BannerMessage(**payload.model_dump())
    db.add(item)
    await log_audit(db, user_id=current_user.id, action="create", entity_type="banner_message")
    await db.commit()
    await db.refresh(item)
    return item


@router.put("/{item_id}", response_model=BannerMessageResponse)
async def update_banner(
    item_id: uuid.UUID,
    payload: BannerMessageUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> BannerMessage:
    item = await get_by_id(db, BannerMessage, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="לא נמצא")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    await log_audit(db, user_id=current_user.id, action="update", entity_type="banner_message", entity_id=item.id)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_banner(
    item_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> None:
    item = await get_by_id(db, BannerMessage, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="לא נמצא")
    await log_audit(db, user_id=current_user.id, action="delete", entity_type="banner_message", entity_id=item.id)
    await db.delete(item)
    await db.commit()
