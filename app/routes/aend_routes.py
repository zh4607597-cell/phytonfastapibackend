from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.aend_schemas import AendCreate, AendUpdate, AendOut
from app.deps import get_db, PermissionChecker
from app.controllers.aend_controller import (
    create_aend_controller,
    get_all_aends_controller,
    get_aend_by_id_controller,
    update_aend_controller,
    delete_aend_controller,
)

router = APIRouter(prefix="/aend", tags=["Aends"])

@router.post("/", response_model=AendOut, dependencies=[Depends(PermissionChecker("lead_crm", "can_create"))])
def route_create_aend(data: AendCreate, db: Session = Depends(get_db)):
    return create_aend_controller(data, db)

@router.get("/", response_model=list[AendOut], dependencies=[Depends(PermissionChecker("lead_crm", "can_view"))])
def route_get_all_aends(db: Session = Depends(get_db)):
    return get_all_aends_controller(db)

@router.get("/{aend_id}", response_model=AendOut, dependencies=[Depends(PermissionChecker("lead_crm", "can_view"))])
def route_get_aend_by_id(aend_id: int, db: Session = Depends(get_db)):
    return get_aend_by_id_controller(aend_id, db)

@router.put("/{aend_id}", response_model=AendOut, dependencies=[Depends(PermissionChecker("lead_crm", "can_update"))])
def route_update_aend(aend_id: int, data: AendUpdate, db: Session = Depends(get_db)):
    return update_aend_controller(aend_id, data, db)

@router.delete("/{aend_id}", dependencies=[Depends(PermissionChecker("lead_crm", "can_delete"))])
def route_delete_aend(aend_id: int, db: Session = Depends(get_db)):
    return delete_aend_controller(aend_id, db)
