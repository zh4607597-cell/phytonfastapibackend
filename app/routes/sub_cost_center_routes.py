from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.schemas.sub_cost_center_schemas import SubCostCenterCreate, SubCostCenterOut
from app.controllers.sub_cost_center_controller import (
    create_sub_cost_center_controller,
    get_sub_cost_centers_controller,
    get_sub_cost_center_controller
)

router = APIRouter(prefix="/sub-cost-centers", tags=["Sub Cost Centers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SubCostCenterOut)
def route_create_sub_cost_center(data: SubCostCenterCreate, db: Session = Depends(get_db)):
    return create_sub_cost_center_controller(data, db)

@router.get("/", response_model=List[SubCostCenterOut])
def route_get_sub_cost_centers(db: Session = Depends(get_db)):
    return get_sub_cost_centers_controller(db)

@router.get("/{sub_cost_center_id}", response_model=SubCostCenterOut)
def route_get_sub_cost_center(sub_cost_center_id: int, db: Session = Depends(get_db)):
    return get_sub_cost_center_controller(sub_cost_center_id, db)