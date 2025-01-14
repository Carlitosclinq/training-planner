from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Training Planner"
    database_url: str = "postgresql://postgres:postgres@localhost/training_planner"
    jwt_secret: str = "your-secret-key"  # À changer en production
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    intervals_api_url: str = "https://intervals.icu/api/v1"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
