# app/orchestration/router.py

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field

from app.core.config import settings

from app.orchestration.graph import run_orchestration


router = APIRouter(prefix="/api", tags=["orchestration"])


# ----------------------------
# Security
# ----------------------------
async def verify_api_key(x_api_key: str = Header(default="")) -> None:
    expected = getattr(settings, "API_KEY", "") or ""
    if expected and x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )


# ----------------------------
# Schemas
# ----------------------------
class AskRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    meta: Dict[str, Any] = Field(default_factory=dict)


class AskResponse(BaseModel):
    user_id: str
    blocked: bool = False
    category: Optional[str] = None
    agent: Optional[str] = None
    final_answer: str = ""
    meta: Dict[str, Any] = Field(default_factory=dict)


# ----------------------------
# Helpers
# ----------------------------
def _get(o: Any, k: str, default: Any = None) -> Any:
    if isinstance(o, dict):
        return o.get(k, default)
    return getattr(o, k, default)


def _normalize_output(out: Any, req: AskRequest) -> AskResponse:
    user_id = _get(out, "user_id", req.user_id)

    blocked = bool(_get(out, "blocked", False))
    category = _get(out, "category", None)
    agent = _get(out, "agent", None)

    final_answer = (
        _get(out, "final_answer", None)
        or _get(out, "answer", None)
        or _get(out, "response", None)
        or _get(out, "message", None)
        or ""
    )

    meta = _get(out, "meta", None)
    if not isinstance(meta, dict):
        meta = {}

    return AskResponse(
        user_id=user_id,
        blocked=blocked,
        category=category,
        agent=agent,
        final_answer=str(final_answer),
        meta=meta,
    )


# ----------------------------
# Routes
# ----------------------------
@router.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@router.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest, _: None = Depends(verify_api_key)) -> AskResponse:
    try:
        out = await run_orchestration(user_id=req.user_id, text=req.text, meta=req.meta)
        return _normalize_output(out, req)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Orchestration failed: {type(e).__name__}: {e}",
        )
