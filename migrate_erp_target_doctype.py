from app.database import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE customers ADD COLUMN erp_target_doctype VARCHAR(50) DEFAULT 'Customer' NULL"))
            conn.commit()
            print("Successfully added erp_target_doctype column to customers table.")
        except Exception as e:
            err_str = str(e).lower()
            if "already exists" in err_str or "duplicate column name" in err_str:
                print("Column erp_target_doctype already exists.")
            else:
                print(f"Error adding erp_target_doctype: {e}")

if __name__ == "__main__":
    migrate()
