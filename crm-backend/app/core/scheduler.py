from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.lead_product import LeadProduct
from app.models.invoice import Invoice, InvoiceItem
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_monthly_invoices():
    db = SessionLocal()
    try:
        # Find products with Monthly billing cycle
        monthly_products = db.query(LeadProduct).filter(LeadProduct.billing_cycle == "Monthly").all()
        
        # Group by lead
        leads_to_bill = {}
        for lp in monthly_products:
            if lp.lead_id not in leads_to_bill: leads_to_bill[lp.lead_id] = []
            leads_to_bill[lp.lead_id].append(lp)
            
        for lead_id, products in leads_to_bill.items():
            # Check if an invoice was already generated for this month
            # (Simple check: any invoice generated in the last 20 days)
            recent_inv = db.query(Invoice).filter(
                Invoice.lead_id == lead_id,
                Invoice.created_at >= datetime.now() - timedelta(days=20)
            ).first()
            
            if recent_inv: continue
            
            # Generate Invoice (similar to manual generation)
            count = db.query(Invoice).count() + 1
            inv_num = f"AUTO-{datetime.now().strftime('%Y%m')}-{count:04d}"
            
            invoice = Invoice(
                lead_id=lead_id,
                invoice_number=inv_num,
                status="Generated",
                due_date=datetime.now() + timedelta(days=15)
            )
            db.add(invoice)
            db.flush()
            
            subtotal = 0
            for lp in products:
                item_total = float(lp.unit_price) * lp.quantity
                item = InvoiceItem(
                    invoice_id=invoice.id,
                    product_id=lp.product_id,
                    description=f"Monthly Service: {lp.product.name if lp.product else 'Service'}",
                    quantity=lp.quantity,
                    unit_price=lp.unit_price,
                    total=item_total
                )
                db.add(item)
                subtotal += item_total
            
            invoice.subtotal = subtotal
            invoice.grand_total = subtotal
            logger.info(f"Auto-generated invoice {inv_num} for lead {lead_id}")
            
        db.commit()
    except Exception as e:
        logger.error(f"Error in auto-invoice scheduler: {e}")
        db.rollback()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Run every day at 1 AM
    scheduler.add_job(generate_monthly_invoices, 'cron', hour=1, minute=0)
    scheduler.start()
    logger.info("Background scheduler started for monthly invoices.")
