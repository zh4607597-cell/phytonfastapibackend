from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.lead_log_models import LeadLog
from app.schemas.lead_log_schema import LeadLogCreate, LeadLogUpdate

def create_lead_log_controller(data: LeadLogCreate, db: Session):
    new_log = LeadLog(**data.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def get_all_lead_logs_controller(db: Session):
    return db.query(LeadLog).all()

def get_lead_log_by_id_controller(log_id: int, db: Session):
    log = db.query(LeadLog).filter(LeadLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Lead log not found")
    return log

def update_lead_log_controller(log_id: int, data: LeadLogUpdate, db: Session):
    log = db.query(LeadLog).filter(LeadLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Lead log not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(log, key, value)
    db.commit()
    db.refresh(log)
    return log

def delete_lead_log_controller(log_id: int, db: Session):
    log = db.query(LeadLog).filter(LeadLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Lead log not found")
    db.delete(log)
    db.commit()
    return {"message": "Lead log deleted successfully"}