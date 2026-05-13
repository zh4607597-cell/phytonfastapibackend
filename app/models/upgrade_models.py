from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class Upgrade(Base):
    __tablename__ = "upgrades"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    lead_id = Column(Integer, index=True)
    
    # Service properties below
    policy = Column(String(255))
    policy_type = Column(String(255))
    billing_period = Column(String(50))
    contract_type = Column(String(50))
    agent_name = Column(String(255))
    agent_id = Column(Integer)
    sales_representative = Column(String(255))
    
    cost_center_code = Column(String(100))
    cost_center_level1 = Column(String(150))
    cost_center_level2 = Column(String(150))
    cost_center_level3 = Column(String(150))
    
    department = Column(String(150))
    budget_allocation = Column(Integer)
    
    site_location = Column(String(255))
    a_end = Column(String(255))
    b_end = Column(String(255))
    
    service_type = Column(String(150))
    capacity = Column(String(100))
    status = Column(String(50))
    urgency = Column(String(50))
    expected_revenue = Column(Integer)
    
    available_capacity = Column(String(100))
    
    feasibility_notes = Column(Text)
    notes = Column(Text)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer)

    # Fixed date columns
    activation_date = Column(DateTime, nullable=True)
    deactivation_date = Column(DateTime, nullable=True)