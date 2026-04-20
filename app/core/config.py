import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "GitStat Next"
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    GITHUB_TOKEN_ENCRYPTION_KEY: str = "T-q_8E_988888888888888888888888888888888888=" # Default for local dev only

    # GitHub OAuth
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    GITHUB_CALLBACK_URL: str

    # AI
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    DEFAULT_AI_PROVIDER: str = "gemini"

    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"), 
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
