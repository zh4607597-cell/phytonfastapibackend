from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserUpdate, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -----------------------------
# Utility functions
# -----------------------------
# Instead of hashing
def get_password_hash(password: str) -> str:
    return password  # store plain text directly

# Instead of verifying
def verify_password(plain_password: str, stored_password: str) -> bool:
    return plain_password == stored_password

# -----------------------------
# CRUD Operations
# -----------------------------

# Create user
def create_user(user: UserCreate, db: Session):
    db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    hashed_password = get_password_hash(user.password_hash)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        phone=user.phone,
        avatar_url=user.avatar_url
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get all users
def get_all_users(db: Session):
    return db.query(User).all()

# Get single user
def get_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user
def update_user(user_id: int, user: UserUpdate, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for field, value in user.dict(exclude_unset=True).items():
        if field == "password":
            setattr(db_user, "password_hash", get_password_hash(value))
        else:
            setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete user
def delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

# Login user
def login_user(data: UserLogin, db: Session):
    # Check if user exists by email
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    return user