"""
Machine Learning API Endpoints
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
import time
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
import httpx

from app.core.config import settings
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.network import (
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
)

router = APIRouter()


async def call_ml_service(endpoint: str, data: dict) -> dict:
    """Call the ML service API"""
    async with httpx.AsyncClient(timeout=settings.ML_SERVICE_TIMEOUT) as client:
        try:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}{endpoint}",
                json=data
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"ML service error: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"ML service unavailable: {str(e)}"
            )


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    current_user: User = Depends(get_current_user)
):
    """Get prediction for a single sample"""
    start_time = time.time()
    
    result = await call_ml_service("/api/v1/predict", {
        "features": request.features,
        "model_name": request.model_name
    })
    
    processing_time = (time.time() - start_time) * 1000
    
    return PredictionResponse(
        is_anomaly=result.get("is_anomaly", False),
        anomaly_type=result.get("anomaly_type"),
        confidence_score=result.get("confidence_score", 0.0),
        risk_score=result.get("risk_score", 0.0),
        model_used=result.get("model_used", request.model_name),
        processing_time_ms=processing_time,
        recommendations=result.get("recommendations")
    )


@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def batch_predict(
    request: BatchPredictionRequest,
    current_user: User = Depends(get_current_user)
):
    """Get predictions for multiple samples"""
    start_time = time.time()
    
    result = await call_ml_service("/api/v1/predict/batch", {
        "samples": request.samples,
        "model_name": request.model_name
    })
    
    processing_time = (time.time() - start_time) * 1000
    
    predictions = []
    anomalies_count = 0
    
    for pred in result.get("predictions", []):
        prediction = PredictionResponse(
            is_anomaly=pred.get("is_anomaly", False),
            anomaly_type=pred.get("anomaly_type"),
            confidence_score=pred.get("confidence_score", 0.0),
            risk_score=pred.get("risk_score", 0.0),
            model_used=pred.get("model_used", request.model_name),
            processing_time_ms=0,
            recommendations=pred.get("recommendations")
        )
        predictions.append(prediction)
        if pred.get("is_anomaly"):
            anomalies_count += 1
    
    return BatchPredictionResponse(
        predictions=predictions,
        total_samples=len(request.samples),
        anomalies_detected=anomalies_count,
        processing_time_ms=processing_time
    )


@router.get("/models")
async def list_models(
    current_user: User = Depends(get_current_user)
):
    """List available ML models"""
    result = await call_ml_service("/api/v1/models", {})
    return result


@router.get("/models/{model_name}")
async def get_model_info(
    model_name: str,
    current_user: User = Depends(get_current_user)
):
    """Get information about a specific model"""
    result = await call_ml_service(f"/api/v1/models/{model_name}", {})
    return result


@router.get("/metrics")
async def get_model_metrics(
    model_name: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get model performance metrics"""
    endpoint = "/api/v1/metrics"
    if model_name:
        endpoint += f"?model_name={model_name}"
    
    result = await call_ml_service(endpoint, {})
    return result


@router.post("/train")
async def trigger_training(
    model_name: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Trigger model training (background task)"""
    # In production, this would queue a training job
    return {
        "message": "Training job queued",
        "model_name": model_name,
        "status": "queued",
        "queued_at": datetime.utcnow().isoformat()
    }


@router.post("/evaluate")
async def evaluate_model(
    model_name: str,
    test_data: List[Dict[str, Any]],
    current_user: User = Depends(get_current_user)
):
    """Evaluate model on test data"""
    result = await call_ml_service("/api/v1/evaluate", {
        "model_name": model_name,
        "test_data": test_data
    })
    return result


@router.get("/feature-importance/{model_name}")
async def get_feature_importance(
    model_name: str,
    current_user: User = Depends(get_current_user)
):
    """Get feature importance for a model"""
    result = await call_ml_service(f"/api/v1/feature-importance/{model_name}", {})
    return result


@router.post("/anomaly-analysis")
async def analyze_anomaly(
    anomaly_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Get detailed analysis of an anomaly"""
    result = await call_ml_service("/api/v1/analyze", {
        "data": anomaly_data
    })
    return result
