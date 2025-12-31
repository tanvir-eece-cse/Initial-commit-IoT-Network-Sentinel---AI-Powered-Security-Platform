"""
Dashboard API Endpoints
Aggregated statistics and visualizations
"""
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.core.database import get_async_session
from app.core.security import get_current_user
from app.models.user import User
from app.models.network import Device, Anomaly, Alert, NetworkTraffic, DeviceStatus, SeverityLevel
from app.schemas.network import DashboardStats, TimeSeriesDataPoint

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard statistics"""
    # Device counts
    total_devices_result = await db.execute(select(func.count(Device.id)))
    total_devices = total_devices_result.scalar() or 0
    
    online_devices_result = await db.execute(
        select(func.count(Device.id)).where(Device.status == DeviceStatus.ONLINE)
    )
    online_devices = online_devices_result.scalar() or 0
    
    offline_devices_result = await db.execute(
        select(func.count(Device.id)).where(Device.status == DeviceStatus.OFFLINE)
    )
    offline_devices = offline_devices_result.scalar() or 0
    
    suspicious_devices_result = await db.execute(
        select(func.count(Device.id)).where(Device.status == DeviceStatus.SUSPICIOUS)
    )
    suspicious_devices = suspicious_devices_result.scalar() or 0
    
    # Anomaly counts
    total_anomalies_result = await db.execute(select(func.count(Anomaly.id)))
    total_anomalies = total_anomalies_result.scalar() or 0
    
    unresolved_anomalies_result = await db.execute(
        select(func.count(Anomaly.id)).where(Anomaly.is_resolved == False)
    )
    unresolved_anomalies = unresolved_anomalies_result.scalar() or 0
    
    # Alert counts by severity
    critical_alerts_result = await db.execute(
        select(func.count(Alert.id)).where(
            and_(Alert.severity == SeverityLevel.CRITICAL, Alert.is_acknowledged == False)
        )
    )
    critical_alerts = critical_alerts_result.scalar() or 0
    
    high_alerts_result = await db.execute(
        select(func.count(Alert.id)).where(
            and_(Alert.severity == SeverityLevel.HIGH, Alert.is_acknowledged == False)
        )
    )
    high_alerts = high_alerts_result.scalar() or 0
    
    medium_alerts_result = await db.execute(
        select(func.count(Alert.id)).where(
            and_(Alert.severity == SeverityLevel.MEDIUM, Alert.is_acknowledged == False)
        )
    )
    medium_alerts = medium_alerts_result.scalar() or 0
    
    low_alerts_result = await db.execute(
        select(func.count(Alert.id)).where(
            and_(Alert.severity == SeverityLevel.LOW, Alert.is_acknowledged == False)
        )
    )
    low_alerts = low_alerts_result.scalar() or 0
    
    # Calculate network health score
    if total_devices > 0:
        availability = online_devices / total_devices
        security = 1 - (suspicious_devices / total_devices)
        health_score = (availability * 0.4 + security * 0.4 + 0.2) * 100
    else:
        health_score = 100.0
    
    return DashboardStats(
        total_devices=total_devices,
        online_devices=online_devices,
        offline_devices=offline_devices,
        suspicious_devices=suspicious_devices,
        total_anomalies=total_anomalies,
        unresolved_anomalies=unresolved_anomalies,
        critical_alerts=critical_alerts,
        high_alerts=high_alerts,
        medium_alerts=medium_alerts,
        low_alerts=low_alerts,
        network_health_score=round(health_score, 2)
    )


@router.get("/traffic/timeline", response_model=List[TimeSeriesDataPoint])
async def get_traffic_timeline(
    hours: int = Query(24, ge=1, le=168),
    metric: str = Query("bytes", regex="^(bytes|packets|connections)$"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get traffic timeline data for charts"""
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    query = select(NetworkTraffic).where(
        NetworkTraffic.timestamp >= start_time
    ).order_by(NetworkTraffic.timestamp)
    
    result = await db.execute(query)
    traffic_data = result.scalars().all()
    
    timeline = []
    for record in traffic_data:
        if metric == "bytes":
            value = record.bytes_in + record.bytes_out
        elif metric == "packets":
            value = record.packets_in + record.packets_out
        else:  # connections
            value = record.connections
        
        timeline.append(TimeSeriesDataPoint(
            timestamp=record.timestamp,
            value=float(value)
        ))
    
    return timeline


@router.get("/anomalies/timeline", response_model=List[TimeSeriesDataPoint])
async def get_anomalies_timeline(
    hours: int = Query(24, ge=1, le=168),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get anomalies timeline data for charts"""
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    # Group anomalies by hour
    query = select(
        func.date_trunc('hour', Anomaly.detected_at).label('hour'),
        func.count(Anomaly.id).label('count')
    ).where(
        Anomaly.detected_at >= start_time
    ).group_by(
        func.date_trunc('hour', Anomaly.detected_at)
    ).order_by('hour')
    
    result = await db.execute(query)
    data = result.all()
    
    timeline = []
    for row in data:
        timeline.append(TimeSeriesDataPoint(
            timestamp=row.hour,
            value=float(row.count)
        ))
    
    return timeline


@router.get("/recent-anomalies")
async def get_recent_anomalies(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get recent anomalies for dashboard"""
    query = select(Anomaly).order_by(
        Anomaly.detected_at.desc()
    ).limit(limit)
    
    result = await db.execute(query)
    anomalies = result.scalars().all()
    
    return anomalies


@router.get("/recent-alerts")
async def get_recent_alerts(
    limit: int = Query(10, ge=1, le=50),
    unacknowledged_only: bool = False,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get recent alerts for dashboard"""
    query = select(Alert)
    
    if unacknowledged_only:
        query = query.where(Alert.is_acknowledged == False)
    
    query = query.order_by(Alert.created_at.desc()).limit(limit)
    
    result = await db.execute(query)
    alerts = result.scalars().all()
    
    return alerts


@router.get("/risk-distribution")
async def get_risk_distribution(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get device risk score distribution"""
    # Define risk buckets
    buckets = [
        ("low", 0, 0.3),
        ("medium", 0.3, 0.6),
        ("high", 0.6, 0.8),
        ("critical", 0.8, 1.0)
    ]
    
    distribution = {}
    for name, low, high in buckets:
        result = await db.execute(
            select(func.count(Device.id)).where(
                and_(Device.risk_score >= low, Device.risk_score < high)
            )
        )
        distribution[name] = result.scalar() or 0
    
    return distribution


@router.get("/top-threats")
async def get_top_threats(
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get top threat sources"""
    query = select(
        Anomaly.source_ip,
        func.count(Anomaly.id).label('count')
    ).where(
        Anomaly.source_ip.isnot(None)
    ).group_by(
        Anomaly.source_ip
    ).order_by(
        func.count(Anomaly.id).desc()
    ).limit(limit)
    
    result = await db.execute(query)
    threats = []
    
    for row in result.all():
        threats.append({
            "source_ip": row.source_ip,
            "anomaly_count": row.count
        })
    
    return threats
