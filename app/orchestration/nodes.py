from __future__ import annotations
import json
import logging
from app.orchestration.schemas import OrchestratorState
from app.core.config import settings
from app.llm.client import LLMClient
from app.llm import prompts
from app.llm.heuristics import is_blocked, reformulate, classify

from app.agents.text2sql_agent import run_text2sql
from app.agents.policy_agent import run_policy
from app.agents.survey_agent import run_survey

logger = logging.getLogger(__name__)
llm = LLMClient()

def _try_parse_json(s: str):
    try:
        return json.loads(s)
    except Exception:
        return None

async def guard_node(state: OrchestratorState) -> OrchestratorState:
    # Try LLM guard; fallback to heuristics
    try:
        out = await llm.chat([{"role":"user","content": prompts.GUARD_PROMPT + "\nАсуулт: " + state.raw_text}], temperature=0.0)
        data = _try_parse_json(out)
        if isinstance(data, dict) and "blocked" in data:
            state.blocked = bool(data.get("blocked"))
            state.block_reason = str(data.get("reason", ""))
        else:
            b, r = is_blocked(state.raw_text)
            state.blocked, state.block_reason = b, r
    except Exception as e:
        logger.warning("LLM guard failed; using heuristics", extra={"err": str(e)})
        b, r = is_blocked(state.raw_text)
        state.blocked, state.block_reason = b, r

    state.meta["guard"] = {"blocked": state.blocked, "reason": state.block_reason}
    return state

async def reform_node(state: OrchestratorState) -> OrchestratorState:
    if state.blocked:
        return state

    try:
        out = await llm.chat([{"role":"user","content": prompts.REFORM_PROMPT + "\nАсуулт: " + state.raw_text}], temperature=0.0)
        state.normalized_text = out.strip()
    except Exception as e:
        logger.warning("LLM reform failed; using heuristics", extra={"err": str(e)})
        state.normalized_text = reformulate(state.raw_text)

    state.meta["reform"] = {"normalized": state.normalized_text}
    return state

async def classify_node(state: OrchestratorState) -> OrchestratorState:
    if state.blocked:
        return state

    q = state.normalized_text or state.raw_text
    try:
        out = await llm.chat([{"role":"user","content": prompts.CLASSIFY_PROMPT + "\nАсуулт: " + q}], temperature=0.0)
        data = _try_parse_json(out)
        if isinstance(data, dict) and "agent" in data:
            state.agent = data["agent"]
        else:
            state.agent = classify(q)
    except Exception as e:
        logger.warning("LLM classify failed; using heuristics", extra={"err": str(e)})
        state.agent = classify(q)

    state.agent_input = {"query": q}
    state.meta["classify"] = {"agent": state.agent}
    return state

async def call_agent_node(state: OrchestratorState) -> OrchestratorState:
    if state.blocked:
        return state

    q = (state.agent_input or {}).get("query") or state.normalized_text or state.raw_text

    if state.agent == "text2sql":
        state.agent_output = await run_text2sql(q, user_id=state.user_id)
    elif state.agent == "policy":
        state.agent_output = await run_policy(q, user_id=state.user_id)
    elif state.agent == "survey":
        state.agent_output = await run_survey(q, user_id=state.user_id)
    else:
        state.agent_output = {"answer": "Fallback: Одоогоор тусгай агент холбогдоогүй байна."}

    return state

async def finalize_node(state: OrchestratorState) -> OrchestratorState:
    if state.blocked:
        state.final_answer = f"Уучлаарай, энэ асуултад хариулах боломжгүй. Шалтгаан: {state.block_reason}"
        return state

    out = state.agent_output or {}
    ans = out.get("answer") if isinstance(out, dict) else str(out)
    state.final_answer = ans
    return state
