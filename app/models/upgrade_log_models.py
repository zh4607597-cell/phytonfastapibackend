from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class UpgradeLog(Base):
    __tablename__ = "upgrade_logs"

    id = Column(Integer, primary_key=True, index=True)
    upgrade_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    action = Column(String(255), nullable=False)
    user = Column(String(255), nullable=False)
    details = Column(Text)