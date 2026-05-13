from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.erp_models import LeadProduct
from app.services.erp_service import ERPService
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_recurring_invoices():
    logger.info("Starting monthly recurring invoice generation...")
    db = SessionLocal()
    try:
        # Find all leads with recurring products
        recurring_leads = db.query(LeadProduct.lead_id).filter(
            LeadProduct.billing_cycle == "Monthly"
        ).distinct().all()
        
        for (lead_id,) in recurring_leads:
            try:
                # Generate invoice for each lead
                invoice = ERPService.generate_invoice(db, lead_id, billing_type="Monthly")
                if invoice:
                    logger.info(f"Generated recurring invoice {invoice.invoice_number} for lead {lead_id}")
            except Exception as e:
                logger.error(f"Failed to generate recurring invoice for lead {lead_id}: {str(e)}")
        
        db.commit()
    except Exception as e:
        logger.error(f"Error in recurring invoice job: {str(e)}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Run on the 1st of every month at 00:00
    scheduler.add_job(generate_recurring_invoices, 'cron', day=1, hour=0, minute=0)
    scheduler.start()
    logger.info("ERP Scheduler started.")
