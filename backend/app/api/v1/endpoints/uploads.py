from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status

from app.core.security import get_current_user
from app.models import User
from app.schemas import UploadImageResponse
from app.services.cloudinary_service import CloudinaryNotConfiguredError, CloudinaryUploadError, upload_image

router = APIRouter()


@router.post("/image", response_model=UploadImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_image_endpoint(
    file: UploadFile = File(...),
    folder: str = Query(default="poaley-chedec"),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> UploadImageResponse:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="יש להעלות קובץ תמונה בלבד")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="קובץ ריק")

    try:
        uploaded = upload_image(content, folder=folder)
    except CloudinaryNotConfiguredError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except CloudinaryUploadError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"שגיאת Cloudinary: {exc}",
        ) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="שגיאה בהעלאת התמונה") from exc

    return UploadImageResponse(url=uploaded["url"], public_id=uploaded["public_id"])
