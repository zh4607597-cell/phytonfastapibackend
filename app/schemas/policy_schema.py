from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    bandwidth: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    duration: Optional[str] = None
    policy_type: Optional[str] = None
    conditions: Optional[str] = None
    is_active: Optional[bool] = True


class PolicyCreate(PolicyBase):
    created_by: Optional[int] = None


class PolicyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    bandwidth: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    duration: Optional[str] = None
    policy_type: Optional[str] = None
    conditions: Optional[str] = None
    is_active: Optional[bool] = None


class PolicyOut(PolicyBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int]

    class Config:
        from_attributes = True