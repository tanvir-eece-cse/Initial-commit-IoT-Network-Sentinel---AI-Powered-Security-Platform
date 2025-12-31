"""
ML Service API Router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import predict, models

api_router = APIRouter()

api_router.include_router(predict.router, prefix="/predict", tags=["Prediction"])
api_router.include_router(models.router, prefix="/models", tags=["Models"])
