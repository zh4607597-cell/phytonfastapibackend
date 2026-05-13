from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, nullable=False, index=True)
    type = Column(String(50), nullable=False)  # in, out, transfer, adjustment
    quantity = Column(Integer, nullable=False)
    reason = Column(Text, nullable=True)
    from_type = Column(String(100), nullable=True)  # supplier, warehouse, location
    to_type = Column(String(100), nullable=True)  # customer, warehouse, location
    user = Column(Integer, nullable=True, index=True)
    timestamp = Column(DateTime, server_default=func.now())
