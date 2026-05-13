from pydantic import BaseModel
from datetime import date

class PaymentCreate(BaseModel):
    invoice_id: int
    amount: float
    payment_date: date
    method: str
    reference: str | None = None
    notes: str | None = None

class PaymentResponse(PaymentCreate):
    id: int
    invoice_number: str | None = None
    lead_name: str | None = None
    
    class Config:
        from_attributes = True
