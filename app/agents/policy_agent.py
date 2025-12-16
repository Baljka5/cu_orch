from __future__ import annotations

async def run_policy(question: str, user_id: str):
    # TODO: replace with RAG over company policy docs (vector DB) or knowledge base
    return {
        "answer": (
            "Policy Agent (MVP): Одоогоор журам/дотоод баримтын мэдлэгийн сан холбогдоогүй байна.\n"
            f"Таны асуулт: {question}\n"
            "Дараагийн алхам: app/data/policies дээр баримтаа байршуулж RAG холбох."
        )
    }
