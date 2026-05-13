
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Adjust path to import models
sys.path.append(os.getcwd())
from app.models.lead_models import Lead
from app.database import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def check_lead(id_str):
    print(f"Checking lead: {id_str}")
    # Try by ID
    try:
        lid = int(id_str)
        lead = db.query(Lead).filter(Lead.id == lid).first()
    except:
        lead = None
        
    if not lead:
        # Try by name
        lead = db.query(Lead).filter(Lead.lead_name == id_str).first()
        
    if lead:
        print(f"FOUND LEAD: id={lead.id}, name={lead.lead_name}, status={lead.status}")
    else:
        print("LEAD NOT FOUND")

if __name__ == "__main__":
    # Check some recent leads
    leads = db.query(Lead).order_by(Lead.id.desc()).limit(10).all()
    print("Recent Leads in DB:")
    for l in leads:
        print(f"ID: {l.id} | Name: {l.lead_name} | Status: {l.status} | ERP ID: {l.represents_company}")
