from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    policy_id: Optional[int] = None
    cost_center_id: Optional[int] = None
    agent_id: Optional[int] = None

    customer_name: Optional[str] = None
    customer_type: Optional[str] = "Company"
    customer_group: Optional[str] = "Commercial"
    territory: Optional[str] = "Pakistan"
    salutation: Optional[str] = None
    gender: Optional[str] = None
    lead_name: Optional[str] = None
    opportunity_name: Optional[str] = None
    account_manager: Optional[str] = None
    image: Optional[str] = None
    default_price_list: Optional[str] = None
    default_bank_account: Optional[str] = None
    default_currency: Optional[str] = None
    is_internal_customer: Optional[int] = 0
    represents_company: Optional[str] = None
    market_segment: Optional[str] = None
    industry: Optional[str] = None
    customer_pos_id: Optional[str] = None
    website: Optional[str] = None
    language: Optional[str] = "en"
    customer_details: Optional[str] = None
    customer_primary_contact: Optional[str] = None
    mobile_no: Optional[str] = None
    email_id: Optional[str] = None
    customer_primary_address: Optional[str] = None
    primary_address: Optional[str] = None
    tax_id: Optional[str] = None
    tax_category: Optional[str] = None
    tax_withholding_category: Optional[str] = None
    payment_terms: Optional[str] = None
    loyalty_program: Optional[str] = None
    loyalty_program_tier: Optional[str] = None
    default_sales_partner: Optional[str] = None
    default_commission_rate: Optional[int] = 0
    so_required: Optional[int] = 0
    dn_required: Optional[int] = 0
    is_frozen: Optional[int] = 0
    disabled: Optional[int] = 0
    _user_tags: Optional[str] = None
    _comments: Optional[str] = None
    _assign: Optional[str] = None
    _liked_by: Optional[str] = None
    
    # Custom Fields
    custom_ntn_number: Optional[str] = None
    custom_technical_poc: Optional[str] = None
    custom_aend_address: Optional[str] = None
    custom_bend_address: Optional[str] = None
    custom_static_ip: Optional[str] = None
    custom_vlan_id: Optional[int] = 0
    custom_handover_point: Optional[str] = None
    custom_bandwidth_type: Optional[str] = None
    custom_aggregated_port_speed: Optional[str] = None
    customer_code: Optional[str] = None
    city: Optional[str] = None
    address_line_2: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = "Pakistan"
    erp_target_doctype: Optional[str] = "Customer"

class CustomerCreate(CustomerBase):
    customer_name: Optional[str] = None


class CustomerUpdate(CustomerBase):
    customer_name: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None

    class Config:
        from_attributes = True