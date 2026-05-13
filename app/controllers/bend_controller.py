from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.bend_model import Bend
from app.schemas.bend_schemas import BendCreate, BendUpdate

def create_bend_controller(data: BendCreate, db: Session):
    new_bend = Bend(**data.dict())
    db.add(new_bend)
    db.commit()
    db.refresh(new_bend)
    return new_bend

def get_all_bends_controller(db: Session):
    return db.query(Bend).all()

def get_bend_by_id_controller(bend_id: int, db: Session):
    bend = db.query(Bend).filter(Bend.id == bend_id).first()
    if not bend:
        raise HTTPException(status_code=404, detail="Bend not found")
    return bend

def update_bend_controller(bend_id: int, data: BendUpdate, db: Session):
    bend = db.query(Bend).filter(Bend.id == bend_id).first()
    if not bend:
        raise HTTPException(status_code=404, detail="Bend not found")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(bend, key, value)
        
    db.commit()
    db.refresh(bend)
    return bend

def delete_bend_controller(bend_id: int, db: Session):
    bend = db.query(Bend).filter(Bend.id == bend_id).first()
    if not bend:
        raise HTTPException(status_code=404, detail="Bend not found")
    
    db.delete(bend)
    db.commit()
    return {"message": "Bend deleted successfully"}
