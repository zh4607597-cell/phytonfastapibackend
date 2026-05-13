from sqlalchemy import text
from app.database import engine

def run_migration():
    print("Starting migration to add deactivation_date to leads...")
    
    with engine.connect() as connection:
        try:
            connection.execute(text("ALTER TABLE leads ADD COLUMN deactivation_date DATETIME NULL"))
            connection.commit()
            print("Successfully added deactivation_date to leads table")
        except Exception as e:
            print(f"Skipped/Error: {e}")

if __name__ == "__main__":
    run_migration()
