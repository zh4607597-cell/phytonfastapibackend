from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UpgradeLogBase(BaseModel):
    upgrade_id: int
    action: str
    user: str
    details: Optional[str] = None

class UpgradeLogCreate(UpgradeLogBase):
    pass

class UpgradeLogOut(UpgradeLogBase):
    id: int
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True

