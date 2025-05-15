import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Legal Assistant AI"


    CORS_ORIGINS: List[str] = ["*"]

    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-3-sonnet-20240229")

    class Config:
        env_file = ".env"

settings = Settings()