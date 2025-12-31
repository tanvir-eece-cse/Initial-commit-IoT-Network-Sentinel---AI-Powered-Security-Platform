"""
Device Management API Endpoints
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import uuid

from app.core.database import get_async_session
from app.core.security import get_current_user
from app.models.user import User
from app.models.network import Device, DeviceStatus
from app.schemas.network import (
    DeviceCreate,
    DeviceUpdate,
    DeviceResponse,
    DeviceListResponse,
)

router = APIRouter()


@router.get("/", response_model=DeviceListResponse)
async def list_devices(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[DeviceStatus] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """List all devices with pagination and filtering"""
    query = select(Device)
    count_query = select(func.count(Device.id))
    
    # Apply filters
    if status:
        query = query.where(Device.status == status)
        count_query = count_query.where(Device.status == status)
    
    if search:
        search_filter = f"%{search}%"
        query = query.where(
            (Device.name.ilike(search_filter)) |
            (Device.ip_address.ilike(search_filter)) |
            (Device.device_type.ilike(search_filter))
        )
        count_query = count_query.where(
            (Device.name.ilike(search_filter)) |
            (Device.ip_address.ilike(search_filter)) |
            (Device.device_type.ilike(search_filter))
        )
    
    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(Device.created_at.desc())
    
    result = await db.execute(query)
    devices = result.scalars().all()
    
    return DeviceListResponse(
        items=devices,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(
    device_in: DeviceCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new device"""
    # Check if device_id already exists
    result = await db.execute(
        select(Device).where(Device.device_id == device_in.device_id)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device with this ID already exists"
        )
    
    device = Device(**device_in.model_dump())
    db.add(device)
    await db.commit()
    await db.refresh(device)
    
    return device


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(
    device_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get device by ID"""
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    return device


@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(
    device_id: int,
    device_update: DeviceUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Update device"""
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    update_data = device_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(device, field, value)
    
    await db.commit()
    await db.refresh(device)
    
    return device


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Delete device"""
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    await db.delete(device)
    await db.commit()


@router.post("/{device_id}/trust", response_model=DeviceResponse)
async def toggle_device_trust(
    device_id: int,
    trusted: bool,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Toggle device trust status"""
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    device.is_trusted = trusted
    await db.commit()
    await db.refresh(device)
    
    return device


@router.get("/stats/summary")
async def get_device_stats(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get device statistics summary"""
    # Total devices
    total_result = await db.execute(select(func.count(Device.id)))
    total = total_result.scalar()
    
    # Online devices
    online_result = await db.execute(
        select(func.count(Device.id)).where(Device.status == DeviceStatus.ONLINE)
    )
    online = online_result.scalar()
    
    # Offline devices
    offline_result = await db.execute(
        select(func.count(Device.id)).where(Device.status == DeviceStatus.OFFLINE)
    )
    offline = offline_result.scalar()
    
    # Suspicious devices
    suspicious_result = await db.execute(
        select(func.count(Device.id)).where(Device.status == DeviceStatus.SUSPICIOUS)
    )
    suspicious = suspicious_result.scalar()
    
    # High risk devices
    high_risk_result = await db.execute(
        select(func.count(Device.id)).where(Device.risk_score > 0.7)
    )
    high_risk = high_risk_result.scalar()
    
    return {
        "total": total,
        "online": online,
        "offline": offline,
        "suspicious": suspicious,
        "high_risk": high_risk
    }
