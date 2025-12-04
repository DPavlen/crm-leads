from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import models, schemas
from src.database import get_db

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get(
    "",
    response_model=list[schemas.LeadResponse],
    summary="Просмотр списка лидов",
)
def get_leads(db: Session = Depends(get_db)):
    """Get list of all leads."""
    return db.query(models.Lead).all()


@router.get(
    "/{lead_id}",
    response_model=schemas.LeadResponse,
    summary="Просмотр лида по ID",
)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get specific lead by ID."""
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.get(
    "/{lead_id}/appeals",
    response_model=list[schemas.AppealResponse],
    summary="Просмотр обращений по ID лида",
)
def get_lead_appeals(lead_id: int, db: Session = Depends(get_db)):
    """Get all appeals for a specific lead (showing appeals from different sources)."""
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    appeals = db.query(models.Appeal).filter(models.Appeal.lead_id == lead_id).all()

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
