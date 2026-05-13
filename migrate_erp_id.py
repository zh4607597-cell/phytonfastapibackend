from app.database import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE customers ADD COLUMN erp_id VARCHAR(191) UNIQUE"))
            conn.commit()
            print("Successfully added erp_id column to customers table.")
        except Exception as e:
            if "already exists" in str(e).lower() or "duplicate column name" in str(e).lower():
                print("Column erp_id already exists.")
            else:
                print(f"Error migrating: {e}")

if __name__ == "__main__":
    migrate()
