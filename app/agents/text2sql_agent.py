from __future__ import annotations
import re

def validate_sql(sql: str) -> tuple[bool, str]:
    s = sql.strip().lower()
    if not s.startswith("select"):
        return False, "Only SELECT queries are allowed."
    if re.search(r"\b(drop|alter|truncate|insert|update|delete|create)\b", s):
        return False, "DDL/DML statements are not allowed."
    return True, ""

async def run_text2sql(question: str, user_id: str):
    # MVP: returns a *draft* SQL template only (does not execute)
    draft_sql = f"""SELECT
  /* TODO: choose metrics */
  *
FROM BI_DB.some_table
WHERE 1=1
  /* TODO: add date filter for last month */
LIMIT 100;"""

    ok, reason = validate_sql(draft_sql)
    if not ok:
        return {"answer": f"SQL validation failed: {reason}", "sql": draft_sql}

    return {
        "answer": (
            "Text2SQL Agent (MVP): Дараах SQL нь *draft* (одоогоор ажиллуулахгүй).\n"
            "Хэрвээ та ClickHouse холбоно гэвэл: allowlist table, role filter, timeout, max rows хийж байж ажиллуулна."
        ),
        "sql": draft_sql,
    }
