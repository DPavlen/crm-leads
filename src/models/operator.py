from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.appeal import Appeal
    from src.models.weight import OperatorSourceWeight


class Operator(Base):
    """Operator who handles leads from various sources."""

    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)
    max_load: Mapped[int] = mapped_column(default=10)

    source_weights: Mapped[list["OperatorSourceWeight"]] = relationship(
        "OperatorSourceWeight", back_populates="operator", cascade="all, delete-orphan"
    )
    appeals: Mapped[list["Appeal"]] = relationship("Appeal", back_populates="operator")
