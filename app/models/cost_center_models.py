from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base

class CostCenter(Base):
    __tablename__ = "cost_centers"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    level1 = Column(String(100))
    level2 = Column(String(100))
    level3 = Column(String(100))
    location = Column(String(100))
    department = Column(String(100))
    manager = Column(String(100))
    
    budget_allocated = Column(Float, default=0)
    budget_spent = Column(Float, default=0)
    budget_remaining = Column(Float, default=0)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer)