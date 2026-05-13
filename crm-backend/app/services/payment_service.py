from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.payment import Payment
from app.models.invoice import Invoice
from app.models.lead import Lead
from app.models.activity import Activity

class PaymentService:
    @staticmethod
    def record_payment(db: Session, data):
        inv = db.query(Invoice).filter(Invoice.id == data.invoice_id).first()
        if not inv: return None, "Invoice not found"
        
        payment = Payment(**data.dict())
        db.add(payment)
        
        # Total paid calculation
        total_paid_query = db.query(func.sum(Payment.amount)).filter(Payment.invoice_id == data.invoice_id).scalar() or 0
        
        if float(total_paid_query) + data.amount >= float(inv.grand_total):
            inv.status = "Paid"
            lead = db.query(Lead).filter(Lead.id == inv.lead_id).first()
            if lead: lead.payment_status = "Paid"
        
        db.add(Activity(lead_id=inv.lead_id, action="Payment Received", detail=f"PKR {data.amount} via {data.method}"))
        db.commit()
        return payment, None
