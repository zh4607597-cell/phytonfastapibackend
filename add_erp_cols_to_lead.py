from app.database import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        print("Checking and adding columns to lead table...")
        # Get existing columns
        result = conn.execute(text("SHOW COLUMNS FROM `lead`"))
        existing_cols = [row[0] for row in result]
        
        new_cols = [
            ("contract_status", "VARCHAR(50) DEFAULT 'None'"),
            ("invoice_status", "VARCHAR(50) DEFAULT 'None'"),
            ("payment_status", "VARCHAR(50) DEFAULT 'None'"),
            ("notes", "TEXT")
        ]
        
        for col_name, col_type in new_cols:
            if col_name not in existing_cols:
                print(f"Adding column {col_name}...")
                conn.execute(text(f"ALTER TABLE `lead` ADD COLUMN {col_name} {col_type}"))
            else:
                print(f"Column {col_name} already exists.")
        
        conn.commit()
        print("Migration completed!")

if __name__ == "__main__":
    migrate()
