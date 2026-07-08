import uuid
from datetime import datetime
from typing import Any

from app.schemas.base import ORMModel


class AuditLogResponse(ORMModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    action: str
    entity_type: str
    entity_id: uuid.UUID | None
    changes: dict[str, Any]
    created_at: datetime
