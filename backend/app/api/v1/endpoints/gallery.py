import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit import log_audit
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import GalleryAlbum, GalleryImage, User
from app.schemas import (
    GalleryAlbumCreate,
    GalleryAlbumResponse,
    GalleryAlbumUpdate,
    GalleryImageCreate,
    GalleryImageResponse,
    GalleryImageUpdate,
)
from app.services.cloudinary_service import CloudinaryNotConfiguredError, upload_image
from app.services.image_cleanup import safe_delete_image
from app.services.utils import get_by_id

router = APIRouter()
optional_bearer = HTTPBearer(auto_error=False)


@router.get("/albums", response_model=list[GalleryAlbumResponse])
async def list_albums(
    all: bool = Query(default=False),
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_bearer),
) -> list[GalleryAlbum]:
    query = select(GalleryAlbum).order_by(GalleryAlbum.sort_order)
    if not all:
        query = query.where(GalleryAlbum.is_published.is_(True))
    elif credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="לא מורשה")
    else:
        await get_current_user(credentials, db)

    result = await db.execute(query)
    return list(result.scalars().all())


@router.get("/albums/{album_id}/images", response_model=list[GalleryImageResponse])
async def list_album_images(album_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> list[GalleryImage]:
    result = await db.execute(
        select(GalleryImage).where(GalleryImage.album_id == album_id).order_by(GalleryImage.sort_order)
    )
    return list(result.scalars().all())


@router.post("/albums", response_model=GalleryAlbumResponse, status_code=status.HTTP_201_CREATED)
async def create_album(
    payload: GalleryAlbumCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> GalleryAlbum:
    item = GalleryAlbum(**payload.model_dump())
    db.add(item)
    await log_audit(db, user_id=current_user.id, action="create", entity_type="gallery_album")
    await db.commit()
    await db.refresh(item)
    return item


@router.put("/albums/{album_id}", response_model=GalleryAlbumResponse)
async def update_album(
    album_id: uuid.UUID,
    payload: GalleryAlbumUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> GalleryAlbum:
    item = await get_by_id(db, GalleryAlbum, album_id)
    if not item:
        raise HTTPException(status_code=404, detail="לא נמצא")

    updates = payload.model_dump(exclude_unset=True)
    if updates.get("cover_image_url") and updates.get("cover_public_id") is None:
        updates.pop("cover_public_id", None)

    old_public_id = item.cover_public_id
    new_public_id = updates.get("cover_public_id", item.cover_public_id)
    new_cover_url = updates.get("cover_image_url", item.cover_image_url)

    if "cover_image_url" in updates and not new_cover_url:
        updates["cover_public_id"] = None

    for key, value in updates.items():
        setattr(item, key, value)

    if old_public_id and old_public_id != new_public_id:
        safe_delete_image(old_public_id)
    if "cover_image_url" in updates and not new_cover_url and old_public_id:
        safe_delete_image(old_public_id)

    await log_audit(db, user_id=current_user.id, action="update", entity_type="gallery_album", entity_id=item.id)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/albums/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_album(
    album_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> None:
    item = await get_by_id(db, GalleryAlbum, album_id)
    if not item:
        raise HTTPException(status_code=404, detail="לא נמצא")
    safe_delete_image(item.cover_public_id)
    images = await db.execute(select(GalleryImage).where(GalleryImage.album_id == album_id))
    for image in images.scalars().all():
        safe_delete_image(image.cloudinary_public_id)
        await db.delete(image)
    await log_audit(db, user_id=current_user.id, action="delete", entity_type="gallery_album", entity_id=item.id)
    await db.delete(item)
    await db.commit()


@router.post("/images", response_model=GalleryImageResponse, status_code=status.HTTP_201_CREATED)
async def create_image(
    payload: GalleryImageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> GalleryImage:
    item = GalleryImage(**payload.model_dump())
    db.add(item)
    await log_audit(db, user_id=current_user.id, action="create", entity_type="gallery_image")
    await db.commit()
    await db.refresh(item)
    return item


@router.post("/images/upload", response_model=GalleryImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_gallery_image(
    album_id: uuid.UUID,
    title: str = "",
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> GalleryImage:
    album = await get_by_id(db, GalleryAlbum, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="אלבום לא נמצא")
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="יש להעלות קובץ תמונה בלבד")

    content = await file.read()
    try:
        uploaded = upload_image(content, folder="poaley-chedec/gallery")
    except CloudinaryNotConfiguredError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="שגיאה בהעלאת התמונה") from exc

    item = GalleryImage(
        album_id=album_id,
        title=title,
        cloudinary_public_id=uploaded["public_id"],
        image_url=uploaded["url"],
    )
    db.add(item)
    await log_audit(db, user_id=current_user.id, action="upload", entity_type="gallery_image")
    await db.commit()
    await db.refresh(item)
    return item


@router.put("/images/{image_id}", response_model=GalleryImageResponse)
async def update_image(
    image_id: uuid.UUID,
    payload: GalleryImageUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> GalleryImage:
    item = await get_by_id(db, GalleryImage, image_id)
    if not item:
        raise HTTPException(status_code=404, detail="לא נמצא")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    await log_audit(db, user_id=current_user.id, action="update", entity_type="gallery_image", entity_id=item.id)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gallery_image(
    image_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> None:
    item = await get_by_id(db, GalleryImage, image_id)
    if not item:
        raise HTTPException(status_code=404, detail="לא נמצא")
    safe_delete_image(item.cloudinary_public_id)
    await log_audit(db, user_id=current_user.id, action="delete", entity_type="gallery_image", entity_id=item.id)
    await db.delete(item)
    await db.commit()
