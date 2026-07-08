import uuid

from pydantic import BaseModel

from app.schemas.base import ORMModel


class GalleryAlbumBase(BaseModel):
    title: str
    description: str = ""
    cover_image_url: str | None = None
    sort_order: int = 0
    is_published: bool = True


class GalleryAlbumCreate(GalleryAlbumBase):
    cover_public_id: str | None = None


class GalleryAlbumUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    cover_image_url: str | None = None
    cover_public_id: str | None = None
    sort_order: int | None = None
    is_published: bool | None = None


class GalleryAlbumResponse(GalleryAlbumBase, ORMModel):
    id: uuid.UUID


class GalleryImageBase(BaseModel):
    album_id: uuid.UUID
    title: str = ""
    cloudinary_public_id: str
    image_url: str
    sort_order: int = 0


class GalleryImageCreate(GalleryImageBase):
    pass


class GalleryImageUpdate(BaseModel):
    title: str | None = None
    sort_order: int | None = None


class GalleryImageResponse(GalleryImageBase, ORMModel):
    id: uuid.UUID
