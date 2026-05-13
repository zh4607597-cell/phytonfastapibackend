from sqlalchemy import Column, Integer, String
from app.database import Base

class Bend(Base):
    __tablename__ = "bend"

    id = Column(Integer, primary_key=True, index=True)
    bend = Column(String(250))
