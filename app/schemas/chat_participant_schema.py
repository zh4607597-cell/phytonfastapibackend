from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class ChatParticipantBase(BaseModel):
    chat_id: int
    user_id: int
    participant_name: str
    unread_count: int = 0
    muted: bool = False
    last_read_at: Optional[datetime] = None


class ChatParticipantCreate(ChatParticipantBase):
    pass


class ChatParticipantUpdate(BaseModel):
    participant_name: Optional[str] = None
    unread_count: Optional[int] = None
    muted: Optional[bool] = None
    last_read_at: Optional[datetime] = None


class ChatParticipantResponse(ChatParticipantBase):
    id: int
    joined_at: Optional[datetime] = None

    @field_validator('joined_at', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if v is None:
            return None
        if isinstance(v, str) and v == '0000-00-00 00:00:00':
            return None
        return v

    class Config:
        from_attributes = True
