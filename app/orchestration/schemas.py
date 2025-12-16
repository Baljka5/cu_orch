from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal

AgentType = Literal["policy", "text2sql", "survey", "fallback"]

class OrchestratorState(BaseModel):
    user_id: str
    raw_text: str

    normalized_text: Optional[str] = None

    blocked: bool = False
    block_reason: Optional[str] = None

    agent: Optional[AgentType] = None
    agent_input: Optional[Dict[str, Any]] = None
    agent_output: Optional[Dict[str, Any]] = None

    final_answer: Optional[str] = None

    meta: Dict[str, Any] = Field(default_factory=dict)
