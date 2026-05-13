from app.database import engine, Base
from app.models.user_model import User
from app.models.customer_model import Customer
from app.models.agent_models import Agent
from app.models.policy_models import Policy
from app.models.cost_center_models import CostCenter
from app.models.lead_models import Lead
from app.models.invoice_model import Invoice

print("Creating tables in CRM Database...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully including 'invoices'!")
