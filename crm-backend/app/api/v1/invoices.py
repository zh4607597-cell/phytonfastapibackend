from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.invoice import Invoice
from app.models.lead import Lead
from app.schemas.invoice import InvoiceSchema, InvoiceStatusUpdate
from app.services.invoice_service import InvoiceService
from weasyprint import HTML
from jinja2 import Template
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/", response_model=List[InvoiceSchema])
def list_invoices(lead_id: int | None = None, status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Invoice)
    if lead_id: query = query.filter(Invoice.lead_id == lead_id)
    if status:
        if "," in status: query = query.filter(Invoice.status.in_(status.split(",")))
        else: query = query.filter(Invoice.status == status)
    
    invoices = query.order_by(Invoice.created_at.desc()).all()
    # Manual data enrichment for lead_name
    for inv in invoices:
        lead = db.query(Lead).filter(Lead.id == inv.lead_id).first()
        inv.lead_name = lead.lead_name if lead else "Unknown"
    return invoices

@router.post("/generate/{lead_id}")
def generate_invoice(lead_id: int, db: Session = Depends(get_db)):
    invoice, error = InvoiceService.generate_from_lead(db, lead_id)
    if error: raise HTTPException(400, error)
    return {"message": "Invoice generated", "invoice_number": invoice.invoice_number}

@router.patch("/{id}/status")
def update_invoice_status(id: int, data: InvoiceStatusUpdate, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter(Invoice.id == id).first()
    if not inv: raise HTTPException(404)
    inv.status = data.status
    db.commit()
    return {"message": "Status updated"}

@router.get("/{id}/pdf")
def get_invoice_pdf(id: int, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter(Invoice.id == id).first()
    if not inv: raise HTTPException(404)
    lead = db.query(Lead).filter(Lead.id == inv.lead_id).first()
    
    html_tmpl = """
    <html>
    <head><style>body { font-family: sans-serif; padding: 40px; color: #333; } .header { display: flex; justify-content: space-between; border-bottom: 2px solid #2563eb; padding-bottom: 20px; } .blue { color: #2563eb; } table { width: 100%; border-collapse: collapse; margin: 30px 0; } th { text-align: left; background: #f8fafc; padding: 10px; border-bottom: 1px solid #ddd; } td { padding: 10px; border-bottom: 1px solid #eee; } .totals { margin-left: auto; width: 300px; } .totals div { display: flex; justify-content: space-between; padding: 5px 0; } .grand { font-weight: bold; border-top: 1px solid #333; margin-top: 10px; padding-top: 10px; font-size: 1.2em; }</style></head>
    <body>
        <div class="header">
            <div><h1 class="blue">PACETEL ERP</h1><p>Invoice # {{inv_num}}</p></div>
            <div style="text-align: right;"><p>Date: {{date}}</p><p>Due Date: {{due_date}}</p></div>
        </div>
        <div style="margin: 30px 0;">
            <h3>Bill To:</h3>
            <p><strong>{{lead_name}}</strong><br>{{company}}<br>{{address}}</p>
        </div>
        <table>
            <thead><tr><th>Description</th><th>Qty</th><th>Price</th><th>Tax</th><th>Total</th></tr></thead>
            <tbody>
                {% for it in items %}
                <tr><td>{{it.description}}</td><td>{{it.quantity}}</td><td>{{it.unit_price}}</td><td>{{it.tax}}%</td><td>{{it.total}}</td></tr>
                {% endfor %}
            </tbody>
        </table>
        <div class="totals">
            <div><span>Subtotal</span><span>PKR {{subtotal}}</span></div>
            <div><span>Tax Total</span><span>PKR {{tax_total}}</span></div>
            <div><span>Discount</span><span>-PKR {{disc_total}}</span></div>
            <div class="grand"><span>Grand Total</span><span>PKR {{grand_total}}</span></div>
        </div>
    </body>
    </html>
    """
    t = Template(html_tmpl)
    html_content = t.render(
        inv_num=inv.invoice_number,
        date=inv.created_at.strftime('%Y-%m-%d'),
        due_date=inv.due_date.strftime('%Y-%m-%d') if inv.due_date else "N/A",
        lead_name=lead.lead_name if lead else "Customer",
        company=lead.company_name if lead else "",
        address=lead.address if lead else "",
        items=inv.items,
        subtotal=f"{float(inv.subtotal):,.2f}",
        tax_total=f"{float(inv.tax_total):,.2f}",
        disc_total=f"{float(inv.discount_total):,.2f}",
        grand_total=f"{float(inv.grand_total):,.2f}"
    )
    
    pdf = HTML(string=html_content).write_pdf()
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={inv.invoice_number}.pdf"})
