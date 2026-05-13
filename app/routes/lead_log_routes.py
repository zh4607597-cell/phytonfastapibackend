from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.lead_log_schema import LeadLogCreate, LeadLogUpdate, LeadLogOut
from app.controllers.lead_log_controller import (
    create_lead_log_controller,
    get_all_lead_logs_controller,
    get_lead_log_by_id_controller,
    update_lead_log_controller,
    delete_lead_log_controller
)

router = APIRouter(prefix="/lead-log", tags=["Lead Logs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=LeadLogOut)
def route_create_lead_log(data: LeadLogCreate, db: Session = Depends(get_db)):
    return create_lead_log_controller(data, db)

@router.get("/", response_model=list[LeadLogOut])
def route_get_all_lead_logs(db: Session = Depends(get_db)):
    return get_all_lead_logs_controller(db)

@router.get("/{log_id}", response_model=LeadLogOut)
def route_get_lead_log_by_id(log_id: int, db: Session = Depends(get_db)):
    return get_lead_log_by_id_controller(log_id, db)

@router.put("/{log_id}", response_model=LeadLogOut)
def route_update_lead_log(log_id: int, data: LeadLogUpdate, db: Session = Depends(get_db)):
    return update_lead_log_controller(log_id, data, db)

@router.delete("/{log_id}")
def route_delete_lead_log(log_id: int, db: Session = Depends(get_db)):
    return delete_lead_log_controller(log_id, db)