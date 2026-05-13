from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user_model import User
from app.models.rbac_models import UserPermission, Feature
import os

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Security helper to get the current user
def get_current_user(x_user_id: str = Header(None), db: Session = Depends(get_db)):
    # DEV BYPASS: If no header is provided, we default to the first user (usually admin)
    # This allows testing via browser/Postman without manually adding headers every time.
    if x_user_id is None:
        user = db.query(User).first()
        if user:
            return user
        raise HTTPException(status_code=401, detail="X-User-ID header missing and no default user found")
    
    try:
        user_id_int = int(x_user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid X-User-ID format")

    user = db.query(User).filter(User.id == user_id_int, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user

class PermissionChecker:
    def __init__(self, feature_key: str, action: str):
        self.feature_key = feature_key
        self.action = action

    def __call__(self, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        # Admin bypass
        if user.role and str(user.role).lower() == "admin":
            return True
        
        feature = db.query(Feature).filter(Feature.feature_key == self.feature_key).first()
        if not feature:
            return True # Allow if feature doesn't exist yet for dev flexibility
            
        permission = db.query(UserPermission).filter(
            UserPermission.user_id == user.id,
            UserPermission.feature_id == feature.id
        ).first()

        if not permission:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        allowed = getattr(permission, self.action, False)
        if not allowed:
            raise HTTPException(status_code=403, detail=f"No {self.action} permission")
        
        return True