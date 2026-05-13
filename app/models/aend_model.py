from sqlalchemy import Column, Integer, String
from app.database import Base

class Aend(Base):
    __tablename__ = "aend"

    id = Column(Integer, primary_key=True, index=True)
    aend = Column(String(250))
