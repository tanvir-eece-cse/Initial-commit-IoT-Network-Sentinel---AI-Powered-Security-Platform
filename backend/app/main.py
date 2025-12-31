"""
IoT Network Sentinel - Backend Application
Main entry point for the FastAPI application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_client import make_asgi_app

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router
from app.core.database import create_db_and_tables
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.rate_limit import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events handler"""
    # Startup
    setup_logging()
    await create_db_and_tables()
    yield
    # Shutdown
    pass


def create_application() -> FastAPI:
    """Application factory pattern"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="""
        IoT Network Sentinel - AI-Powered IoT Network Security & Anomaly Detection Platform
        
        ## Features
        - Real-time network traffic analysis
        - ML-based anomaly detection
        - Intrusion detection system
        - Device fingerprinting
        - Security compliance reporting
        
        ## Author
        Md. Tanvir Hossain
        - GitHub: https://github.com/tanvir-eece-cse
        - LinkedIn: https://www.linkedin.com/in/tanvir-eece/
        - Email: tanvir.eece.mist@gmail.com
        """,
        version=settings.VERSION,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
        openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan
    )
    
    # Security Middleware
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Rate Limiting
    app.add_middleware(RateLimitMiddleware)
    
    # Mount Prometheus metrics
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
    
    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    
    return app


app = create_application()


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for Kubernetes probes"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "service": "iot-network-sentinel-backend"
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to IoT Network Sentinel API",
        "version": settings.VERSION,
        "docs": "/docs",
        "author": {
            "name": "Md. Tanvir Hossain",
            "github": "https://github.com/tanvir-eece-cse",
            "linkedin": "https://www.linkedin.com/in/tanvir-eece/",
            "email": "tanvir.eece.mist@gmail.com"
        }
    }
