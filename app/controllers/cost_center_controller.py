from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.cost_center_models import CostCenter
from app.schemas.cost_center_schemas import CostCenterCreate, CostCenterUpdate


# ▶ Create Cost Center
def create_cost_center_controller(data: CostCenterCreate, db: Session):
    new_cc = CostCenter(**data.dict())
    db.add(new_cc)
    db.commit()
    db.refresh(new_cc)
    return new_cc


# ▶ Get All Cost Centers
def get_all_cost_centers_controller(db: Session):
    return db.query(CostCenter).all()


# ▶ Get Single Cost Center
def get_cost_center_by_id_controller(cost_center_id: int, db: Session):
    cc = db.query(CostCenter).filter(CostCenter.id == cost_center_id).first()
    if not cc:
        raise HTTPException(status_code=404, detail="Cost center not found")
    return cc


# ▶ Update Cost Center
def update_cost_center_controller(cost_center_id: int, data: CostCenterUpdate, db: Session):
    cc = db.query(CostCenter).filter(CostCenter.id == cost_center_id).first()
    if not cc:
        raise HTTPException(status_code=404, detail="Cost center not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(cc, key, value)

    db.commit()
    db.refresh(cc)
    return cc


# ▶ Delete Cost Center
def delete_cost_center_controller(cost_center_id: int, db: Session):
    cc = db.query(CostCenter).filter(CostCenter.id == cost_center_id).first()
    if not cc:
        raise HTTPException(status_code=404, detail="Cost center not found")

    db.delete(cc)
    db.commit()
    return {"message": "Cost center deleted successfully"}