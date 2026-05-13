from pydantic import BaseModel
from datetime import date, datetime
from typing import List

class InvoiceItemSchema(BaseModel):
    description: str
    quantity: int
    unit_price: float
    tax: float = 0
    discount: float = 0
    total: float

class InvoiceSchema(BaseModel):
    id: int
    invoice_number: str
    lead_name: str | None = None
    created_at: datetime
    due_date: date | None = None
    grand_total: float
    status: str
    items: List[InvoiceItemSchema] = []
    subtotal: float
    tax_total: float
    discount_total: float

    class Config:
        from_attributes = True

class InvoiceStatusUpdate(BaseModel):
    status: str
