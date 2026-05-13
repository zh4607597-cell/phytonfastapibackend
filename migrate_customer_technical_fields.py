from app.database import engine
from sqlalchemy import text

def migrate():
    columns = [
        ("site_location", "VARCHAR(255)"),
        ("a_end", "VARCHAR(255)"),
        ("b_end", "VARCHAR(255)"),
        ("service_type", "VARCHAR(100)"),
        ("capacity", "VARCHAR(100)"),
        ("bandwidth", "VARCHAR(100)"),
        ("ip_addresses", "TEXT"),
        ("vlan", "VARCHAR(100)"),
        ("erp_sync_detail", "TEXT")
    ]
    
    with engine.connect() as conn:
        for col_name, col_type in columns:
            try:
                # Using MySQL/MariaDB syntax for ALTER TABLE
                conn.execute(text(f"ALTER TABLE customers ADD COLUMN {col_name} {col_type} NULL"))
                conn.commit()
                print(f"Successfully added {col_name} column to customers table.")
            except Exception as e:
                err_str = str(e).lower()
                if "already exists" in err_str or "duplicate column name" in err_str:
                    print(f"Column {col_name} already exists.")
                else:
                    print(f"Error adding {col_name}: {e}")

if __name__ == "__main__":
    migrate()
