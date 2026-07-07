import cloudinary
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryApiError

from app.core.config import settings


class CloudinaryNotConfiguredError(Exception):
    pass


class CloudinaryUploadError(Exception):
    pass


def is_cloudinary_configured() -> bool:
    return bool(
        settings.cloudinary_cloud_name
        and settings.cloudinary_api_key
        and settings.cloudinary_api_secret
    )


def configure_cloudinary() -> None:
    if not is_cloudinary_configured():
        raise CloudinaryNotConfiguredError(
            "יש להגדיר CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY ו-CLOUDINARY_API_SECRET בקובץ .env"
        )
    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )


def upload_image(file_bytes: bytes, folder: str = "poaley-chedec") -> dict[str, str]:
    configure_cloudinary()
    try:
        result = cloudinary.uploader.upload(file_bytes, folder=folder)
    except CloudinaryApiError as exc:
        raise CloudinaryUploadError(str(exc)) from exc
    return {
        "public_id": result["public_id"],
        "url": result["secure_url"],
    }


def delete_image(public_id: str | None) -> None:
    if not public_id:
        return
    configure_cloudinary()
    cloudinary.uploader.destroy(public_id)
