from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.cost_center_schemas import CostCenterCreate, CostCenterUpdate, CostCenterOut
from app.controllers.cost_center_controller import (
    create_cost_center_controller,
    get_all_cost_centers_controller,
    get_cost_center_by_id_controller,
    update_cost_center_controller,
    delete_cost_center_controller
)

router = APIRouter(prefix="/cost-center", tags=["Cost Centers"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CostCenterOut)
def route_create_cost_center(data: CostCenterCreate, db: Session = Depends(get_db)):
    return create_cost_center_controller(data, db)


@router.get("/", response_model=list[CostCenterOut])
def route_get_all_cost_centers(db: Session = Depends(get_db)):
    return get_all_cost_centers_controller(db)


@router.get("/{cost_center_id}", response_model=CostCenterOut)
def route_get_cost_center(cost_center_id: int, db: Session = Depends(get_db)):
    return get_cost_center_by_id_controller(cost_center_id, db)


@router.put("/{cost_center_id}", response_model=CostCenterOut)
def route_update_cost_center(cost_center_id: int, data: CostCenterUpdate, db: Session = Depends(get_db)):
    return update_cost_center_controller(cost_center_id, data, db)


@router.delete("/{cost_center_id}")
def route_delete_cost_center(cost_center_id: int, db: Session = Depends(get_db)):
    return delete_cost_center_controller(cost_center_id, db)