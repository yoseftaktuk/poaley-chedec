from app.services.cloudinary_service import CloudinaryNotConfiguredError, delete_image


def safe_delete_image(public_id: str | None) -> None:
    if not public_id:
        return
    try:
        delete_image(public_id)
    except CloudinaryNotConfiguredError:
        pass
    except Exception:
        pass
