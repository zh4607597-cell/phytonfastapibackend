from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

# -----------------------------
# Base schema for shared fields
# -----------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = "user"
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = True
    password_hash: Optional[str] = None
   

# -----------------------------
# Schema for creating a user
# -----------------------------
class UserCreate(UserBase):
    password_hash: str  # Plain password to be hashed


# -----------------------------
# Schema for updating a user
# -----------------------------
class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[str]
    phone: Optional[str]
    avatar_url: Optional[str]
    is_active: Optional[bool]
    password_hash: Optional[str]  # Optional, if updating password


# -----------------------------
# Schema for user login
# -----------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
# -----------------------------
# Schema for response (output)
# -----------------------------
class UserOut(UserBase):
    id: int
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('created_at', 'updated_at', 'last_login', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if v is None:
            return None
        if isinstance(v, str) and v == '0000-00-00 00:00:00':
            return None
        return v

    class Config:
        from_attributes = True  # Allows SQLAlchemy model to be returned directly