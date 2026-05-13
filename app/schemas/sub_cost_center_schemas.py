from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubCostCenterBase(BaseModel):
    cost_center_id: int
    code: str
    name: str
    description: Optional[str] = None
    budget_allocated: Optional[float] = 0.0
    budget_spent: Optional[float] = 0.0
    monthly_revenue: Optional[float] = 0.0
    monthly_cost: Optional[float] = 0.0
    manager: Optional[str] = None

class SubCostCenterCreate(SubCostCenterBase):
    pass

class SubCostCenterOut(SubCostCenterBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True