# CU Orchestrator (MVP)

FastAPI + LangGraph-based multi-agent orchestrator:
Guard -> Reformulate -> Classify -> Call Agent -> Finalize

## Quick start (local, without LLM)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```
Then open:
- POST http://127.0.0.1:8080/api/ask

Example:
```bash
curl -X POST http://127.0.0.1:8080/api/ask \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u1","text":"Өнгөрсөн сарын борлуулалт хэд вэ?"}'
```

## With local LLM (optional)
Run an OpenAI-compatible LLM server (e.g., vLLM) and set:
- `LLM_BASE_URL=http://127.0.0.1:8001`

## Env
Copy `.env.example` to `.env` and adjust.

## Notes
- Text2SQL agent is a safe stub: it *does not* execute SQL by default.
- Add your DB connectors + allowlist validation in `app/agents/text2sql_agent.py`.
