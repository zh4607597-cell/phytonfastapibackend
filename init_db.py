from app.database import engine, Base
# Import all models to ensure they are registered with Base
from app.models.user_model import User
from app.models.customer_model import Customer
from app.models.agent_models import Agent
from app.models.policy_models import Policy
from app.models.cost_center_models import CostCenter
from app.models.lead_models import Lead
from app.models.lead_log_models import LeadLog
from app.models.upgrade_models import Upgrade
from app.models.upgrade_log_models import UpgradeLog
from app.models.sub_cost_center_models import SubCostCenter
from app.models.task_models import Task
from app.models.task_comment_model import TaskComment
from app.models.teams_models import Team
from app.models.inventory_model import InventoryItem
from app.models.stock_movement_model import StockMovement
from app.models.chat_model import Chat
from app.models.chat_participant_model import ChatParticipant
from app.models.message_model import Message
from app.models.city_model import City
from app.models.rbac_models import Role, Feature, Permission, UserPermission

def init_db():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

if __name__ == "__main__":
    init_db()
