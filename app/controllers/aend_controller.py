from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.aend_model import Aend
from app.schemas.aend_schemas import AendCreate, AendUpdate

def create_aend_controller(data: AendCreate, db: Session):
    new_aend = Aend(**data.dict())
    db.add(new_aend)
    db.commit()
    db.refresh(new_aend)
    return new_aend

def get_all_aends_controller(db: Session):
    return db.query(Aend).all()

def get_aend_by_id_controller(aend_id: int, db: Session):
    aend = db.query(Aend).filter(Aend.id == aend_id).first()
    if not aend:
        raise HTTPException(status_code=404, detail="Aend not found")
    return aend

def update_aend_controller(aend_id: int, data: AendUpdate, db: Session):
    aend = db.query(Aend).filter(Aend.id == aend_id).first()
    if not aend:
        raise HTTPException(status_code=404, detail="Aend not found")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(aend, key, value)
        
    db.commit()
    db.refresh(aend)
    return aend

def delete_aend_controller(aend_id: int, db: Session):
    aend = db.query(Aend).filter(Aend.id == aend_id).first()
    if not aend:
        raise HTTPException(status_code=404, detail="Aend not found")
    
    db.delete(aend)
    db.commit()
    return {"message": "Aend deleted successfully"}
