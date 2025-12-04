"""Operator service for CRUD operations."""

from typing import List, Optional

from sqlalchemy.orm import Session

from src import models, schemas


class OperatorService:
    """Service for managing operators."""

    @staticmethod
    def create_operator(db: Session, operator: schemas.OperatorCreate) -> models.Operator:
        """Create new operator."""
        db_operator = models.Operator(**operator.model_dump())
        db.add(db_operator)
        db.commit()
        db.refresh(db_operator)
        return db_operator

    @staticmethod
    def get_operators(db: Session) -> list[models.Operator]:
        """Get all operators."""
        return db.query(models.Operator).all()

    @staticmethod
    def get_operator(db: Session, operator_id: int) -> models.Operator | None:
        """Get operator by id."""
        return db.query(models.Operator).filter(models.Operator.id == operator_id).first()

    @staticmethod
    def update_operator(
        db: Session, operator_id: int, operator_update: schemas.OperatorUpdate
    ) -> models.Operator | None:
        """Update operator."""
        db_operator = OperatorService.get_operator(db, operator_id)
        if not db_operator:
            return None

        update_data = operator_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_operator, field, value)

        db.commit()
        db.refresh(db_operator)
        return db_operator
