from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    sku = Column(String(100), unique=True, index=True)
    category = Column(String(100))
    unit_price = Column(Numeric(15, 2), default=0.0)
    recurring_price = Column(Numeric(15, 2), default=0.0)
    status = Column(String(50), default="Active") # Active, Inactive
    type = Column(String(50), default="Product") # Service, Product
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class LeadProduct(Base):
    __tablename__ = "lead_products"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("lead.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    
    product_name = Column(String(255))
    description = Column(Text)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, default=0.0)
    billing_cycle = Column(String(50), default="One-time") # One-time, Monthly, Quarterly, Yearly
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    tax = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    product = relationship("Product")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    
    item_name = Column(String(255))
    description = Column(Text)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    
    created_at = Column(DateTime, server_default=func.now())

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    amount = Column(Float, default=0.0)
    payment_date = Column(DateTime, server_default=func.now())
    payment_method = Column(String(50)) # Cash, Bank Transfer, Credit Card
    transaction_id = Column(String(100))
    status = Column(String(50), default="Completed") # Completed, Pending, Failed
    notes = Column(Text)
    
    created_at = Column(DateTime, server_default=func.now())

class ContractTemplate(Base):
    __tablename__ = "contract_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    file_path = Column(String(512)) # Path to DOCX template
    content = Column(Text) # Optional text content
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, server_default=func.now())

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("lead.id"))
    template_id = Column(Integer, ForeignKey("contract_templates.id"))
    
    contract_number = Column(String(100), unique=True)
    file_path = Column(String(512)) # Path to generated DOCX/PDF
    signed_file_path = Column(String(512)) # Path to uploaded signed contract
    status = Column(String(50), default="Draft") # Draft, Sent, Signed, Cancelled
    version = Column(Integer, default=1)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("lead.id"), nullable=True)
    performed_by = Column(String(100), nullable=True) # Name of user who performed action
    action = Column(String(255))
    entity_type = Column(String(50)) # Lead, Invoice, Contract, Product
    entity_id = Column(Integer)
    details = Column(Text)
    
    created_at = Column(DateTime, server_default=func.now())

class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50)) # Lead, Invoice, Contract
    entity_id = Column(Integer)
    file_name = Column(String(255))
    file_path = Column(String(512))
    file_type = Column(String(100))
    file_size = Column(Integer)
    
    created_at = Column(DateTime, server_default=func.now())
