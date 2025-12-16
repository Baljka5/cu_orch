from __future__ import annotations
from fastapi import FastAPI, Depends
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.security import require_api_key
from app.orchestration.router import router as orch_router

setup_logging()

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

# Protect API with API key header
app.include_router(orch_router, prefix="/api", dependencies=[Depends(require_api_key)])
