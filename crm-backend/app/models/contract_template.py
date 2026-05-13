from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.core.db import Base

class ContractTemplate(Base):
    __tablename__ = "contract_templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # path to .docx template
    placeholders = Column(Text, nullable=True)  # JSON string of placeholders
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
