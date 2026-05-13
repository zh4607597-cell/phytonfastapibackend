from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.sub_cost_center_models import SubCostCenter
from app.schemas.sub_cost_center_schemas import SubCostCenterCreate

def create_sub_cost_center_controller(data: SubCostCenterCreate, db: Session):
    new_sub_cost_center = SubCostCenter(**data.dict())
    db.add(new_sub_cost_center)
    db.commit()
    db.refresh(new_sub_cost_center)
    return new_sub_cost_center

def get_sub_cost_centers_controller(db: Session):
    return db.query(SubCostCenter).all()

def get_sub_cost_center_controller(sub_cost_center_id: int, db: Session):
    sub_cost_center = db.query(SubCostCenter).filter(SubCostCenter.id == sub_cost_center_id).first()
    if not sub_cost_center:
        raise HTTPException(status_code=404, detail="Sub Cost Center not found")
    return sub_cost_center