"""Source service for managing sources and weight configurations."""

from typing import List, Optional

from sqlalchemy.orm import Session

from src import models, schemas


class SourceService:
    """Service for managing sources and weight configurations."""

    @staticmethod
    def create_source(db: Session, source: schemas.SourceCreate) -> models.Source:
        """Create new source."""
        db_source = models.Source(**source.model_dump())
        db.add(db_source)
        db.commit()
        db.refresh(db_source)
        return db_source

    @staticmethod
    def get_sources(db: Session) -> list[models.Source]:
        """Get all sources."""
        return db.query(models.Source).all()

    @staticmethod
    def get_source(db: Session, source_id: int) -> models.Source | None:
        """Get source by id."""
        return db.query(models.Source).filter(models.Source.id == source_id).first()

    @staticmethod
    def configure_source_weights(
        db: Session, config: schemas.SourceWeightConfig
    ) -> list[models.OperatorSourceWeight]:
        """
        Configure operator weights for a source.
        Replaces existing configuration.
        """
        # Delete existing weights for this source
        db.query(models.OperatorSourceWeight).filter(
            models.OperatorSourceWeight.source_id == config.source_id
        ).delete()

        new_weights = []
        for weight_config in config.weights:
            weight = models.OperatorSourceWeight(
                operator_id=weight_config.operator_id,
                source_id=config.source_id,
                weight=weight_config.weight,
            )
            db.add(weight)
            new_weights.append(weight)

        db.commit()
        for weight in new_weights:
            db.refresh(weight)

        return new_weights

    @staticmethod
    def get_source_weights(db: Session, source_id: int) -> list[models.OperatorSourceWeight]:
        """Get all weight configurations for a source."""
        return (
            db.query(models.OperatorSourceWeight)
            .filter(models.OperatorSourceWeight.source_id == source_id)
            .all()
        )
