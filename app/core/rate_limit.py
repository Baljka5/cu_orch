import time
from dataclasses import dataclass
from typing import Dict
from fastapi import HTTPException
from app.core.config import settings

@dataclass
class Bucket:
    tokens: float
    last: float

_buckets: Dict[str, Bucket] = {}

def rate_limit(user_id: str):
    now = time.time()
    rate = settings.RATE_LIMIT_PER_MINUTE / 60.0
    cap = float(settings.RATE_LIMIT_PER_MINUTE)

    b = _buckets.get(user_id)
    if not b:
        b = Bucket(tokens=cap, last=now)
        _buckets[user_id] = b

    # refill
    elapsed = now - b.last
    b.tokens = min(cap, b.tokens + elapsed * rate)
    b.last = now

    if b.tokens < 1.0:
        raise HTTPException(status_code=429, detail="Too Many Requests")
    b.tokens -= 1.0
