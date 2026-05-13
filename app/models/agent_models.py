from sqlalchemy import Column, Integer, String, DECIMAL, Boolean
from sqlalchemy.sql import func
from sqlalchemy import TIMESTAMP
from app.database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(255), nullable=False)
    agent_email = Column(String(255), unique=True, nullable=False)
    agent_phone = Column(String(50))
    sales_representative = Column(String(255))
    commission_rate = Column(DECIMAL(10, 2), default=0.00)
    total_sales = Column(DECIMAL(10, 2), default=0.00)
    total_commission = Column(DECIMAL(10, 2), default=0.00)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())