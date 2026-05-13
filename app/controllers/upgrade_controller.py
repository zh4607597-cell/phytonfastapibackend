from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.upgrade_models import Upgrade
from app.schemas.upgrade_schemas import UpgradeCreate, UpgradeUpdate
import logging

logger = logging.getLogger("uvicorn.error")

def create_upgrade_controller(data: UpgradeCreate, db: Session):
    try:
        new_upgrade = Upgrade(**data.dict())
        db.add(new_upgrade)
        db.commit()
        db.refresh(new_upgrade)
        return new_upgrade
    except Exception as e:
        logger.error(f"Error creating upgrade: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_all_upgrades_controller(db: Session):
    return db.query(Upgrade).all()

def get_upgrade_by_id_controller(upgrade_id: int, db: Session):
    upgrade = db.query(Upgrade).filter(Upgrade.id == upgrade_id).first()
    if not upgrade:
        raise HTTPException(status_code=404, detail="Upgrade not found")
    return upgrade

def update_upgrade_controller(upgrade_id: int, data: UpgradeUpdate, db: Session):
    try:
        upgrade = db.query(Upgrade).filter(Upgrade.id == upgrade_id).first()
        if not upgrade:
            raise HTTPException(status_code=404, detail="Upgrade not found")
        
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(upgrade, key, value)
            
        db.commit()
        db.refresh(upgrade)
        return upgrade
    except Exception as e:
        logger.error(f"Error updating upgrade {upgrade_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_upgrade_controller(upgrade_id: int, db: Session):
    try:
        upgrade = db.query(Upgrade).filter(Upgrade.id == upgrade_id).first()
        if not upgrade:
            raise HTTPException(status_code=404, detail="Upgrade not found")
        db.delete(upgrade)
        db.commit()
        return {"message": "Upgrade deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting upgrade {upgrade_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))