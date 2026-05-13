from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers.user_controller import (
    create_user, get_all_users, get_user, update_user, delete_user, login_user
)
from app.database import get_db
from app.schemas.user_schemas import UserCreate, UserUpdate, UserLogin, UserOut
from fastapi import Request

router = APIRouter(prefix="/users", tags=["Users"])

# -----------------------------
# Routes
# -----------------------------

# Create user
@router.post("/", response_model=UserOut)
def route_create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

# Get all users
@router.get("/", response_model=list[UserOut])
def route_get_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)

# # Get user by id
# @router.get("/{user_id}", response_model=UserOut)
# def route_get_user(user_id: int, db: Session = Depends(get_db)):
#     return get_user(user_id, db)

# # Update user
# @router.put("/{user_id}", response_model=UserOut)
# def route_update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
#     return update_user(user_id, user, db)

# # Delete user
# @router.delete("/{user_id}")
# def route_delete_user(user_id: int, db: Session = Depends(get_db)):
#     return delete_user(user_id, db)

# Login user
@router.post("/login", response_model=UserOut)
def route_login_user(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)