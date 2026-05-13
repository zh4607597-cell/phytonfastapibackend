from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.user import User
from app.schemas.user import UserSchema, UserCreate
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/", response_model=List[UserSchema])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/")
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    # In a real app, hash password here
    user = User(username=data.username, email=data.email, full_name=data.full_name, role=data.role, hashed_password=data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
