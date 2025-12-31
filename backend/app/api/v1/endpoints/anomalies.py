"""
Anomaly Detection API Endpoints
"""
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.core.database import get_async_session
from app.core.security import get_current_user
from app.models.user import User
from app.models.network import Anomaly, AnomalyType, SeverityLevel
from app.schemas.network import (
    AnomalyCreate,
    AnomalyUpdate,
    AnomalyResponse,
    AnomalyListResponse,
)

router = APIRouter()


@router.get("/", response_model=AnomalyListResponse)
async def list_anomalies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    anomaly_type: Optional[AnomalyType] = None,
    severity: Optional[SeverityLevel] = None,
    is_resolved: Optional[bool] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """List all anomalies with pagination and filtering"""
    query = select(Anomaly)
    count_query = select(func.count(Anomaly.id))
    
    # Apply filters
    if anomaly_type:
        query = query.where(Anomaly.anomaly_type == anomaly_type)
        count_query = count_query.where(Anomaly.anomaly_type == anomaly_type)
    
    if severity:
        query = query.where(Anomaly.severity == severity)
        count_query = count_query.where(Anomaly.severity == severity)
    
    if is_resolved is not None:
        query = query.where(Anomaly.is_resolved == is_resolved)
        count_query = count_query.where(Anomaly.is_resolved == is_resolved)
    
    if start_date:
        query = query.where(Anomaly.detected_at >= start_date)
        count_query = count_query.where(Anomaly.detected_at >= start_date)
    
    if end_date:
        query = query.where(Anomaly.detected_at <= end_date)
        count_query = count_query.where(Anomaly.detected_at <= end_date)
    
    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(Anomaly.detected_at.desc())
    
    result = await db.execute(query)
    anomalies = result.scalars().all()
    
    return AnomalyListResponse(
        items=anomalies,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("/", response_model=AnomalyResponse, status_code=status.HTTP_201_CREATED)
async def create_anomaly(
    anomaly_in: AnomalyCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new anomaly record"""
    anomaly = Anomaly(**anomaly_in.model_dump())
    db.add(anomaly)
    await db.commit()
    await db.refresh(anomaly)
    
    return anomaly


@router.get("/{anomaly_id}", response_model=AnomalyResponse)
async def get_anomaly(
    anomaly_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get anomaly by ID"""
    result = await db.execute(select(Anomaly).where(Anomaly.id == anomaly_id))
    anomaly = result.scalar_one_or_none()
    
    if not anomaly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anomaly not found"
        )
    
    return anomaly


@router.put("/{anomaly_id}", response_model=AnomalyResponse)
async def update_anomaly(
    anomaly_id: int,
    anomaly_update: AnomalyUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Update anomaly status"""
    result = await db.execute(select(Anomaly).where(Anomaly.id == anomaly_id))
    anomaly = result.scalar_one_or_none()
    
    if not anomaly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anomaly not found"
        )
    
    update_data = anomaly_update.model_dump(exclude_unset=True)
    
    # Set resolved metadata
    if update_data.get("is_resolved"):
        update_data["resolved_by"] = current_user.id
        update_data["resolved_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(anomaly, field, value)
    
    await db.commit()
    await db.refresh(anomaly)
    
    return anomaly


@router.post("/{anomaly_id}/resolve", response_model=AnomalyResponse)
async def resolve_anomaly(
    anomaly_id: int,
    notes: Optional[str] = None,
    is_false_positive: bool = False,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Mark anomaly as resolved"""
    result = await db.execute(select(Anomaly).where(Anomaly.id == anomaly_id))
    anomaly = result.scalar_one_or_none()
    
    if not anomaly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anomaly not found"
        )
    
    anomaly.is_resolved = True
    anomaly.is_false_positive = is_false_positive
    anomaly.resolution_notes = notes
    anomaly.resolved_by = current_user.id
    anomaly.resolved_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(anomaly)
    
    return anomaly


@router.delete("/{anomaly_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_anomaly(
    anomaly_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Delete anomaly"""
    result = await db.execute(select(Anomaly).where(Anomaly.id == anomaly_id))
    anomaly = result.scalar_one_or_none()
    
    if not anomaly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anomaly not found"
        )
    
    await db.delete(anomaly)
    await db.commit()


@router.get("/stats/summary")
async def get_anomaly_stats(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get anomaly statistics summary"""
    # Total anomalies
    total_result = await db.execute(select(func.count(Anomaly.id)))
    total = total_result.scalar()
    
    # Unresolved anomalies
    unresolved_result = await db.execute(
        select(func.count(Anomaly.id)).where(Anomaly.is_resolved == False)
    )
    unresolved = unresolved_result.scalar()
    
    # By severity
    critical_result = await db.execute(
        select(func.count(Anomaly.id)).where(
            and_(Anomaly.severity == SeverityLevel.CRITICAL, Anomaly.is_resolved == False)
        )
    )
    critical = critical_result.scalar()
    
    high_result = await db.execute(
        select(func.count(Anomaly.id)).where(
            and_(Anomaly.severity == SeverityLevel.HIGH, Anomaly.is_resolved == False)
        )
    )
    high = high_result.scalar()
    
    # Last 24 hours
    last_24h = datetime.utcnow() - timedelta(hours=24)
    recent_result = await db.execute(
        select(func.count(Anomaly.id)).where(Anomaly.detected_at >= last_24h)
    )
    recent = recent_result.scalar()
    
    # By type
    type_stats = {}
    for anomaly_type in AnomalyType:
        type_result = await db.execute(
            select(func.count(Anomaly.id)).where(Anomaly.anomaly_type == anomaly_type)
        )
        type_stats[anomaly_type.value] = type_result.scalar()
    
    return {
        "total": total,
        "unresolved": unresolved,
        "critical": critical,
        "high": high,
        "last_24h": recent,
        "by_type": type_stats
    }
