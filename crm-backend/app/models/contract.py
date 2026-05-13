from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("contract_templates.id"), nullable=False)
    version = Column(Integer, default=1)
    status = Column(String, default="Draft")  # Draft, Signed, Cancelled
    generated_docx_path = Column(String, nullable=True)
    signed_doc_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lead = relationship("Lead", back_populates="contracts")
    template = relationship("ContractTemplate", back_populates="contracts")
