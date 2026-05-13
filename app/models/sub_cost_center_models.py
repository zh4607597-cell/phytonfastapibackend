from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class SubCostCenter(Base):
    __tablename__ = "sub_cost_centers"

    id = Column(Integer, primary_key=True, index=True)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    budget_allocated = Column(Float, default=0.0)
    budget_spent = Column(Float, default=0.0)
    monthly_revenue = Column(Float, default=0.0)
    monthly_cost = Column(Float, default=0.0)
    manager = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())