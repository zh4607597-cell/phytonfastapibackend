from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.upgrade_log_schemas import UpgradeLogCreate, UpgradeLogOut
from app.controllers.upgrade_log_controller import (
    create_upgrade_log_controller,
    get_upgrade_logs_controller
)

router = APIRouter(prefix="/upgrade-logs", tags=["Upgrade Logs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UpgradeLogOut)
def route_create_upgrade_log(data: UpgradeLogCreate, db: Session = Depends(get_db)):
    return create_upgrade_log_controller(data, db)

@router.get("/{upgrade_id}", response_model=list[UpgradeLogOut])
def route_get_upgrade_logs(upgrade_id: int, db: Session = Depends(get_db)):
    return get_upgrade_logs_controller(upgrade_id, db)