"""FastAPI entrypoint. Real analysis endpoints land in Phase 3 (PRD §13)."""

from fastapi import FastAPI
from pydantic import BaseModel

from loadlab_stats import __version__

app = FastAPI(title="LoadLab Stats Service", version=__version__)


class HealthResponse(BaseModel):
    status: str
    version: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)
