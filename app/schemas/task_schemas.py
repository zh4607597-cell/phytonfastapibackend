from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    assigned_to: int
    team_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = "pending"
    due_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    related_lead_id: Optional[int] = None
    related_customer_id: Optional[int] = None
    progress: Optional[float] = 0.0
    created_by: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    assigned_to: Optional[int] = None
    title: Optional[str] = None
    pass

class TaskOut(TaskBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True