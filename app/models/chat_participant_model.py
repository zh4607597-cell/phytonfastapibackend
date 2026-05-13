from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base


class ChatParticipant(Base):
    __tablename__ = "chat_participants"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    participant_name = Column(String(255), nullable=False)
    unread_count = Column(Integer, default=0)
    muted = Column(Boolean, default=False)
    joined_at = Column(DateTime, server_default=func.now())
    last_read_at = Column(DateTime, nullable=True)
