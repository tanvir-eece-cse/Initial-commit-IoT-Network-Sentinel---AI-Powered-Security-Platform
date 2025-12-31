"""
Pydantic Schemas for Network and Security operations
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, IPvAnyAddress
from app.models.network import DeviceStatus, AnomalyType, SeverityLevel


# Device Schemas
class DeviceBase(BaseModel):
    """Base device schema"""
    name: str = Field(..., max_length=255)
    device_type: Optional[str] = None
    manufacturer: Optional[str] = None
    ip_address: str
    mac_address: Optional[str] = None
    hostname: Optional[str] = None


class DeviceCreate(DeviceBase):
    """Schema for device creation"""
    device_id: str = Field(..., max_length=100)


class DeviceUpdate(BaseModel):
    """Schema for device update"""
    name: Optional[str] = Field(None, max_length=255)
    device_type: Optional[str] = None
    manufacturer: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    hostname: Optional[str] = None
    status: Optional[DeviceStatus] = None
    is_trusted: Optional[bool] = None


class DeviceResponse(DeviceBase):
    """Schema for device response"""
    id: int
    device_id: str
    status: DeviceStatus
    last_seen: Optional[datetime] = None
    risk_score: float
    is_trusted: bool
    fingerprint: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DeviceListResponse(BaseModel):
    """Schema for paginated device list"""
    items: List[DeviceResponse]
    total: int
    page: int
    page_size: int


# Anomaly Schemas
class AnomalyBase(BaseModel):
    """Base anomaly schema"""
    anomaly_type: AnomalyType
    severity: SeverityLevel
    title: str = Field(..., max_length=255)
    description: Optional[str] = None


class AnomalyCreate(AnomalyBase):
    """Schema for anomaly creation"""
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    protocol: Optional[str] = None
    confidence_score: float = Field(0.0, ge=0.0, le=1.0)
    ml_model_used: Optional[str] = None
    raw_features: Optional[Dict[str, Any]] = None
    device_id: Optional[int] = None


class AnomalyUpdate(BaseModel):
    """Schema for anomaly update"""
    is_resolved: Optional[bool] = None
    is_false_positive: Optional[bool] = None
    resolution_notes: Optional[str] = None


class AnomalyResponse(AnomalyBase):
    """Schema for anomaly response"""
    id: int
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    protocol: Optional[str] = None
    confidence_score: float
    ml_model_used: Optional[str] = None
    is_resolved: bool
    is_false_positive: bool
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    device_id: Optional[int] = None
    detected_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnomalyListResponse(BaseModel):
    """Schema for paginated anomaly list"""
    items: List[AnomalyResponse]
    total: int
    page: int
    page_size: int


# Traffic Schemas
class TrafficStats(BaseModel):
    """Traffic statistics schema"""
    timestamp: datetime
    bytes_in: int
    bytes_out: int
    packets_in: int
    packets_out: int
    connections: int
    tcp_connections: int
    udp_connections: int
    icmp_packets: int
    blocked_connections: int
    anomalies_detected: int


class TrafficSummary(BaseModel):
    """Traffic summary schema"""
    total_bytes_in: int
    total_bytes_out: int
    total_packets: int
    total_connections: int
    total_anomalies: int
    peak_bandwidth: float
    average_bandwidth: float
    time_range_start: datetime
    time_range_end: datetime


# Alert Schemas
class AlertBase(BaseModel):
    """Base alert schema"""
    title: str = Field(..., max_length=255)
    message: str
    severity: SeverityLevel


class AlertCreate(AlertBase):
    """Schema for alert creation"""
    anomaly_id: Optional[int] = None
    device_id: Optional[int] = None


class AlertResponse(AlertBase):
    """Schema for alert response"""
    id: int
    is_acknowledged: bool
    acknowledged_by: Optional[int] = None
    acknowledged_at: Optional[datetime] = None
    anomaly_id: Optional[int] = None
    device_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AlertListResponse(BaseModel):
    """Schema for paginated alert list"""
    items: List[AlertResponse]
    total: int
    unacknowledged_count: int


# ML Prediction Schemas
class PredictionRequest(BaseModel):
    """Schema for ML prediction request"""
    features: Dict[str, Any]
    model_name: Optional[str] = "isolation_forest"


class PredictionResponse(BaseModel):
    """Schema for ML prediction response"""
    is_anomaly: bool
    anomaly_type: Optional[AnomalyType] = None
    confidence_score: float
    risk_score: float
    model_used: str
    processing_time_ms: float
    recommendations: Optional[List[str]] = None


class BatchPredictionRequest(BaseModel):
    """Schema for batch prediction request"""
    samples: List[Dict[str, Any]]
    model_name: Optional[str] = "isolation_forest"


class BatchPredictionResponse(BaseModel):
    """Schema for batch prediction response"""
    predictions: List[PredictionResponse]
    total_samples: int
    anomalies_detected: int
    processing_time_ms: float


# Dashboard Schemas
class DashboardStats(BaseModel):
    """Dashboard statistics schema"""
    total_devices: int
    online_devices: int
    offline_devices: int
    suspicious_devices: int
    total_anomalies: int
    unresolved_anomalies: int
    critical_alerts: int
    high_alerts: int
    medium_alerts: int
    low_alerts: int
    network_health_score: float


class TimeSeriesDataPoint(BaseModel):
    """Time series data point"""
    timestamp: datetime
    value: float


class NetworkTopologyNode(BaseModel):
    """Network topology node"""
    id: str
    label: str
    type: str
    status: DeviceStatus
    risk_score: float


class NetworkTopologyEdge(BaseModel):
    """Network topology edge"""
    source: str
    target: str
    weight: float


class NetworkTopology(BaseModel):
    """Network topology schema"""
    nodes: List[NetworkTopologyNode]
    edges: List[NetworkTopologyEdge]
