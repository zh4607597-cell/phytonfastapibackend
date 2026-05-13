from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LeadLogBase(BaseModel):
    lead_id: int
    action: Optional[str] = None
    user: Optional[str] = None
    details: Optional[str] = None
    created_by: Optional[int] = None

class LeadLogCreate(LeadLogBase):
    pass

class LeadLogUpdate(BaseModel):
    action: Optional[str] = None
    user: Optional[str] = None
    details: Optional[str] = None

class LeadLogOut(LeadLogBase):
    id: int
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True