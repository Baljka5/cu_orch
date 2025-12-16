from __future__ import annotations

async def run_survey(question: str, user_id: str):
    # TODO: connect to your survey summaries/metrics or a report store
    return {
        "answer": (
            "Survey Agent (MVP): Судалгааны үр дүнгийн өгөгдлийн эх үүсвэр холбогдоогүй байна.\n"
            f"Таны асуулт: {question}\n"
            "Дараагийн алхам: урьдчилсан summary (CSV/DB) эсвэл RAG тайлан холбох."
        )
    }
