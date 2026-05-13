from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class LeadLog(Base):
    __tablename__ = "lead_logs"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("lead.id"))
    timestamp = Column(DateTime, server_default=func.now())
    action = Column(String(255))
    user = Column(String(255))
    details = Column(Text)
    created_by = Column(Integer)