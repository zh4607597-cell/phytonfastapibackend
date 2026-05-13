from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    payment_date = Column(Date, default=datetime.utcnow)
    method = Column(String) # Bank Transfer, Cash, etc.
    reference = Column(String) # Cheque no, etc.
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    invoice = relationship("Invoice", backref="payments")
