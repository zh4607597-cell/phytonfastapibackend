from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.activity import Activity
from app.schemas.activity import ActivitySchema
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/", response_model=List[ActivitySchema])
def list_activities(lead_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Activity)
    if lead_id: query = query.filter(Activity.lead_id == lead_id)
    return query.order_by(Activity.created_at.desc()).all()
