from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.policy_models import Policy
from app.schemas.policy_schema import PolicyCreate, PolicyUpdate


# ▶ Create Policy
def create_policy_controller(data: PolicyCreate, db: Session):

    new_policy = Policy(**data.dict())
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)

    return new_policy



# ▶ Get All Policies
def get_all_policies_controller(db: Session):
    return db.query(Policy).all()



# ▶ Get One Policy
def get_policy_by_id_controller(policy_id: int, db: Session):

    policy = db.query(Policy).filter(Policy.id == policy_id).first()

    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    return policy



# ▶ Update Policy
def update_policy_controller(policy_id: int, data: PolicyUpdate, db: Session):

    policy = db.query(Policy).filter(Policy.id == policy_id).first()

    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    # Update only provided fields
    for key, value in data.dict(exclude_unset=True).items():
        setattr(policy, key, value)

    db.commit()
    db.refresh(policy)

    return policy



# ▶ Delete Policy
def delete_policy_controller(policy_id: int, db: Session):

    policy = db.query(Policy).filter(Policy.id == policy_id).first()

    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    db.delete(policy)
    db.commit()

    return {"message": "Policy deleted successfully"}