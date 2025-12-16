from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from app.orchestration.graph import run_graph
from app.core.rate_limit import rate_limit

router = APIRouter()

class AskReq(BaseModel):
    user_id: str
    text: str

@router.post("/ask")
async def ask(req: AskReq):
    rate_limit(req.user_id)
    out = await run_graph(user_id=req.user_id, text=req.text)
    return {
        "user_id": out.user_id,
        "raw_text": out.raw_text,
        "normalized_text": out.normalized_text,
        "blocked": out.blocked,
        "block_reason": out.block_reason,
        "agent": out.agent,
        "agent_output": out.agent_output,
        "final_answer": out.final_answer,
        "meta": out.meta,
    }
