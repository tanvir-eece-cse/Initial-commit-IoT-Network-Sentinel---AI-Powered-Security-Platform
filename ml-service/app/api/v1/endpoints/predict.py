"""
Prediction API Endpoints
"""
from typing import List, Dict, Any
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.main import model_manager

router = APIRouter()


class PredictionRequest(BaseModel):
    """Prediction request schema"""
    features: Dict[str, Any]
    model_name: str = "isolation_forest"


class BatchPredictionRequest(BaseModel):
    """Batch prediction request schema"""
    samples: List[Dict[str, Any]]
    model_name: str = "isolation_forest"


@router.post("")
async def predict(request: PredictionRequest):
    """Get prediction for a single sample"""
    if not model_manager.models_loaded:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    start_time = time.time()
    
    result = model_manager.predict_anomaly(
        request.features,
        request.model_name
    )
    
    result["processing_time_ms"] = (time.time() - start_time) * 1000
    
    return result


@router.post("/batch")
async def batch_predict(request: BatchPredictionRequest):
    """Get predictions for multiple samples"""
    if not model_manager.models_loaded:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    start_time = time.time()
    
    predictions = model_manager.predict_batch(
        request.samples,
        request.model_name
    )
    
    anomalies_count = sum(1 for p in predictions if p["is_anomaly"])
    
    return {
        "predictions": predictions,
        "total_samples": len(request.samples),
        "anomalies_detected": anomalies_count,
        "processing_time_ms": (time.time() - start_time) * 1000
    }


@router.post("/analyze")
async def analyze_anomaly(data: Dict[str, Any]):
    """Get detailed analysis of traffic data"""
    if not model_manager.models_loaded:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    # Get predictions from all models
    isolation_result = model_manager.predict_anomaly(data, "isolation_forest")
    rf_result = model_manager.predict_anomaly(data, "random_forest")
    
    return {
        "isolation_forest_analysis": isolation_result,
        "random_forest_analysis": rf_result,
        "combined_risk_score": max(
            isolation_result["risk_score"],
            rf_result["risk_score"]
        ),
        "consensus": isolation_result["is_anomaly"] == rf_result["is_anomaly"],
        "recommendations": list(set(
            isolation_result.get("recommendations", []) +
            rf_result.get("recommendations", [])
        ))
    }
