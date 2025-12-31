"""
IoT Network Sentinel - ML Service
Main entry point for the Machine Learning service
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router
from app.services.model_manager import ModelManager


model_manager = ModelManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events handler"""
    # Startup - Load ML models
    model_manager.load_models()
    yield
    # Shutdown
    pass


def create_application() -> FastAPI:
    """Application factory pattern"""
    app = FastAPI(
        title="IoT Network Sentinel - ML Service",
        description="""
        Machine Learning Service for IoT Network Security
        
        Provides:
        - Anomaly detection using Isolation Forest
        - Attack classification using Random Forest
        - Deep learning models for sequential anomaly detection
        - Device fingerprinting
        
        Author: Md. Tanvir Hossain
        GitHub: https://github.com/tanvir-eece-cse
        """,
        version=settings.VERSION,
        lifespan=lifespan
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    return app


app = create_application()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "service": "ml-service",
        "models_loaded": model_manager.models_loaded
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "IoT Network Sentinel - ML Service",
        "version": settings.VERSION,
        "author": {
            "name": "Md. Tanvir Hossain",
            "github": "https://github.com/tanvir-eece-cse"
        }
    }
