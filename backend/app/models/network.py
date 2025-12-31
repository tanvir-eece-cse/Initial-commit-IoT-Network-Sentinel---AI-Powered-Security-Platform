"""
Network and Security Models
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import String, Boolean, DateTime, JSON, Integer, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.core.database import Base


class DeviceStatus(str, enum.Enum):
    """Device status enumeration"""
    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"
    SUSPICIOUS = "suspicious"


class AnomalyType(str, enum.Enum):
    """Anomaly type enumeration"""
    TRAFFIC_SPIKE = "traffic_spike"
    PORT_SCAN = "port_scan"
    DDOS_ATTACK = "ddos_attack"
    MALWARE = "malware"
    BOTNET = "botnet"
    DATA_EXFILTRATION = "data_exfiltration"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    PROTOCOL_ANOMALY = "protocol_anomaly"
    UNKNOWN = "unknown"


class SeverityLevel(str, enum.Enum):
    """Severity level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Device(Base):
    """IoT Device model"""
    
    __tablename__ = "devices"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    device_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    device_type: Mapped[str] = mapped_column(String(100), nullable=True)
    manufacturer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Network information
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    mac_address: Mapped[Optional[str]] = mapped_column(String(17), nullable=True)
    hostname: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Status
    status: Mapped[DeviceStatus] = mapped_column(
        Enum(DeviceStatus), default=DeviceStatus.UNKNOWN
    )
    last_seen: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Security
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    is_trusted: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # ML fingerprint
    fingerprint: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    
    # Relationships
    anomalies: Mapped[List["Anomaly"]] = relationship(
        "Anomaly", back_populates="device", lazy="dynamic"
    )


class Anomaly(Base):
    """Network Anomaly model"""
    
    __tablename__ = "anomalies"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    anomaly_type: Mapped[AnomalyType] = mapped_column(
        Enum(AnomalyType), default=AnomalyType.UNKNOWN
    )
    severity: Mapped[SeverityLevel] = mapped_column(
        Enum(SeverityLevel), default=SeverityLevel.LOW
    )
    
    # Details
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Source information
    source_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    destination_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    source_port: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    destination_port: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    protocol: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # ML prediction
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    ml_model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    raw_features: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Status
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    is_false_positive: Mapped[bool] = mapped_column(Boolean, default=False)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolved_by: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Device relationship
    device_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("devices.id"), nullable=True
    )
    device: Mapped[Optional["Device"]] = relationship(
        "Device", back_populates="anomalies"
    )
    
    # Timestamps
    detected_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )


class NetworkTraffic(Base):
    """Network Traffic Statistics model"""
    
    __tablename__ = "network_traffic"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Time bucket
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    
    # Traffic metrics
    bytes_in: Mapped[int] = mapped_column(Integer, default=0)
    bytes_out: Mapped[int] = mapped_column(Integer, default=0)
    packets_in: Mapped[int] = mapped_column(Integer, default=0)
    packets_out: Mapped[int] = mapped_column(Integer, default=0)
    connections: Mapped[int] = mapped_column(Integer, default=0)
    
    # Protocol breakdown
    tcp_connections: Mapped[int] = mapped_column(Integer, default=0)
    udp_connections: Mapped[int] = mapped_column(Integer, default=0)
    icmp_packets: Mapped[int] = mapped_column(Integer, default=0)
    
    # Security metrics
    blocked_connections: Mapped[int] = mapped_column(Integer, default=0)
    anomalies_detected: Mapped[int] = mapped_column(Integer, default=0)
    
    # Additional data
    metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)


class Alert(Base):
    """Security Alert model"""
    
    __tablename__ = "alerts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[SeverityLevel] = mapped_column(
        Enum(SeverityLevel), default=SeverityLevel.LOW
    )
    
    # Alert status
    is_acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)
    acknowledged_by: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Related entities
    anomaly_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("anomalies.id"), nullable=True
    )
    device_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("devices.id"), nullable=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
