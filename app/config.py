import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Server
    PORT: int = 8000
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/payment_api"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # USDT
    USDT_PRECISION: int = 6
    MIN_TRANSFER_AMOUNT: float = 0.000001
    
    class Config:
        env_file = ".env"


settings = Settings() 