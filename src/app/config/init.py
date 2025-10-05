from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Drive-Thru Ordering System"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-change-in-production"

    # Database
    DATABASE_URL: str = "postgresql://appuser:devpassword@localhost/drivethru"
    CREATE_TABLES: bool = True

    # Redis
    REDIS_URL: str = "redis://:devpassword@localhost:6379/0"

    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]

    # LLM Configuration
    LOCAL_LLM_MODEL: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    MODEL_CACHE_DIR: str = "./model_cache"

    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    DEEPGRAM_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()