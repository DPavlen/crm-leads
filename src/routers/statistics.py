from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src import schemas, services
from src.database import get_db

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get(
    "/operators",
    response_model=list[schemas.OperatorStatistics],
    summary="Просмотр статистики загруженности операторов",
)
def get_operator_statistics(db: Session = Depends(get_db)):
    """Get statistics for all operators."""
    return services.StatisticsService.get_operator_statistics(db)


@router.get(
    "/sources",
    response_model=list[schemas.SourceStatistics],
    summary="Просмотр статистики источников по процентному соотношению операторов",
)
def get_source_statistics(db: Session = Depends(get_db)):
    """
    Get statistics for all sources with detailed operator distribution.
    Shows weights, expected vs actual distribution percentages.
    """
    return services.StatisticsService.get_source_statistics(db)
