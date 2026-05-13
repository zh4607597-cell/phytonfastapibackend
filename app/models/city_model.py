from sqlalchemy import Column, Integer, String
from app.database import Base


class City(Base):
    __tablename__ = "cityies"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False, unique=True, index=True)
    city_code = Column(String(10), nullable=False, unique=True, index=True)  # e.g., RWP, ISB, KAR
