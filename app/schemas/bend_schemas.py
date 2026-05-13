from pydantic import BaseModel
from typing import Optional

class BendBase(BaseModel):
    bend: Optional[str] = None

class BendCreate(BendBase):
    bend: str

class BendUpdate(BendBase):
    pass

class BendOut(BendBase):
    id: int

    class Config:
        from_attributes = True
