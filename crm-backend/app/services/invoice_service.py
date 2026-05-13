from sqlalchemy.orm import Session
from app.models.invoice import Invoice, InvoiceItem
from app.models.lead import Lead
from app.models.lead_product import LeadProduct
from app.models.activity import Activity
from datetime import datetime, timedelta

class InvoiceService:
    @staticmethod
    def generate_from_lead(db: Session, lead_id: int):
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead: return None, "Lead not found"
        
        lead_products = db.query(LeadProduct).filter(LeadProduct.lead_id == lead_id).all()
        if not lead_products: return None, "No products added to this lead"
        
        count = db.query(Invoice).count() + 1
        inv_num = f"INV-{datetime.now().strftime('%Y%m')}-{count:04d}"
        
        invoice = Invoice(
            lead_id=lead_id,
            invoice_number=inv_num,
            status="Generated",
            due_date=datetime.now() + timedelta(days=15),
            created_at=datetime.now()
        )
        db.add(invoice)
        db.flush()
        
        subtotal = 0
        tax_total = 0
        disc_total = 0
        
        for lp in lead_products:
            item_base = float(lp.unit_price) * lp.quantity
            item_disc = item_base * (float(lp.discount) / 100)
            item_tax = (item_base - item_disc) * (float(lp.tax) / 100)
            item_total = item_base - item_disc + item_tax
            
            item = InvoiceItem(
                invoice_id=invoice.id,
                product_id=lp.product_id,
                description=f"{lead.lead_name} - {lp.product.name if lp.product else 'Service'}",
                quantity=lp.quantity,
                unit_price=lp.unit_price,
                tax=lp.tax,
                discount=lp.discount,
                total=item_total
            )
            db.add(item)
            subtotal += item_base
            tax_total += item_tax
            disc_total += item_disc
            
        invoice.subtotal = subtotal
        invoice.tax_total = tax_total
        invoice.discount_total = disc_total
        invoice.grand_total = subtotal + tax_total - disc_total
        
        lead.invoice_status = "Generated"
        db.add(Activity(lead_id=lead_id, action="Invoice Generated", detail=f"Generated {inv_num}"))
        
        db.commit()
        return invoice, None
