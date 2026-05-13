from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class InventoryItemBase(BaseModel):
    name: str
    sku: str
    category: str
    subcategory: Optional[str] = None
    quantity: int = 0
    min_stock: int = 0
    max_stock: int = 0
    status: str = "active"
    inventory_type: Optional[str] = None
    location: Optional[str] = None
    supplier: Optional[str] = None
    unit_price: Optional[float] = None
    currency: str = "USD"
    created_by: Optional[int] = None


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    quantity: Optional[int] = None
    min_stock: Optional[int] = None
    max_stock: Optional[int] = None
    status: Optional[str] = None
    inventory_type: Optional[str] = None
    location: Optional[str] = None
    supplier: Optional[str] = None
    unit_price: Optional[float] = None
    currency: Optional[str] = None


class InventoryItemResponse(InventoryItemBase):
    id: int
    created_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True
