from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import init_db
from src.routers import appeals, leads, operators, sources, statistics


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    init_db()
    yield


app = FastAPI(
    title="Mini-CRM Lead Distribution System",
    description="System for distributing leads to operators based on source weights and load limits",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(operators)
app.include_router(sources)
app.include_router(appeals)
app.include_router(leads)
app.include_router(statistics)
