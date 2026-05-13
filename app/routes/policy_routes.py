from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.policy_models import Policy
from app.schemas.policy_schema import PolicyCreate, PolicyUpdate, PolicyOut

router = APIRouter(prefix="/policy", tags=["Policies"])

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ▶ Create Policy
@router.post("/", response_model=PolicyOut)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    new_policy = Policy(**policy.dict())
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return new_policy


# ▶ Get All Policies
@router.get("/", response_model=list[PolicyOut])
def get_policies(db: Session = Depends(get_db)):
    return db.query(Policy).all()


# ▶ Get Policy By ID
@router.get("/{policy_id}", response_model=PolicyOut)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


# # ▶ Update Policy
# @router.put("/{policy_id}", response_model=PolicyOut)
# def update_policy(policy_id: int, update_data: PolicyUpdate, db: Session = Depends(get_db)):
#     policy = db.query(Policy).filter(Policy.id == policy_id).first()

#     if not policy:
#         raise HTTPException(status_code=404, detail="Policy not found")

#     for key, value in update_data.dict(exclude_unset=True).items():
#         setattr(policy, key, value)

#     db.commit()
#     db.refresh(policy)
#     return policy


# # ▶ Delete Policy
# @router.delete("/{policy_id}")
# def delete_policy(policy_id: int, db: Session = Depends(get_db)):
#     policy = db.query(Policy).filter(Policy.id == policy_id).first()

#     if not policy:
#         raise HTTPException(status_code=404, detail="Policy not found")

#     db.delete(policy)
#     db.commit()

#     return {"message": "Policy deleted successfully"}