from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    lead_id = Column(Integer, index=True, nullable=True)
    sub_invoice = Column(Integer, index=True, nullable=True)
    
    invoice_number = Column(String(50), unique=True, index=True)
    amount = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    invoice_month = Column(String(20), nullable=True)
    
    currency = Column(String(10), default="PKR")
    
    status = Column(String(50), default="Pending") # Pending, Generated, Paid, Overdue
    
    # Billing cycle logic
    issue_date = Column(DateTime, server_default=func.now())
    start_date = Column(DateTime) # After 2 days grace period
    due_date = Column(DateTime)   # 30 days after start_date
    
    subtotal = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    billing_type = Column(String(50)) # One-time, Monthly, etc.
    
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

