from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    role: str = "agent"

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    class Config:
        from_attributes = True
