"""
Models API Endpoints
"""
from typing import Optional
from fastapi import APIRouter, HTTPException

from app.main import model_manager

router = APIRouter()


@router.get("")
async def list_models():
    """List all available models"""
    return model_manager.get_all_models()


@router.get("/{model_name}")
async def get_model_info(model_name: str):
    """Get information about a specific model"""
    info = model_manager.get_model_info(model_name)
    
    if "error" in info:
        raise HTTPException(status_code=404, detail=info["error"])
    
    return info


@router.get("/feature-importance/{model_name}")
async def get_feature_importance(model_name: str):
    """Get feature importance for a model"""
    importance = model_manager.get_feature_importance(model_name)
    
    if not importance:
        raise HTTPException(
            status_code=404,
            detail=f"Feature importance not available for {model_name}"
        )
    
    # Sort by importance
    sorted_importance = dict(
        sorted(importance.items(), key=lambda x: x[1], reverse=True)
    )
    
    return {
        "model_name": model_name,
        "feature_importance": sorted_importance
    }


@router.get("/metrics")
async def get_model_metrics(model_name: Optional[str] = None):
    """Get model performance metrics"""
    # In production, these would come from model evaluation
    demo_metrics = {
        "isolation_forest": {
            "accuracy": 0.942,
            "precision": 0.921,
            "recall": 0.958,
            "f1_score": 0.939,
            "false_positive_rate": 0.079,
            "training_samples": 1100,
            "last_trained": "2024-12-01T00:00:00Z"
        },
        "random_forest": {
            "accuracy": 0.978,
            "precision": 0.972,
            "recall": 0.981,
            "f1_score": 0.976,
            "false_positive_rate": 0.028,
            "training_samples": 1100,
            "last_trained": "2024-12-01T00:00:00Z"
        }
    }
    
    if model_name:
        if model_name not in demo_metrics:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        return {model_name: demo_metrics[model_name]}
    
    return demo_metrics
