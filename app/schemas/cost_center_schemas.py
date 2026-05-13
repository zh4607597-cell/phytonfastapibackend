from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CostCenterBase(BaseModel):
    code: str
    level1: Optional[str] = None
    level2: Optional[str] = None
    level3: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    manager: Optional[str] = None

    budget_allocated: Optional[float] = 0
    budget_spent: Optional[float] = 0
    budget_remaining: Optional[float] = 0

    is_active: Optional[bool] = True


class CostCenterCreate(CostCenterBase):
    created_by: Optional[int] = None


class CostCenterUpdate(BaseModel):
    level1: Optional[str] = None
    level2: Optional[str] = None
    level3: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    manager: Optional[str] = None
    budget_allocated: Optional[float] = None
    budget_spent: Optional[float] = None
    budget_remaining: Optional[float] = None
    is_active: Optional[bool] = None


class CostCenterOut(CostCenterBase):
    id: int
    created_at:  Optional[datetime] = None
    updated_at:  Optional[datetime] = None
    created_by: Optional[int] = None

    class Config:
        from_attributes = True