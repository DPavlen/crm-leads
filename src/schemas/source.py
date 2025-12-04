from typing import Optional

from pydantic import BaseModel


class SourceBase(BaseModel):
    name: str
    description: str | None = None


class SourceCreate(SourceBase):
    pass


class SourceResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
