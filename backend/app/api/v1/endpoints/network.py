"""
Network Monitoring API Endpoints
"""
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_async_session
from app.core.security import get_current_user
from app.models.user import User
from app.models.network import Device, NetworkTraffic, DeviceStatus
from app.schemas.network import (
    TrafficStats,
    TrafficSummary,
    NetworkTopology,
    NetworkTopologyNode,
    NetworkTopologyEdge,
)

router = APIRouter()


@router.get("/traffic", response_model=List[TrafficStats])
async def get_traffic_stats(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    interval: str = Query("1h", regex="^(1m|5m|15m|1h|6h|1d)$"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get network traffic statistics"""
    if not start_time:
        start_time = datetime.utcnow() - timedelta(hours=24)
    if not end_time:
        end_time = datetime.utcnow()
    
    query = select(NetworkTraffic).where(
        NetworkTraffic.timestamp.between(start_time, end_time)
    ).order_by(NetworkTraffic.timestamp)
    
    result = await db.execute(query)
    traffic_data = result.scalars().all()
    
    return traffic_data


@router.get("/traffic/summary", response_model=TrafficSummary)
async def get_traffic_summary(
    hours: int = Query(24, ge=1, le=168),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get traffic summary for a time period"""
    start_time = datetime.utcnow() - timedelta(hours=hours)
    end_time = datetime.utcnow()
    
    # Aggregate traffic data
    result = await db.execute(
        select(
            func.sum(NetworkTraffic.bytes_in).label("total_bytes_in"),
            func.sum(NetworkTraffic.bytes_out).label("total_bytes_out"),
            func.sum(NetworkTraffic.packets_in + NetworkTraffic.packets_out).label("total_packets"),
            func.sum(NetworkTraffic.connections).label("total_connections"),
            func.sum(NetworkTraffic.anomalies_detected).label("total_anomalies"),
            func.max(NetworkTraffic.bytes_in + NetworkTraffic.bytes_out).label("peak_bandwidth"),
            func.avg(NetworkTraffic.bytes_in + NetworkTraffic.bytes_out).label("average_bandwidth"),
        ).where(NetworkTraffic.timestamp.between(start_time, end_time))
    )
    
    row = result.one()
    
    return TrafficSummary(
        total_bytes_in=row.total_bytes_in or 0,
        total_bytes_out=row.total_bytes_out or 0,
        total_packets=row.total_packets or 0,
        total_connections=row.total_connections or 0,
        total_anomalies=row.total_anomalies or 0,
        peak_bandwidth=float(row.peak_bandwidth or 0),
        average_bandwidth=float(row.average_bandwidth or 0),
        time_range_start=start_time,
        time_range_end=end_time
    )


@router.get("/topology", response_model=NetworkTopology)
async def get_network_topology(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get network topology map"""
    # Get all devices
    result = await db.execute(select(Device))
    devices = result.scalars().all()
    
    # Create nodes
    nodes = []
    for device in devices:
        nodes.append(NetworkTopologyNode(
            id=device.device_id,
            label=device.name,
            type=device.device_type or "unknown",
            status=device.status,
            risk_score=device.risk_score
        ))
    
    # Create edges (simplified - in production, this would come from actual network data)
    # For demo, connect devices to a central "router" node
    edges = []
    if nodes:
        # Add central router node
        nodes.append(NetworkTopologyNode(
            id="router_main",
            label="Main Router",
            type="router",
            status=DeviceStatus.ONLINE,
            risk_score=0.0
        ))
        
        for node in nodes[:-1]:  # Exclude router itself
            edges.append(NetworkTopologyEdge(
                source="router_main",
                target=node.id,
                weight=1.0
            ))
    
    return NetworkTopology(nodes=nodes, edges=edges)


@router.post("/scan")
async def initiate_network_scan(
    scan_type: str = Query("quick", regex="^(quick|full|deep)$"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Initiate a network scan"""
    # In production, this would trigger an actual network scan job
    scan_id = f"scan_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    return {
        "message": "Network scan initiated",
        "scan_id": scan_id,
        "scan_type": scan_type,
        "status": "running",
        "started_at": datetime.utcnow().isoformat()
    }


@router.get("/health-score")
async def get_network_health_score(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Calculate overall network health score"""
    # Get device statistics
    total_devices_result = await db.execute(select(func.count(Device.id)))
    total_devices = total_devices_result.scalar() or 1  # Avoid division by zero
    
    online_devices_result = await db.execute(
        select(func.count(Device.id)).where(Device.status == DeviceStatus.ONLINE)
    )
    online_devices = online_devices_result.scalar() or 0
    
    suspicious_devices_result = await db.execute(
        select(func.count(Device.id)).where(Device.status == DeviceStatus.SUSPICIOUS)
    )
    suspicious_devices = suspicious_devices_result.scalar() or 0
    
    # Get average risk score
    avg_risk_result = await db.execute(select(func.avg(Device.risk_score)))
    avg_risk = avg_risk_result.scalar() or 0
    
    # Calculate health score (0-100)
    # Factors: device availability, suspicious devices, average risk
    availability_score = (online_devices / total_devices) * 40
    security_score = max(0, 40 - (suspicious_devices / total_devices) * 100)
    risk_score = max(0, 20 - avg_risk * 20)
    
    health_score = availability_score + security_score + risk_score
    
    return {
        "health_score": round(health_score, 2),
        "components": {
            "availability": round(availability_score, 2),
            "security": round(security_score, 2),
            "risk": round(risk_score, 2)
        },
        "metrics": {
            "total_devices": total_devices,
            "online_devices": online_devices,
            "suspicious_devices": suspicious_devices,
            "average_risk_score": round(float(avg_risk), 4)
        }
    }


@router.get("/protocols")
async def get_protocol_distribution(
    hours: int = Query(24, ge=1, le=168),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get protocol distribution statistics"""
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    result = await db.execute(
        select(
            func.sum(NetworkTraffic.tcp_connections).label("tcp"),
            func.sum(NetworkTraffic.udp_connections).label("udp"),
            func.sum(NetworkTraffic.icmp_packets).label("icmp"),
        ).where(NetworkTraffic.timestamp >= start_time)
    )
    
    row = result.one()
    
    total = (row.tcp or 0) + (row.udp or 0) + (row.icmp or 0)
    
    if total == 0:
        return {
            "protocols": {
                "tcp": {"count": 0, "percentage": 0},
                "udp": {"count": 0, "percentage": 0},
                "icmp": {"count": 0, "percentage": 0}
            },
            "total": 0
        }
    
    return {
        "protocols": {
            "tcp": {
                "count": row.tcp or 0,
                "percentage": round(((row.tcp or 0) / total) * 100, 2)
            },
            "udp": {
                "count": row.udp or 0,
                "percentage": round(((row.udp or 0) / total) * 100, 2)
            },
            "icmp": {
                "count": row.icmp or 0,
                "percentage": round(((row.icmp or 0) / total) * 100, 2)
            }
        },
        "total": total
    }
