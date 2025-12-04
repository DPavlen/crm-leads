from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.operator import Operator
    from src.models.source import Source


class OperatorSourceWeight(Base):
    """Weight (competency) of operator for specific source."""

    __tablename__ = "operator_source_weights"

    id: Mapped[int] = mapped_column(primary_key=True)
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"))
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    weight: Mapped[int] = mapped_column(default=1)

    operator: Mapped["Operator"] = relationship("Operator", back_populates="source_weights")
    source: Mapped["Source"] = relationship("Source", back_populates="operator_weights")
