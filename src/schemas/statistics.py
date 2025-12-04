from typing import List

from pydantic import BaseModel


class OperatorStatistics(BaseModel):
    id: int
    name: str
    is_active: bool
    max_load: int
    current_load: int
    total_contacts: int


class OperatorAppealDetail(BaseModel):
    """Detailed operator appeal info for a source."""

    operator_id: int
    operator_name: str
    weight: int
    contacts_count: int
    expected_percent: float
    actual_percent: float


class SourceStatistics(BaseModel):
    id: int
    name: str
    total_contacts: int
    operators_count: int
    operators: list[OperatorAppealDetail]
