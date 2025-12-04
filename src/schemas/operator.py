from typing import Optional

from pydantic import BaseModel, Field


class OperatorBase(BaseModel):
    name: str
    is_active: bool = True
    max_load: int = Field(default=10, gt=0)


class OperatorCreate(OperatorBase):
    pass


class OperatorUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None
    max_load: int | None = Field(default=None, gt=0)


class OperatorResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    max_load: int
    current_load: int = 0

    class Config:
        from_attributes = True
