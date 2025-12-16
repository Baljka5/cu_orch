from __future__ import annotations
import json
from pathlib import Path
import asyncio
from app.orchestration.graph import run_graph

TESTCASES = Path(__file__).parent / "testcases.jsonl"

async def run():
    ok = 0
    total = 0
    for line in TESTCASES.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        tc = json.loads(line)
        total += 1
        out = await run_graph(user_id="eval", text=tc["input"])
        exp = tc["expected_agent"]
        if exp == "blocked":
            passed = out.blocked is True
        else:
            passed = out.agent == exp and out.blocked is False
        print(f"[{ 'OK' if passed else 'FAIL' }] input={tc['input']} agent={out.agent} blocked={out.blocked}")
        ok += 1 if passed else 0
    print(f"Passed {ok}/{total}")

if __name__ == "__main__":
    asyncio.run(run())
