from typing import List, Optional

from pydantic import BaseModel, Field


class WeightConfig(BaseModel):
    operator_id: int
    weight: int = Field(gt=0)


class SourceWeightConfig(BaseModel):
    source_id: int
    weights: list[WeightConfig]


class OperatorSourceWeightResponse(BaseModel):
    id: int
    operator_id: int
    source_id: int
    weight: int
    operator_name: str | None = None

    class Config:
        from_attributes = True
