from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    sku = Column(String, unique=True, nullable=True)
    category = Column(String)
    unit_price = Column(Numeric(12, 2), nullable=False, default=0)
    recurring_price = Column(Numeric(12, 2), nullable=True)
    status = Column(String, default="Active")
    type = Column(String, default="Service")  # Service or Product
    # Relationships
    lead_products = relationship("LeadProduct", back_populates="product", cascade="all, delete-orphan")
    invoice_items = relationship("InvoiceItem", back_populates="product", cascade="all, delete-orphan")
