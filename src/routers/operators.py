from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import schemas, services
from src.database import get_db

router = APIRouter(prefix="/operators", tags=["operators"])


@router.post(
    "",
    response_model=schemas.OperatorResponse,
    summary="Создать нового операторов",
    status_code=201,
)
def create_operator(operator: schemas.OperatorCreate, db: Session = Depends(get_db)):
    db_operator = services.OperatorService.create_operator(db, operator)
    current_load = services.AppealAssignmentService.get_operator_current_load(db, db_operator.id)

    return schemas.OperatorResponse(
        id=db_operator.id,
        name=db_operator.name,
        is_active=db_operator.is_active,
        max_load=db_operator.max_load,
        current_load=current_load,
    )


@router.get(
    "",
    response_model=list[schemas.OperatorResponse],
    summary="Просмотр списка операторов",
)
def get_operators(db: Session = Depends(get_db)):
    """Get list of all operators with their current load."""
    operators = services.OperatorService.get_operators(db)

    return [
        schemas.OperatorResponse(
            id=op.id,
            name=op.name,
            is_active=op.is_active,
            max_load=op.max_load,
            current_load=services.AppealAssignmentService.get_operator_current_load(db, op.id),
        )
        for op in operators
    ]


@router.get(
    "/{operator_id}",
    response_model=schemas.OperatorResponse,
    summary="Просмотр оператора по id",
)
def get_operator(operator_id: int, db: Session = Depends(get_db)):
    """Get specific operator by ID."""
    operator = services.OperatorService.get_operator(db, operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")

    current_load = services.AppealAssignmentService.get_operator_current_load(db, operator.id)

    return schemas.OperatorResponse(
        id=operator.id,
        name=operator.name,
        is_active=operator.is_active,
        max_load=operator.max_load,
        current_load=current_load,
    )


@router.patch(
    "/{operator_id}",
    response_model=schemas.OperatorResponse,
    summary="Обновление оператора по id",
)
def update_operator(
    operator_id: int, operator_update: schemas.OperatorUpdate, db: Session = Depends(get_db)
):
    """Update operator (activity status, max load, name)."""
    operator = services.OperatorService.update_operator(db, operator_id, operator_update)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")

    current_load = services.AppealAssignmentService.get_operator_current_load(db, operator.id)

    return schemas.OperatorResponse(
        id=operator.id,
        name=operator.name,
        is_active=operator.is_active,
        max_load=operator.max_load,
        current_load=current_load,
    )
