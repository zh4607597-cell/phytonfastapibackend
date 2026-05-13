from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class TaskCommentBase(BaseModel):
    task_id: int
    user_id: int
    comment: str


class TaskCommentCreate(TaskCommentBase):
    pass


class TaskCommentUpdate(BaseModel):
    comment: Optional[str] = None


class TaskCommentResponse(TaskCommentBase):
    id: int
    created_at: Optional[datetime] = None

    @field_validator('created_at', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if v is None:
            return None
        if isinstance(v, str) and v == '0000-00-00 00:00:00':
            return None
        return v

    class Config:
        from_attributes = True
