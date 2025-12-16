from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "cu-orchestrator"
    ENV: str = "dev"

    LLM_BASE_URL: str = "http://127.0.0.1:8001"
    LLM_MODEL: str = "local"

    API_KEY: str = "dev-key-change-me"
    RATE_LIMIT_PER_MINUTE: int = 60

settings = Settings()
