"""Statistics service for optimized data aggregation."""

from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src import models, schemas


class StatisticsService:
    """Service for getting statistics with optimized queries."""

    @staticmethod
    def get_operator_statistics(db: Session) -> list[schemas.OperatorStatistics]:
        """
        Get statistics for all operators with optimized query.
        """
        # Subquery for active appeals count (current_load)
        active_appeals_subq = (
            select(models.Appeal.operator_id, func.count(models.Appeal.id).label("active_count"))
            .where(models.Appeal.is_active == True)
            .group_by(models.Appeal.operator_id)
            .subquery()
        )

        # Subquery for total appeals count
        total_appeals_subq = (
            select(models.Appeal.operator_id, func.count(models.Appeal.id).label("total_count"))
            .group_by(models.Appeal.operator_id)
            .subquery()
        )

        # Main query with LEFT JOINs
        query = (
            db.query(
                models.Operator.id,
                models.Operator.name,
                models.Operator.is_active,
                models.Operator.max_load,
                func.coalesce(active_appeals_subq.c.active_count, 0).label("current_load"),
                func.coalesce(total_appeals_subq.c.total_count, 0).label("total_contacts"),
            )
            .outerjoin(active_appeals_subq, models.Operator.id == active_appeals_subq.c.operator_id)
            .outerjoin(total_appeals_subq, models.Operator.id == total_appeals_subq.c.operator_id)
        )

        results = query.all()

        return [
            schemas.OperatorStatistics(
                id=row.id,
                name=row.name,
                is_active=row.is_active,
                max_load=row.max_load,
                current_load=row.current_load,
                total_contacts=row.total_contacts,
            )
            for row in results
        ]

    @staticmethod
    def get_source_statistics(db: Session) -> list[schemas.SourceStatistics]:
        """
        Get statistics for all sources with detailed operator distribution.
        Shows weights, expected vs actual distribution percentages.
        """
        sources = db.query(models.Source).all()
        result = []

        for source in sources:
            # Get all operator weights for this source
            weights = (
                db.query(models.OperatorSourceWeight, models.Operator.name)
                .join(
                    models.Operator, models.OperatorSourceWeight.operator_id == models.Operator.id
                )
                .filter(models.OperatorSourceWeight.source_id == source.id)
                .all()
            )

            # Calculate total weight and total contacts
            total_weight = sum(w[0].weight for w in weights)
            total_contacts = (
                db.query(func.count(models.Appeal.id))
                .filter(models.Appeal.source_id == source.id)
                .scalar()
                or 0
            )

            # Build operator distribution details
            operators_details = []
            for weight_record, operator_name in weights:
                # Count contacts for this operator from this source
                contacts_count = (
                    db.query(func.count(models.Appeal.id))
                    .filter(
                        models.Appeal.source_id == source.id,
                        models.Appeal.operator_id == weight_record.operator_id,
                    )
                    .scalar()
                    or 0
                )

                # Calculate percentages
                expected_percent = (
                    (weight_record.weight / total_weight * 100) if total_weight > 0 else 0
                )
                actual_percent = (
                    (contacts_count / total_contacts * 100) if total_contacts > 0 else 0
                )

                operators_details.append(
                    schemas.OperatorAppealDetail(
                        operator_id=weight_record.operator_id,
                        operator_name=operator_name,
                        weight=weight_record.weight,
                        contacts_count=contacts_count,
                        expected_percent=round(expected_percent, 2),
                        actual_percent=round(actual_percent, 2),
                    )
                )

            result.append(
                schemas.SourceStatistics(
                    id=source.id,
                    name=source.name,
                    total_contacts=total_contacts,
                    operators_count=len(weights),
                    operators=operators_details,
                )
            )

        return result
