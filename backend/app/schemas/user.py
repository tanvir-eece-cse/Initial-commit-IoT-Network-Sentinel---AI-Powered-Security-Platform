"""
Pydantic Schemas for User operations
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user creation"""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema for user update"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    is_superuser: bool
    is_verified: bool
    role: str
    permissions: Optional[List[str]] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    mfa_enabled: bool
    
    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    """Schema for user in database"""
    hashed_password: str


class Token(BaseModel):
    """Token schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload schema"""
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class PasswordChange(BaseModel):
    """Password change schema"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)


class PasswordReset(BaseModel):
    """Password reset schema"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class PasswordResetRequest(BaseModel):
    """Password reset request schema"""
    email: EmailStr
