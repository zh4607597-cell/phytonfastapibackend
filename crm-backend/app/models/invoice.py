from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    invoice_number = Column(String, unique=True, nullable=False)
    status = Column(String, default="Draft")  # Draft, Generated, Sent, Paid, Overdue, Cancelled
    due_date = Column(Date, nullable=True)
    subtotal = Column(Numeric(12, 2), default=0)
    tax_total = Column(Numeric(12, 2), default=0)
    discount_total = Column(Numeric(12, 2), default=0)
    grand_total = Column(Numeric(12, 2), default=0)
    pdf_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lead = relationship("Lead", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    description = Column(String, nullable=True)
    quantity = Column(Integer, default=1)
    unit_price = Column(Numeric(12, 2), default=0)
    tax = Column(Numeric(5, 2), default=0)       # percentage
    discount = Column(Numeric(5, 2), default=0)  # percentage
    total = Column(Numeric(12, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product", back_populates="invoice_items")
