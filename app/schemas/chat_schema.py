from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class ChatBase(BaseModel):
    name: str
    type: str  # direct, group, channel
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None


class ChatCreate(ChatBase):
    receiver_id: Optional[int] = None


class ChatUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None


class ChatResponse(ChatBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if v is None:
            return None
        if isinstance(v, str) and v == '0000-00-00 00:00:00':
            return None
        return v

    class Config:
        from_attributes = True
