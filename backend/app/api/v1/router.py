"""
API Router Configuration
Aggregates all API endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, devices, anomalies, network, ml, dashboard

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(devices.router, prefix="/devices", tags=["Devices"])
api_router.include_router(anomalies.router, prefix="/anomalies", tags=["Anomalies"])
api_router.include_router(network.router, prefix="/network", tags=["Network"])
api_router.include_router(ml.router, prefix="/ml", tags=["Machine Learning"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
