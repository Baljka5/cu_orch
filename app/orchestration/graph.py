from __future__ import annotations
from langgraph.graph import StateGraph, END
from app.orchestration.schemas import OrchestratorState
from app.orchestration.nodes import guard_node, reform_node, classify_node, call_agent_node, finalize_node

graph = StateGraph(OrchestratorState)

graph.add_node("guard", guard_node)
graph.add_node("reform", reform_node)
graph.add_node("classify", classify_node)
graph.add_node("call_agent", call_agent_node)
graph.add_node("finalize", finalize_node)

graph.set_entry_point("guard")

def guard_route(state: OrchestratorState):
    return "finalize" if state.blocked else "reform"

graph.add_conditional_edges("guard", guard_route)
graph.add_edge("reform", "classify")
graph.add_edge("classify", "call_agent")
graph.add_edge("call_agent", "finalize")
graph.add_edge("finalize", END)

compiled = graph.compile()

async def run_graph(user_id: str, text: str):
    state = OrchestratorState(user_id=user_id, raw_text=text)
    out = await compiled.ainvoke(state)
    return out
