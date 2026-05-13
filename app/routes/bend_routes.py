from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.bend_schemas import BendCreate, BendUpdate, BendOut
from app.deps import get_db, PermissionChecker
from app.controllers.bend_controller import (
    create_bend_controller,
    get_all_bends_controller,
    get_bend_by_id_controller,
    update_bend_controller,
    delete_bend_controller,
)

router = APIRouter(prefix="/bend", tags=["Bends"])

@router.post("/", response_model=BendOut, dependencies=[Depends(PermissionChecker("lead_crm", "can_create"))])
def route_create_bend(data: BendCreate, db: Session = Depends(get_db)):
    return create_bend_controller(data, db)

@router.get("/", response_model=list[BendOut], dependencies=[Depends(PermissionChecker("lead_crm", "can_view"))])
def route_get_all_bends(db: Session = Depends(get_db)):
    return get_all_bends_controller(db)

@router.get("/{bend_id}", response_model=BendOut, dependencies=[Depends(PermissionChecker("lead_crm", "can_view"))])
def route_get_bend_by_id(bend_id: int, db: Session = Depends(get_db)):
    return get_bend_by_id_controller(bend_id, db)

@router.put("/{bend_id}", response_model=BendOut, dependencies=[Depends(PermissionChecker("lead_crm", "can_update"))])
def route_update_bend(bend_id: int, data: BendUpdate, db: Session = Depends(get_db)):
    return update_bend_controller(bend_id, data, db)

@router.delete("/{bend_id}", dependencies=[Depends(PermissionChecker("lead_crm", "can_delete"))])
def route_delete_bend(bend_id: int, db: Session = Depends(get_db)):
    return delete_bend_controller(bend_id, db)
