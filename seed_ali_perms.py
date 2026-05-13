from sqlalchemy import text
from app.database import engine

def seed_permissions():
    print("Seeding permissions for user Ali (ID: 1)...")
    with engine.connect() as connection:
        # Get feature ID for leads_crm
        feature = connection.execute(text("SELECT id FROM features WHERE feature_key = 'leads_crm'")).first()
        if not feature:
            # Create feature if missing
            print("Feature leads_crm not found, creating it...")
            connection.execute(text("INSERT INTO features (feature_name, feature_key, icon, path, is_active) VALUES ('Leads CRM', 'leads_crm', 'MdPersonAdd', '/leads/list', 1)"))
            feature = connection.execute(text("SELECT id FROM features WHERE feature_key = 'leads_crm'")).first()
            connection.commit()
            
        # Grant all permissions to user 1
        try:
            connection.execute(text(f"INSERT INTO user_permissions (user_id, feature_id, can_view, can_create, can_update, can_delete) VALUES (1, {feature.id}, 1, 1, 1, 1)"))
            connection.commit()
            print("Successfully granted all permissions to Ali for Leads CRM")
        except Exception as e:
            print(f"Skipped/Error: {e}")

if __name__ == "__main__":
    seed_permissions()
