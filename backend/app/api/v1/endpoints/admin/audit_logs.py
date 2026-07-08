from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models import AuditLog, User
from app.schemas import AuditLogResponse
from app.services.admin_service import AdminService
from app.services.dependencies import get_admin_service

router = APIRouter()


@router.get("", response_model=list[AuditLogResponse])
async def list_audit_logs(
    current_user: Annotated[User, Depends(get_current_user)],
    service: AdminService = Depends(get_admin_service),
) -> list[AuditLog]:
    return await service.list_audit_logs()
