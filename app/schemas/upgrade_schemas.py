from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class UpgradeBase(BaseModel):
    customer_id: Optional[int] = None
    lead_id: Optional[int] = None
    policy: Optional[str] = None
    policy_type: Optional[str] = None
    billing_period: Optional[str] = None
    contract_type: Optional[str] = None
    agent_name: Optional[str] = None
    agent_id: Optional[int] = None
    sales_representative: Optional[str] = None
    cost_center_code: Optional[str] = None
    cost_center_level1: Optional[str] = None
    cost_center_level2: Optional[str] = None
    cost_center_level3: Optional[str] = None
    department: Optional[str] = None
    budget_allocation: Optional[int] = None
    site_location: Optional[str] = None
    a_end: Optional[str] = None
    b_end: Optional[str] = None
    service_type: Optional[str] = None
    capacity: Optional[str] = None
    status: Optional[str] = None
    urgency: Optional[str] = None
    expected_revenue: Optional[int] = None
    available_capacity: Optional[str] = None
    
    # Unified date fields
    activation_date: Optional[datetime] = None
    deactivation_date: Optional[datetime] = None

    feasibility_notes: Optional[str] = None
    notes: Optional[str] = None
    created_by: Optional[int] = None

    @field_validator('activation_date', 'deactivation_date', mode='before')

    @classmethod
    def parse_datetime(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str) and (v == '0000-00-00 00:00:00' or v == '0000-00-00'):
            return None
        return v

class UpgradeCreate(UpgradeBase):
    pass

class UpgradeUpdate(UpgradeBase):
    pass

class UpgradeOut(UpgradeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def parse_audit_datetime(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str) and (v == '0000-00-00 00:00:00' or v == '0000-00-00'):
            return None
        return v

    class Config:
        from_attributes = True