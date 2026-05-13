from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.invoice_schema import (
    InvoiceCreate, InvoiceResponse,
    InvoiceGenerateRequest, InvoiceGenerateResponse, MonthlyInvoiceRequest,
    ReportRequest
)
from app.controllers.invoice_controller import (
    create_invoice, create_invoice_for_lead, get_all_invoices, get_customer_invoices,
    update_invoice_status, update_invoice_controller, generate_invoice_for_customer,
    generate_complex_invoice, generate_monthly_invoice_controller, get_revenue_report
)

router = APIRouter(prefix="/invoice", tags=["Billing & Invoices"])

@router.post("/", response_model=InvoiceResponse)
def route_create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db)):
    return create_invoice(payload, db)

@router.post("/generate", response_model=InvoiceGenerateResponse)
def route_generate_invoice(payload: InvoiceGenerateRequest, db: Session = Depends(get_db)):
    return generate_invoice_for_customer(payload, db)

@router.post("/generate-complex/{customer_id}")
def route_generate_complex_invoice(customer_id: int, db: Session = Depends(get_db)):
    return generate_complex_invoice(customer_id, db)

@router.post("/generate-monthly", response_model=InvoiceResponse)
def route_generate_monthly_invoice(payload: MonthlyInvoiceRequest, db: Session = Depends(get_db)):
    return generate_monthly_invoice_controller(payload, db)

@router.get("/", response_model=list[InvoiceResponse])
def route_get_all_invoices(db: Session = Depends(get_db)):
    return get_all_invoices(db)

@router.get("/customer/{customer_id}", response_model=list[InvoiceResponse])
def route_get_customer_invoices(customer_id: int, db: Session = Depends(get_db)):
    return get_customer_invoices(customer_id, db)

@router.put("/{invoice_id}/status")
def route_update_invoice_status(invoice_id: int, status: str, db: Session = Depends(get_db)):
    return update_invoice_status(invoice_id, status, db)

from app.schemas.invoice_schema import InvoiceUpdate
@router.put("/{invoice_id}", response_model=InvoiceResponse)
def route_update_invoice(invoice_id: int, data: InvoiceUpdate, db: Session = Depends(get_db)):
    return update_invoice_controller(invoice_id, data, db)

@router.post("/lead/{lead_id}")
def route_create_invoice_for_lead(lead_id: int, db: Session = Depends(get_db)):
    return create_invoice_for_lead(lead_id, db)


@router.post("/revenue-report")
def create_revenue_report(req: ReportRequest, db: Session = Depends(get_db)):
    return get_revenue_report(req, db)