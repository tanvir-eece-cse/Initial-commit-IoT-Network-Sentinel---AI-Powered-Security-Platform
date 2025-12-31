"""
ML Service Configuration
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """ML Service settings"""
    
    # Application
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Model paths
    MODEL_PATH: str = "./models"
    ISOLATION_FOREST_MODEL: str = "isolation_forest.joblib"
    RANDOM_FOREST_MODEL: str = "random_forest.joblib"
    AUTOENCODER_MODEL: str = "autoencoder.keras"
    
    # Model parameters
    ANOMALY_THRESHOLD: float = 0.5
    CONFIDENCE_THRESHOLD: float = 0.7
    
    # Feature engineering
    NUM_FEATURES: int = 20
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
