from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StockMovementBase(BaseModel):
    item_id: int
    type: str  # in, out, transfer, adjustment
    quantity: int
    reason: Optional[str] = None
    from_type: Optional[str] = None
    to_type: Optional[str] = None
    user: Optional[int] = 1


class StockMovementCreate(StockMovementBase):
    pass


class StockMovementUpdate(BaseModel):
    reason: Optional[str] = None
    from_type: Optional[str] = None
    to_type: Optional[str] = None


class StockMovementResponse(StockMovementBase):
    id: int
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True
