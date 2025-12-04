from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import schemas, services
from src.database import get_db

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post(
    "", response_model=schemas.SourceResponse, summary="Создание нового источника", status_code=201
)
def create_source(source: schemas.SourceCreate, db: Session = Depends(get_db)):
    """Create a new source (bot/channel)."""
    return services.SourceService.create_source(db, source)


@router.get(
    "", response_model=list[schemas.SourceResponse], summary="Просмотр списка всех источников"
)
def get_sources(db: Session = Depends(get_db)):
    """Get list of all sources."""
    return services.SourceService.get_sources(db)


@router.get(
    "/{source_id}",
    response_model=schemas.SourceResponse,
    summary="Просмотр информации об источнике по ID",
)
def get_source(source_id: int, db: Session = Depends(get_db)):
    """Get specific source by ID."""
    source = services.SourceService.get_source(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.post(
    "/{source_id}/weights",
    response_model=list[schemas.OperatorSourceWeightResponse],
    summary="Настройка весов операторов для источника",
)
def configure_source_weights(
    source_id: int, weights: list[schemas.WeightConfig], db: Session = Depends(get_db)
):
    """
    Configure operator weights for a source.
    Replaces existing configuration.

    Example: [{"operator_id": 1, "weight": 10}, {"operator_id": 2, "weight": 30}]
    This means operator 1 gets 25% and operator 2 gets 75% of traffic.
    """
    source = services.SourceService.get_source(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    for weight_config in weights:
        operator = services.OperatorService.get_operator(db, weight_config.operator_id)
        if not operator:
            raise HTTPException(
                status_code=404, detail=f"Operator {weight_config.operator_id} not found"
            )

    config = schemas.SourceWeightConfig(source_id=source_id, weights=weights)
    db_weights = services.SourceService.configure_source_weights(db, config)

    return [
        schemas.OperatorSourceWeightResponse(
            id=w.id,
            operator_id=w.operator_id,
            source_id=w.source_id,
            weight=w.weight,
            operator_name=w.operator.name,
        )
        for w in db_weights
    ]


@router.get(
    "/{source_id}/weights",
    response_model=list[schemas.OperatorSourceWeightResponse],
    summary="Просмотр весов по id источника",
)
def get_source_weights(source_id: int, db: Session = Depends(get_db)):
    """Get weight configuration for a source."""

    source = services.SourceService.get_source(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    weights = services.SourceService.get_source_weights(db, source_id)

    return [
        schemas.OperatorSourceWeightResponse(
            id=w.id,
            operator_id=w.operator_id,
            source_id=w.source_id,
            weight=w.weight,
            operator_name=w.operator.name,
        )
        for w in weights
    ]
