from pydantic import BaseModel
from typing import Optional

class AendBase(BaseModel):
    aend: Optional[str] = None

class AendCreate(AendBase):
    aend: str

class AendUpdate(AendBase):
    pass

class AendOut(AendBase):
    id: int

    class Config:
        from_attributes = True
