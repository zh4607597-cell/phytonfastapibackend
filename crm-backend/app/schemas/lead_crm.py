from pydantic import BaseModel
from datetime import date
from typing import List

class LeadProductSchema(BaseModel):
    product_id: int | None = None
    quantity: int = 1
    unit_price: float = 0
    billing_cycle: str = "One-time"
    start_date: date | None = None
    end_date: date | None = None
    tax: float = 0
    discount: float = 0

class LeadProductResponse(LeadProductSchema):
    id: int
    total: float
    product_name: str | None = None
    product_description: str | None = None

    class Config:
        from_attributes = True
