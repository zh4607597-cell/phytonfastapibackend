from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class InvoiceBase(BaseModel):
    customer_id: int
    lead_id: Optional[int] = None
    sub_invoice: Optional[int] = None
    invoice_number: str
    amount: float
    total_amount: Optional[float] = 0.0
    subtotal: Optional[float] = 0.0
    tax_amount: Optional[float] = 0.0
    discount_amount: Optional[float] = 0.0
    invoice_month: Optional[str] = None
    currency: Optional[str] = "PKR"
    status: Optional[str] = "Pending"
    billing_type: Optional[str] = "One-time"
    issue_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    notes: Optional[str] = ""


    

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(InvoiceBase):
    customer_id: Optional[int] = None
    invoice_number: Optional[str] = None
    amount: Optional[float] = None
    pass

class InvoiceGenerateRequest(BaseModel):
    customer_id: int
    lead_id: Optional[int] = None
    amount: Optional[float] = None
    invoice_number: Optional[str] = None
    currency: Optional[str] = "PKR"
    status: Optional[str] = "Pending"
    notes: Optional[str] = ""

class MonthlyInvoiceRequest(BaseModel):
    customer_id: int
    invoice_month: str  # e.g. "2026-04"

class InvoiceLeadSummary(BaseModel):
    lead_id: int
    policy_type: Optional[str] = None
    billing_period: Optional[str] = None
    lead_type: str
    upgrade_count: int
    days_to_first_upgrade: Optional[int] = None
    total_active_days: Optional[int] = None
    notes: Optional[str] = None

class InvoiceResponse(InvoiceBase):
    id: int
    issue_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class InvoiceGenerateResponse(BaseModel):
    invoice: InvoiceResponse
    total_leads: int
    total_upgrades: int
    leads: List[InvoiceLeadSummary]
    summary: str
    voice_text: str

    class Config:
        from_attributes = True

class ReportRequest(BaseModel):
    customer_id: Optional[int] = None
    lead_id: Optional[int] = None
    start_date: Optional[str] = "2026-04-01"
    end_date: Optional[str] = "2026-04-30"
