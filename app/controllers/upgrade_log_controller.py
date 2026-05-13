from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.upgrade_log_models import UpgradeLog
from app.schemas.upgrade_log_schemas import UpgradeLogCreate

def create_upgrade_log_controller(data: UpgradeLogCreate, db: Session):
    new_log = UpgradeLog(**data.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def get_upgrade_logs_controller(upgrade_id: int, db: Session):
    logs = db.query(UpgradeLog).filter(UpgradeLog.upgrade_id == upgrade_id).all()
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for this upgrade")
    return logs