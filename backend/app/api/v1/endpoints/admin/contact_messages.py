from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models import ContactMessage, User
from app.schemas import ContactMessageResponse
from app.services.admin_service import AdminService
from app.services.dependencies import get_admin_service

router = APIRouter()


@router.get("", response_model=list[ContactMessageResponse])
async def list_contact_messages(
    current_user: Annotated[User, Depends(get_current_user)],
    service: AdminService = Depends(get_admin_service),
) -> list[ContactMessage]:
    return await service.list_contact_messages()
