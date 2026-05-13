from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Correct MySQL URL format
DATABASE_URL = "mysql+pymysql://root:@localhost/crmdb"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# Session Local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 