from pydantic import BaseModel
from datetime import date, datetime

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    sku: str | None = None
    category: str | None = None
    unit_price: float = 0
    recurring_price: float | None = 0
    status: str = "Active"
    type: str = "Service"

class ProductCreate(ProductBase):
    pass

class ProductSchema(ProductBase):
    id: int
    class Config:
        from_attributes = True
