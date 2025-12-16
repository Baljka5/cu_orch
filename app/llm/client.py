from __future__ import annotations
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings

class LLMClient:
    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or settings.LLM_BASE_URL).rstrip("/")
        self.model = model or settings.LLM_MODEL

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
    async def chat(self, messages, temperature: float = 0.0) -> str:
        """Calls an OpenAI-compatible chat completion endpoint.
        If the endpoint is unreachable, raises an exception.
        """
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                },
            )
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"]
