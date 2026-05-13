from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base
from datetime import datetime

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    lead_name = Column(String, nullable=False)
    company_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    status = Column(String, default="New")
    source = Column(String)
    assigned_user_id = Column(Integer, ForeignKey("users.id"))
    notes = Column(Text)
    contract_status = Column(String, default="Draft")
    invoice_status = Column(String, default="None")
    payment_status = Column(String, default="Unpaid")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    # Relationships
    assigned_user = relationship("User", backref="leads")
    products = relationship("LeadProduct", back_populates="lead", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="lead", cascade="all, delete-orphan")
    contracts = relationship("Contract", back_populates="lead", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="lead", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="lead", cascade="all, delete-orphan")
