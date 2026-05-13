from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    chat_id: int
    sender_id: int
    receiver_id: Optional[int] = None
    sender_name: str
    message_text: str
    is_read: bool = False


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    receiver_id: Optional[int] = None
    message_text: Optional[str] = None
    is_read: Optional[bool] = None


class MessageResponse(MessageBase):
    id: int
    sent_at: Optional[datetime] = None

    @field_validator('sent_at', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if v is None:
            return None
        if isinstance(v, str) and v == '0000-00-00 00:00:00':
            return None
        return v

    class Config:
        from_attributes = True
