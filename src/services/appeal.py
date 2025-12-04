"""Appeal assignment service."""

import random
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from src import models, schemas


class AppealAssignmentService:
    """Assigns appeals to operators using weighted distribution."""

    @staticmethod
    def get_operator_current_load(db: Session, operator_id: int) -> int:
        """Get current load of operator (count of active appeals)."""
        return (
            db.query(models.Appeal)
            .filter(models.Appeal.operator_id == operator_id, models.Appeal.is_active == True)
            .count()
        )

    @staticmethod
    def get_or_create_lead(db: Session, appeal_data: schemas.AppealCreate) -> models.Lead:
        """Find existing lead by external_id or create new one."""
        lead = (
            db.query(models.Lead)
            .filter(models.Lead.external_id == appeal_data.lead_external_id)
            .first()
        )

        if not lead:
            lead = models.Lead(
                external_id=appeal_data.lead_external_id,
                name=appeal_data.lead_name,
                email=appeal_data.lead_email,
                phone=appeal_data.lead_phone,
            )
            db.add(lead)
            db.commit()
            db.refresh(lead)

        return lead

    @staticmethod
    def get_available_operators(db: Session, source_id: int) -> list[tuple[models.Operator, int]]:
        """Get available operators for source with weights (active + not overloaded)."""
        # Get all operator-weight configs for this source
        weights = (
            db.query(models.OperatorSourceWeight)
            .filter(models.OperatorSourceWeight.source_id == source_id)
            .all()
        )

        available = []

        for weight_config in weights:
            operator = weight_config.operator

            if not operator.is_active:
                continue

            # Check current load
            current_load = AppealAssignmentService.get_operator_current_load(db, operator.id)
            if current_load >= operator.max_load:
                continue

            available.append((operator, weight_config.weight))

        return available

    @staticmethod
    def select_operator_by_weight(
        operators_with_weights: list[tuple[models.Operator, int]]
    ) -> models.Operator | None:
        """Select operator using weighted random choice."""
        if not operators_with_weights:
            return None

        operators = [op for op, _ in operators_with_weights]
        weights = [weight for _, weight in operators_with_weights]

        # Weighted random choice
        selected = random.choices(operators, weights=weights, k=1)[0]
        return selected

    @staticmethod
    def create_appeal(db: Session, appeal_data: schemas.AppealCreate) -> models.Appeal:
        """Create appeal and auto-assign to available operator by weight."""
        lead = AppealAssignmentService.get_or_create_lead(db, appeal_data)
        available_operators = AppealAssignmentService.get_available_operators(
            db, appeal_data.source_id
        )

        selected_operator = None
        if available_operators:
            selected_operator = AppealAssignmentService.select_operator_by_weight(
                available_operators
            )

        appeal = models.Appeal(
            lead_id=lead.id,
            source_id=appeal_data.source_id,
            operator_id=selected_operator.id if selected_operator else None,
            message=appeal_data.message,
            is_active=True,
        )

        db.add(appeal)
        db.commit()
        db.refresh(appeal)

        return appeal
