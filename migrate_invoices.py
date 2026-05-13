import sys
import os

from sqlalchemy import create_engine, text
from app.database import DATABASE_URL

def migrate():
    print(f"Connecting to {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    
    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN lead_id INTEGER DEFAULT NULL;"))
            print("Added lead_id successfully.")
        except Exception as e:
            print(f"lead_id error: {e}")
            
        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN sub_invoice INTEGER DEFAULT NULL;"))
            print("Added sub_invoice successfully.")
        except Exception as e:
            print(f"sub_invoice error: {e}")

        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN amount FLOAT DEFAULT 0.0;"))
            print("Added amount successfully.")
        except Exception as e:
            print(f"amount error: {e}")
            
        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN total_amount FLOAT DEFAULT 0.0;"))
            print("Added total_amount successfully.")
        except Exception as e:
            print(f"total_amount error: {e}")
            
        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN invoice_month VARCHAR(20) DEFAULT NULL;"))
            print("Added invoice_month successfully.")
        except Exception as e:
            print(f"invoice_month error: {e}")
            
        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN issue_date DATETIME DEFAULT NULL;"))
            print("Added issue_date successfully.")
        except Exception as e:
            print(f"issue_date error: {e}")
            
        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN start_date DATETIME DEFAULT NULL;"))
            print("Added start_date successfully.")
        except Exception as e:
            print(f"start_date error: {e}")
            
        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN due_date DATETIME DEFAULT NULL;"))
            print("Added due_date successfully.")
        except Exception as e:
            print(f"due_date error: {e}")

        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN notes VARCHAR(500) DEFAULT NULL;"))
            print("Added notes successfully.")
        except Exception as e:
            print(f"notes error: {e}")
            
        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN currency VARCHAR(10) DEFAULT 'PKR';"))
            print("Added currency successfully.")
        except Exception as e:
            print(f"currency error: {e}")
            
        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN invoice_number VARCHAR(50);"))
            print("Added invoice_number successfully.")
        except Exception as e:
            print(f"invoice_number error: {e}")

        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;"))
            print("Added updated_at successfully.")
        except Exception as e:
            print(f"updated_at error: {e}")
            
        try:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;"))
            print("Added created_at successfully.")
        except Exception as e:
            print(f"created_at error: {e}")

if __name__ == "__main__":
    migrate()
