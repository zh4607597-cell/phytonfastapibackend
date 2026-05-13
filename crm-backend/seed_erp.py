import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from app.core.db import SessionLocal, engine, Base
from app.models.user import User
from app.models.lead import Lead
from app.models.product import Product
from app.models.lead_product import LeadProduct
from app.models.invoice import Invoice, InvoiceItem
from app.models.contract import Contract
from app.models.contract_template import ContractTemplate
from app.models.activity import Activity
from app.models.payment import Payment

def seed():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Check if we have leads. If not, create some.
        leads = db.query(Lead).all()
        if not leads:
            print("No leads found. Creating sample leads...")
            lead1 = Lead(
                lead_name="John Doe",
                company_name="Doe Industries",
                email="john@doe.com",
                phone="+923001234567",
                address="Office 101, Tech Park, Islamabad",
                status="Opportunity",
                source="Website"
            )
            lead2 = Lead(
                lead_name="Jane Smith",
                company_name="Smith Solutions",
                email="jane@smith.com",
                phone="+923007654321",
                address="Plot 52, Phase 6, DHA Lahore",
                status="Survey",
                source="Referral"
            )
            db.add_all([lead1, lead2])
            db.commit()
            db.refresh(lead1)
            db.refresh(lead2)
            leads = [lead1, lead2]
            print(f"Created {len(leads)} sample leads.")
        
        # 2. Create sample Products
        if db.query(Product).count() == 0:
            print("Creating sample products...")
            p1 = Product(name="100Mbps DIA", description="Dedicated Internet Access 1:1", sku="DIA-100", category="Internet", type="Service", unit_price=25000, recurring_price=25000, status="Active")
            p2 = Product(name="Managed Router", description="Cisco Managed Router", sku="HW-RTR-01", category="Hardware", type="Product", unit_price=15000, recurring_price=0, status="Active")
            p3 = Product(name="Firewall Subscription", description="Annual Security License", sku="SEC-FW-YR", category="Cloud", type="Service", unit_price=0, recurring_price=120000, status="Active")
            db.add_all([p1, p2, p3])
            db.commit()
            print("Products created.")

        # 3. Add products to the first lead
        lead = leads[0]
        if db.query(LeadProduct).filter(LeadProduct.lead_id == lead.id).count() == 0:
            print(f"Adding products to lead: {lead.lead_name}...")
            products = db.query(Product).all()
            lp1 = LeadProduct(lead_id=lead.id, product_id=products[0].id, quantity=1, unit_price=25000, billing_cycle="Monthly", tax=16, discount=5)
            lp2 = LeadProduct(lead_id=lead.id, product_id=products[1].id, quantity=1, unit_price=15000, billing_cycle="One-time", tax=16, discount=0)
            db.add_all([lp1, lp2])
            db.commit()
            print("Lead products added.")

        # 4. Create an Activity log
        activity = Activity(lead_id=lead.id, action="Lead Created", detail="Initial seed lead created")
        db.add(activity)
        db.commit()
        
        print("Seeding completed successfully!")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
