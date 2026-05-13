from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=False)
    subcategory = Column(String(100), nullable=True)
    quantity = Column(Integer, default=0)
    min_stock = Column(Integer, default=0)
    max_stock = Column(Integer, default=0)
    status = Column(String(50), default="active")  # active, inactive, discontinued
    inventory_type = Column(String(50), nullable=True)  # raw, finished, component
    location = Column(String(255), nullable=True)
    supplier = Column(String(255), nullable=True)
    unit_price = Column(Float, nullable=True)
    currency = Column(String(3), default="USD")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by =  Column(Integer, default=0, nullable=True)
