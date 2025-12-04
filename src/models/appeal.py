"""Appeal model - represents customer appeal/request."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.lead import Lead
    from src.models.operator import Operator
    from src.models.source import Source


class Appeal(Base):
    """Specific appeal from lead via source, assigned to operator."""

    __tablename__ = "appeals"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"))
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    operator_id: Mapped[int | None] = mapped_column(ForeignKey("operators.id"))
    message: Mapped[str | None] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    closed_at: Mapped[datetime | None]

    lead: Mapped["Lead"] = relationship("Lead", back_populates="appeals")
    source: Mapped["Source"] = relationship("Source", back_populates="appeals")
    operator: Mapped[Optional["Operator"]] = relationship("Operator", back_populates="appeals")
