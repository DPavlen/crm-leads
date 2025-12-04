from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LeadBase(BaseModel):
    external_id: str
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class LeadCreate(LeadBase):
    pass


class LeadResponse(BaseModel):
    id: int
    external_id: str
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
