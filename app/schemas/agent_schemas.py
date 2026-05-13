from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AgentBase(BaseModel):
    agent_name: str
    agent_email: EmailStr
    agent_phone: Optional[str] = None
    sales_representative: Optional[str] = None
    commission_rate: Optional[float] = 0.0

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    agent_name: Optional[str] = None
    agent_email: Optional[EmailStr] = None
    agent_phone: Optional[str] = None
    sales_representative: Optional[str] = None
    commission_rate: Optional[float] = None
    is_active: Optional[bool] = None

class AgentOut(AgentBase):
    id: int
    is_active: bool
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True