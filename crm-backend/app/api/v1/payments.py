from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.payment import Payment
from app.models.invoice import Invoice
from app.models.lead import Lead
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import PaymentService
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/", response_model=List[PaymentResponse])
def list_payments(db: Session = Depends(get_db)):
    payments = db.query(Payment).order_by(Payment.created_at.desc()).all()
    for p in payments:
        inv = db.query(Invoice).filter(Invoice.id == p.invoice_id).first()
        if inv:
            p.invoice_number = inv.invoice_number
            lead = db.query(Lead).filter(Lead.id == inv.lead_id).first()
            p.lead_name = lead.lead_name if lead else "N/A"
    return payments

@router.post("/")
def record_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    payment, error = PaymentService.record_payment(db, data)
    if error: raise HTTPException(400, error)
    return {"message": "Payment recorded"}
