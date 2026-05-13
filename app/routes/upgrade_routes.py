from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.upgrade_schemas import UpgradeCreate, UpgradeUpdate, UpgradeOut
from app.controllers.upgrade_controller import (
    create_upgrade_controller,
    get_all_upgrades_controller,
    get_upgrade_by_id_controller,
    update_upgrade_controller,
    delete_upgrade_controller
)

router = APIRouter(prefix="/upgrade", tags=["Upgrades"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UpgradeOut)
def route_create_upgrade(data: UpgradeCreate, db: Session = Depends(get_db)):
    return create_upgrade_controller(data, db)

@router.get("/", response_model=list[UpgradeOut])
def route_get_all_upgrades(db: Session = Depends(get_db)):
    return get_all_upgrades_controller(db)

@router.get("/{upgrade_id}", response_model=UpgradeOut)
def route_get_upgrade_by_id(upgrade_id: int, db: Session = Depends(get_db)):
    return get_upgrade_by_id_controller(upgrade_id, db)

@router.put("/{upgrade_id}", response_model=UpgradeOut)
def route_update_upgrade(upgrade_id: int, data: UpgradeUpdate, db: Session = Depends(get_db)):
    return update_upgrade_controller(upgrade_id, data, db)

@router.delete("/{upgrade_id}")
def route_delete_upgrade(upgrade_id: int, db: Session = Depends(get_db)):
    return delete_upgrade_controller(upgrade_id, db)