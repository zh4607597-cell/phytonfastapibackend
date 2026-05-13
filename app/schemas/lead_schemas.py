from pydantic import BaseModel, field_validator
from typing import Optional, Union
from datetime import datetime
from decimal import Decimal

class LeadBase(BaseModel):
    id: Optional[Union[int, str]] = None
    creation: Optional[datetime] = None
    modified: Optional[datetime] = None
    modified_by: Optional[str] = None
    owner: Optional[str] = None

    docstatus: Optional[int] = 0
    doctype: Optional[str] = "Lead"
    idx: Optional[int] = 0

    lead_name: Optional[str] = None
    lead_owner: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    lead_type: Optional[str] = None
    request_type: Optional[str] = None

    salutation: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None

    customer_name: Optional[str] = None
    company_name: Optional[str] = None
    customer_type: Optional[str] = "Company"
    customer_group: Optional[str] = "Commercial"

    job_title: Optional[str] = None
    gender: Optional[str] = None

    phone: Optional[str] = None
    mobile_no: Optional[str] = None
    phone_ext: Optional[str] = None
    whatsapp: Optional[str] = None
    email_id: Optional[str] = None
    website: Optional[str] = None

    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

    territory: Optional[str] = None
    language: Optional[str] = "en"

    no_of_employees: Optional[str] = None
    annual_revenue: Optional[Decimal] = Decimal("0.00")
    industry: Optional[str] = None
    market_segment: Optional[str] = None

    qualification_status: Optional[str] = None
    qualified_by: Optional[str] = None
    qualified_on: Optional[datetime] = None

    campaign_name: Optional[str] = None
    company: Optional[str] = None

    unsubscribed: Optional[bool] = False
    blog_subscriber: Optional[bool] = False
    disabled: Optional[bool] = False

    image: Optional[str] = None

    # ERP Specific & Custom Fields
    opportunity_name: Optional[str] = None
    account_manager: Optional[str] = None
    default_price_list: Optional[str] = None
    default_bank_account: Optional[str] = None
    default_currency: Optional[str] = "PKR"
    is_internal_customer: Optional[int] = 0
    represents_company: Optional[str] = None
    customer_pos_id: Optional[str] = None
    customer_details: Optional[str] = None
    customer_primary_contact: Optional[str] = None
    customer_primary_address: Optional[str] = None
    primary_address: Optional[str] = None
    tax_id: Optional[str] = None
    tax_category: Optional[str] = None
    tax_withholding_category: Optional[str] = None
    payment_terms: Optional[str] = None
    loyalty_program: Optional[str] = None
    loyalty_program_tier: Optional[str] = None
    default_sales_partner: Optional[str] = None
    default_commission_rate: Optional[float] = 0.0
    so_required: Optional[int] = 0
    dn_required: Optional[int] = 0
    is_frozen: Optional[int] = 0
    
    # Custom Technical Fields
    custom_ntn_number: Optional[str] = None
    custom_technical_poc: Optional[str] = None
    custom_aend_address: Optional[str] = None
    custom_bend_address: Optional[str] = None
    custom_static_ip: Optional[str] = None
    custom_vlan_id: Optional[int] = 0
    custom_handover_point: Optional[str] = None
    custom_bandwidth_type: Optional[str] = None
    custom_aggregated_port_speed: Optional[str] = None
    noc_active: Optional[int] = 0
    custom_noc_active: Optional[int] = 0
    contract_status: Optional[str] = "None"
    invoice_status: Optional[str] = "None"
    payment_status: Optional[str] = "None"
    notes: Optional[str] = None


    @field_validator('creation', 'modified', 'qualified_on', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str) and (v == '0000-00-00 00:00:00' or v == '0000-00-00'):
            return None
        return v

class LeadCreate(LeadBase):
    products: Optional[list[dict]] = None
    contract_template_id: Optional[int] = None

class LeadUpdate(LeadBase):
    pass

class LeadOut(LeadBase):
    class Config:
        from_attributes = True

class LeadApproval(BaseModel):
    action: str
    comments: Optional[str] = None
    user_id: Optional[int] = None
    user_name: Optional[str] = None

class LeadStatusUpdate(BaseModel):
    status: str