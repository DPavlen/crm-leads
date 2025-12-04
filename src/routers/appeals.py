from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import models, schemas, services
from src.database import get_db

router = APIRouter(prefix="/appeals", tags=["appeals"])


@router.post(
    "", response_model=schemas.AppealResponse, summary="Создать новое обращение", status_code=201
)
def create_appeal(appeal: schemas.AppealCreate, db: Session = Depends(get_db)):
    """
    Register a new appeal from a lead.

    Automatically:
    - Finds or creates lead by external_id
    - Selects operator based on source weights and load limits
    - Creates appeal record

    If no operators are available, creates appeal without assigned operator.
    """
    source = services.SourceService.get_source(db, appeal.source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    # Create appeal with automatic operator assignment
    db_appeal = services.AppealAssignmentService.create_appeal(db, appeal)

    return schemas.AppealResponse(
        id=db_appeal.id,
        lead_id=db_appeal.lead_id,
        source_id=db_appeal.source_id,
        operator_id=db_appeal.operator_id,
        message=db_appeal.message,
        is_active=db_appeal.is_active,
        created_at=db_appeal.created_at,
        operator_name=db_appeal.operator.name if db_appeal.operator else None,
        lead_external_id=db_appeal.lead.external_id,
        source_name=db_appeal.source.name,
    )


@router.get(
    "",
    response_model=list[schemas.AppealResponse],
    summary="Получить список обращений",
)
def get_appeals(
    source_id: int | None = None,
    operator_id: int | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
):
    """Get list of appeals with optional filters."""
    query = db.query(models.Appeal)

    if source_id is not None:
        query = query.filter(models.Appeal.source_id == source_id)
    if operator_id is not None:
        query = query.filter(models.Appeal.operator_id == operator_id)
    if is_active is not None:
        query = query.filter(models.Appeal.is_active == is_active)

    appeals = query.all()

    return [
        schemas.AppealResponse(
            id=a.id,
            lead_id=a.lead_id,
            source_id=a.source_id,
            operator_id=a.operator_id,
            message=a.message,
            is_active=a.is_active,
            created_at=a.created_at,
            operator_name=a.operator.name if a.operator else None,
            lead_external_id=a.lead.external_id,
            source_name=a.source.name,
        )
        for a in appeals
    ]
