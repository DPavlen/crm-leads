from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.appeal import Appeal
    from src.models.weight import OperatorSourceWeight


class Source(Base):
    """Channel/bot from which contacts arrive."""

    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str | None] = mapped_column(String)

    # Relationships
    operator_weights: Mapped[list["OperatorSourceWeight"]] = relationship(
        "OperatorSourceWeight", back_populates="source", cascade="all, delete-orphan"
    )
    appeals: Mapped[list["Appeal"]] = relationship("Appeal", back_populates="source")
