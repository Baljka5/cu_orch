from __future__ import annotations

from typing import Any, Dict, Optional

from langgraph.graph import StateGraph, END

from app.orchestration.schemas import OrchestratorState
from app.orchestration.nodes import (
    guard_node,
    reform_node,
    classify_node,
    call_agent_node,
    finalize_node,
)

# ---------------------------------------------------------
# Build LangGraph
# ---------------------------------------------------------

graph = StateGraph(OrchestratorState)

# Nodes
graph.add_node("guard", guard_node)
graph.add_node("reform", reform_node)
graph.add_node("classify", classify_node)
graph.add_node("call_agent", call_agent_node)
graph.add_node("finalize", finalize_node)

# Entry
graph.set_entry_point("guard")

# ---------------------------------------------------------
# Routing logic
# ---------------------------------------------------------

def guard_route(state: OrchestratorState) -> str:
    """
    If request is blocked → skip everything and finalize immediately.
    """
    return "finalize" if state.blocked else "reform"


graph.add_conditional_edges("guard", guard_route)

# Normal flow
graph.add_edge("reform", "classify")
graph.add_edge("classify", "call_agent")
graph.add_edge("call_agent", "finalize")
graph.add_edge("finalize", END)

# ---------------------------------------------------------
# Compile graph
# ---------------------------------------------------------

compiled_graph = graph.compile()

# ---------------------------------------------------------
# Public entrypoint (used by router)
# ---------------------------------------------------------

async def run_graph(
    user_id: str,
    text: str,
    meta: Optional[Dict[str, Any]] = None,
) -> OrchestratorState:
    """
    Run orchestration graph and return final OrchestratorState.

    This function is the ONLY thing router.py should import.
    """

    # Initial state
    state = OrchestratorState(
        user_id=user_id,
        raw_text=text,
    )

    # Optional meta (safe attach)
    if meta:
        try:
            state.meta = meta  # type: ignore[attr-defined]
        except Exception:
            pass

    # Run graph
    result: OrchestratorState = await compiled_graph.ainvoke(state)
    return result
