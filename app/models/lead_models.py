from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, Numeric
from sqlalchemy.sql import func
from app.database import Base

class Lead(Base):
    __tablename__ = "lead"

    id = Column(Integer, primary_key=True, index=True)
    creation = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now(), onupdate=func.now())
    modified_by = Column(String(100))
    owner = Column(String(100))

    docstatus = Column(Integer, default=0)
    doctype = Column(String(50), default="Lead")
    idx = Column(Integer, default=0)

    lead_name = Column(String(100))
    lead_owner = Column(String(100))
    status = Column(String(50))
    source = Column(String(100))
    lead_type = Column(String(50))
    request_type = Column(String(100))

    salutation = Column(String(50))
    first_name = Column(String(100))
    middle_name = Column(String(100))
    last_name = Column(String(100))

    customer_name = Column(String(255))
    company_name = Column(String(255))
    customer_type = Column(String(50), default="Company")
    customer_group = Column(String(100), default="Commercial")

    job_title = Column(String(100))
    gender = Column(String(20))

    phone = Column(String(50))
    mobile_no = Column(String(50))
    phone_ext = Column(String(20))
    whatsapp = Column(String(50))
    email_id = Column(String(150))
    website = Column(String(255))

    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))

    territory = Column(String(100))
    language = Column(String(20), default="en")

    no_of_employees = Column(String(50))
    annual_revenue = Column(Numeric(15, 2), default=0.0)
    industry = Column(String(100))
    market_segment = Column(String(100))

    qualification_status = Column(String(50))
    qualified_by = Column(String(100))
    qualified_on = Column(DateTime)

    campaign_name = Column(String(100))
    company = Column(String(100))

    unsubscribed = Column(Boolean, default=False)
    blog_subscriber = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)

    image = Column(Text)

    # ERP Specific & Custom Fields
    opportunity_name = Column(String(100))
    account_manager = Column(String(100))
    default_price_list = Column(String(100))
    default_bank_account = Column(String(100))
    default_currency = Column(String(20), default="PKR")
    is_internal_customer = Column(Integer, default=0)
    represents_company = Column(String(100))
    customer_pos_id = Column(String(100))
    customer_details = Column(Text)
    customer_primary_contact = Column(String(100))
    customer_primary_address = Column(Text)
    primary_address = Column(Text)
    tax_id = Column(String(100))
    tax_category = Column(String(100))
    tax_withholding_category = Column(String(100))
    payment_terms = Column(String(100))
    loyalty_program = Column(String(100))
    loyalty_program_tier = Column(String(100))
    default_sales_partner = Column(String(100))
    default_commission_rate = Column(Float, default=0.0)
    so_required = Column(Integer, default=0)
    dn_required = Column(Integer, default=0)
    is_frozen = Column(Integer, default=0)
    
    # Custom Technical Fields
    custom_ntn_number = Column(String(100))
    custom_technical_poc = Column(String(100))
    custom_aend_address = Column(Text)
    custom_bend_address = Column(Text)
    custom_static_ip = Column(String(100))
    custom_vlan_id = Column(Integer, default=0)
    custom_handover_point = Column(String(255))
    custom_bandwidth_type = Column(String(100))
    custom_aggregated_port_speed = Column(String(100))
    noc_active = Column(Integer, default=0)
    custom_noc_active = Column(Integer, default=0)

    # New ERP Fields
    contract_status = Column(String(50), default="None")
    invoice_status = Column(String(50), default="None")
    payment_status = Column(String(50), default="None")
    notes = Column(Text)