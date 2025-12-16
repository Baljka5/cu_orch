import re
from typing import Literal

AgentType = Literal["policy", "text2sql", "survey", "fallback"]

def is_blocked(text: str) -> tuple[bool, str]:
    t = text.lower()
    # Minimal block rules: credentials, hacking, malware, etc.
    bad = [
        "password", "нууц үг", "token", "api key", "хак", "malware", "virus", "ddos",
        "credit card", "карт", "cvv"
    ]
    for w in bad:
        if w in t:
            return True, f"Contains sensitive/unsafe keyword: {w}"
    return False, ""

def reformulate(text: str) -> str:
    # MVP: trim + normalize spaces; real version uses LLM for galig->кирилл
    return re.sub(r"\s+", " ", text).strip()

def classify(text: str) -> AgentType:
    t = text.lower()
    # crude routing keywords
    if any(k in t for k in ["журам", "дүрэм", "policy", "заавар", "процедур", "хөдөлмөр"]):
        return "policy"
    if any(k in t for k in ["борлуул", "тайлан", "хэд", "хэмжээ", "дүн", "sql", "select", "өсөлт", "cagr"]):
        return "text2sql"
    if any(k in t for k in ["судалгаа", "асуулга", "spss", "questionnaire", "survey", "дүгнэлт"]):
        return "survey"
    return "fallback"
