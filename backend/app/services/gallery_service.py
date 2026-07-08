import uuid

from fastapi import HTTPException, status
from sqlalchemy import select

from app.models import GalleryAlbum, GalleryImage
from app.schemas import GalleryAlbumCreate, GalleryAlbumUpdate, GalleryImageCreate, GalleryImageUpdate
from app.services.base import BaseService
from app.services.cloudinary_service import CloudinaryNotConfiguredError, upload_image
from app.services.image_assets import cleanup_replaced_image, prepare_image_field_updates
from app.services.image_cleanup import safe_delete_image
from app.services.utils import get_by_id


class GalleryService(BaseService):
    async def list_albums(self, *, include_unpublished: bool) -> list[GalleryAlbum]:
        query = select(GalleryAlbum).order_by(GalleryAlbum.sort_order)
        if not include_unpublished:
            query = query.where(GalleryAlbum.is_published.is_(True))
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def list_album_images(self, album_id: uuid.UUID) -> list[GalleryImage]:
        result = await self.db.execute(
            select(GalleryImage).where(GalleryImage.album_id == album_id).order_by(GalleryImage.sort_order)
        )
        return list(result.scalars().all())

    async def create_album(self, user_id: uuid.UUID, payload: GalleryAlbumCreate) -> GalleryAlbum:
        item = GalleryAlbum(**payload.model_dump())
        return await self.create_audited(item, user_id=user_id, entity_type="gallery_album")

    async def update_album(
        self,
        user_id: uuid.UUID,
        album_id: uuid.UUID,
        payload: GalleryAlbumUpdate,
    ) -> GalleryAlbum:
        item = await self.get_or_404(GalleryAlbum, album_id)
        updates = payload.model_dump(exclude_unset=True)
        updates, old_public_id, new_public_id, new_cover_url = prepare_image_field_updates(
            item,
            updates,
            url_field="cover_image_url",
            public_id_field="cover_public_id",
        )
        for key, value in updates.items():
            setattr(item, key, value)
        cleanup_replaced_image(
            old_public_id,
            new_public_id,
            updates,
            url_field="cover_image_url",
            new_url=new_cover_url,
        )
        return await self.commit_audited_update(item, user_id=user_id, entity_type="gallery_album")

    async def delete_album(self, user_id: uuid.UUID, album_id: uuid.UUID) -> None:
        item = await self.get_or_404(GalleryAlbum, album_id)
        safe_delete_image(item.cover_public_id)
        images = await self.db.execute(select(GalleryImage).where(GalleryImage.album_id == album_id))
        for image in images.scalars().all():
            safe_delete_image(image.cloudinary_public_id)
            await self.db.delete(image)
        await self.delete_audited(item, user_id=user_id, entity_type="gallery_album")

    async def create_image(self, user_id: uuid.UUID, payload: GalleryImageCreate) -> GalleryImage:
        item = GalleryImage(**payload.model_dump())
        return await self.create_audited(item, user_id=user_id, entity_type="gallery_image")

    async def upload_image(
        self,
        user_id: uuid.UUID,
        album_id: uuid.UUID,
        title: str,
        content: bytes,
        content_type: str | None,
    ) -> GalleryImage:
        album = await get_by_id(self.db, GalleryAlbum, album_id)
        if not album:
            raise HTTPException(status_code=404, detail="אלבום לא נמצא")
        if not content_type or not content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="יש להעלות קובץ תמונה בלבד")

        try:
            uploaded = upload_image(content, folder="poaley-chedec/gallery")
        except CloudinaryNotConfiguredError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="שגיאה בהעלאת התמונה",
            ) from exc

        item = GalleryImage(
            album_id=album_id,
            title=title,
            cloudinary_public_id=uploaded["public_id"],
            image_url=uploaded["url"],
        )
        return await self.create_audited(item, user_id=user_id, entity_type="gallery_image", action="upload")

    async def update_image(
        self,
        user_id: uuid.UUID,
        image_id: uuid.UUID,
        payload: GalleryImageUpdate,
    ) -> GalleryImage:
        item = await self.get_or_404(GalleryImage, image_id)
        updates = payload.model_dump(exclude_unset=True)
        return await self.update_audited(
            item,
            user_id=user_id,
            entity_type="gallery_image",
            updates=updates,
        )

    async def delete_image(self, user_id: uuid.UUID, image_id: uuid.UUID) -> None:
        item = await self.get_or_404(GalleryImage, image_id)
        safe_delete_image(item.cloudinary_public_id)
        await self.delete_audited(item, user_id=user_id, entity_type="gallery_image")
