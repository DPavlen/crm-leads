from src.routers.appeals import router as appeals
from src.routers.leads import router as leads
from src.routers.operators import router as operators
from src.routers.sources import router as sources
from src.routers.statistics import router as statistics

__all__ = [
    "operators",
    "sources",
    "appeals",
    "leads",
    "statistics",
]
