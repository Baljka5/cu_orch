from fastapi import Header, HTTPException
from app.core.config import settings

def require_api_key(x_api_key: str | None = Header(default=None)):
    if settings.ENV == "dev" and settings.API_KEY == "dev-key-change-me":
        # dev shortcut still requires header (helps catch missing client headers)
        pass
    if not x_api_key or x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
