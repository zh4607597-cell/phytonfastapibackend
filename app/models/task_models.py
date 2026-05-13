from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    assigned_to = Column(Integer, nullable=False)
    team_id = Column(Integer, nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    category = Column(String(100), nullable=True)
    priority = Column(String(50), nullable=True)
    status = Column(String(50), default="pending")
    due_date = Column(DateTime, nullable=True)
    start_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    related_lead_id = Column(Integer, nullable=True)
    related_customer_id = Column(Integer, nullable=True)
    progress = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, nullable=True)