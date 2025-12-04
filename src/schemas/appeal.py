from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AppealCreate(BaseModel):
    lead_external_id: str
    source_id: int
    message: str | None = None
    lead_name: str | None = None
    lead_email: str | None = None
    lead_phone: str | None = None


class AppealResponse(BaseModel):
    id: int
    lead_id: int
    source_id: int
    operator_id: int | None = None
    message: str | None = None
    is_active: bool
    created_at: datetime

    operator_name: str | None = None
    lead_external_id: str | None = None
    source_name: str | None = None

    class Config:
        from_attributes = True
