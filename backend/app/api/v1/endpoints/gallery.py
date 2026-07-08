import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

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
from app.services.dependencies import get_gallery_service
from app.services.gallery_service import GalleryService

router = APIRouter()
optional_bearer = HTTPBearer(auto_error=False)


@router.get("/albums", response_model=list[GalleryAlbumResponse])
async def list_albums(
    all: bool = Query(default=False),
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_bearer),
    service: GalleryService = Depends(get_gallery_service),
) -> list[GalleryAlbum]:
    if all:
        if credentials is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="לא מורשה")
        await get_current_user(credentials, db)
    return await service.list_albums(include_unpublished=all)


@router.get("/albums/{album_id}/images", response_model=list[GalleryImageResponse])
async def list_album_images(
    album_id: uuid.UUID,
    service: GalleryService = Depends(get_gallery_service),
) -> list[GalleryImage]:
    return await service.list_album_images(album_id)


@router.post("/albums", response_model=GalleryAlbumResponse, status_code=status.HTTP_201_CREATED)
async def create_album(
    payload: GalleryAlbumCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: GalleryService = Depends(get_gallery_service),
) -> GalleryAlbum:
    return await service.create_album(current_user.id, payload)


@router.put("/albums/{album_id}", response_model=GalleryAlbumResponse)
async def update_album(
    album_id: uuid.UUID,
    payload: GalleryAlbumUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: GalleryService = Depends(get_gallery_service),
) -> GalleryAlbum:
    return await service.update_album(current_user.id, album_id, payload)


@router.delete("/albums/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_album(
    album_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: GalleryService = Depends(get_gallery_service),
) -> None:
    await service.delete_album(current_user.id, album_id)


@router.post("/images", response_model=GalleryImageResponse, status_code=status.HTTP_201_CREATED)
async def create_image(
    payload: GalleryImageCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: GalleryService = Depends(get_gallery_service),
) -> GalleryImage:
    return await service.create_image(current_user.id, payload)


@router.post("/images/upload", response_model=GalleryImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_gallery_image(
    album_id: uuid.UUID,
    title: str = "",
    file: UploadFile = File(...),
    current_user: Annotated[User, Depends(get_current_user)] = None,
    service: GalleryService = Depends(get_gallery_service),
) -> GalleryImage:
    content = await file.read()
    return await service.upload_image(
        current_user.id,
        album_id,
        title,
        content,
        file.content_type,
    )


@router.put("/images/{image_id}", response_model=GalleryImageResponse)
async def update_image(
    image_id: uuid.UUID,
    payload: GalleryImageUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: GalleryService = Depends(get_gallery_service),
) -> GalleryImage:
    return await service.update_image(current_user.id, image_id, payload)


@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gallery_image(
    image_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: GalleryService = Depends(get_gallery_service),
) -> None:
    await service.delete_image(current_user.id, image_id)
