from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class LeadProduct(Base):
    __tablename__ = "lead_products"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(12, 2), nullable=False, default=0)
    billing_cycle = Column(String, default="One-time")  # One-time, Monthly, Yearly
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    tax = Column(Numeric(5, 2), default=0)       # percentage
    discount = Column(Numeric(5, 2), default=0)  # percentage
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    lead = relationship("Lead", back_populates="products")
    product = relationship("Product", back_populates="lead_products")

    @property
    def total(self):
        base = float(self.unit_price) * self.quantity
        discounted = base * (1 - float(self.discount) / 100)
        taxed = discounted * (1 + float(self.tax) / 100)
        return round(taxed, 2)
