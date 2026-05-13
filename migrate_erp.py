from app.database import engine, Base
from app.models.user_model import User
from app.models.customer_model import Customer
from app.models.lead_models import Lead
from app.models.invoice_model import Invoice
from app.models.erp_models import Product, LeadProduct, InvoiceItem, Payment, ContractTemplate, Contract, Activity, Attachment

print("Upgrading database with ERP tables...")
Base.metadata.create_all(bind=engine)
print("ERP Tables created successfully!")
