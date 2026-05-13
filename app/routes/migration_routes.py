from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from app.database import get_db
from sqlalchemy.orm import Session
from typing import Dict, Any

router = APIRouter(prefix="/migrate", tags=["Migration"])

@router.post("/add-receiver-id", response_model=Dict[str, Any])
def add_receiver_id_column(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Add receiver_id column to messages table"""
    try:
        # Check if column already exists
        result = db.execute(text("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'messages' AND COLUMN_NAME = 'receiver_id'
        """))

        if result.fetchone():
            return {"message": "receiver_id column already exists"}

        # Add the column
        db.execute(text("""
            ALTER TABLE messages
            ADD COLUMN receiver_id INT NULL
        """))

        # Add foreign key constraint
        try:
            db.execute(text("""
                ALTER TABLE messages
                ADD CONSTRAINT fk_messages_receiver_id
                FOREIGN KEY (receiver_id) REFERENCES users(id)
            """))
        except Exception as e:
            print(f"Warning: Could not add foreign key constraint: {e}")

        # Create index
        try:
            db.execute(text("""
                CREATE INDEX ix_messages_receiver_id ON messages(receiver_id)
            """))
        except Exception as e:
            print(f"Warning: Could not create index: {e}")

        db.commit()
        return {"message": "Successfully added receiver_id column to messages table"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding receiver_id column: {str(e)}")

@router.post("/create-invoices-table", response_model=Dict[str, Any])
def create_invoices_table(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Create invoices table if it doesn't exist"""
    try:
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                lead_id INT NULL,
                invoice_number VARCHAR(50) UNIQUE NOT NULL,
                amount FLOAT NOT NULL DEFAULT 0.0,
                currency VARCHAR(10) DEFAULT 'PKR',
                status VARCHAR(50) DEFAULT 'Pending',
                issue_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                start_date DATETIME,
                due_date DATETIME,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX ix_invoice_customer_id (customer_id),
                INDEX ix_invoice_lead_id (lead_id),
                INDEX ix_invoice_number (invoice_number)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """))
        db.commit()
        return {"message": "Successfully initialized invoices table"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating invoices table: {str(e)}")

@router.post("/add-erp-lead-columns", response_model=Dict[str, Any])
def add_erp_lead_columns(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Add all missing ERP-related columns to the leads table"""
    columns_to_add = [
        ("salutation", "VARCHAR(50)"),
        ("customer_type", "VARCHAR(50)"),
        ("customer_group", "VARCHAR(100)"),
        ("territory", "VARCHAR(100)"),
        ("gender", "VARCHAR(20)"),
        ("lead_name", "VARCHAR(150)"),
        ("opportunity_name", "VARCHAR(150)"),
        ("account_manager", "VARCHAR(150)"),
        ("image", "VARCHAR(255)"),
        ("default_price_list", "VARCHAR(150)"),
        ("default_bank_account", "VARCHAR(150)"),
        ("default_currency", "VARCHAR(20)"),
        ("is_internal_customer", "BOOLEAN DEFAULT FALSE"),
        ("represents_company", "VARCHAR(150)"),
        ("market_segment", "VARCHAR(100)"),
        ("industry", "VARCHAR(100)"),
        ("customer_pos_id", "VARCHAR(100)"),
        ("website", "VARCHAR(255)"),
        ("language", "VARCHAR(20) DEFAULT 'en'"),
        ("customer_details", "TEXT"),
        ("customer_primary_contact", "VARCHAR(150)"),
        ("mobile_no", "VARCHAR(50)"),
        ("email_id", "VARCHAR(150)"),
        ("customer_primary_address", "VARCHAR(255)"),
        ("primary_address", "VARCHAR(255)"),
        ("tax_id", "VARCHAR(100)"),
        ("tax_category", "VARCHAR(100)"),
        ("tax_withholding_category", "VARCHAR(100)"),
        ("payment_terms", "VARCHAR(150)"),
        ("loyalty_program", "VARCHAR(150)"),
        ("loyalty_program_tier", "VARCHAR(150)"),
        ("default_sales_partner", "VARCHAR(150)"),
        ("default_commission_rate", "FLOAT DEFAULT 0.0"),
        ("so_required", "BOOLEAN DEFAULT FALSE"),
        ("dn_required", "BOOLEAN DEFAULT FALSE"),
        ("is_frozen", "BOOLEAN DEFAULT FALSE"),
        ("disabled", "BOOLEAN DEFAULT FALSE"),
        ("custom_ntn_number", "VARCHAR(100)"),
        ("custom_technical_poc", "VARCHAR(150)"),
        ("custom_aend_address", "TEXT"),
        ("custom_bend_address", "TEXT"),
        ("custom_static_ip", "VARCHAR(100)"),
        ("custom_vlan_id", "INT DEFAULT 0"),
        ("custom_handover_point", "VARCHAR(150)"),
        ("custom_bandwidth_type", "VARCHAR(100)"),
        ("custom_aggregated_port_speed", "VARCHAR(100)"),
        ("docstatus", "INT DEFAULT 0"),
        ("doctype", "VARCHAR(50) DEFAULT 'Lead'"),
        ("idx", "INT DEFAULT 0"),
        ("owner", "VARCHAR(150)"),
        ("modified_by", "VARCHAR(150)"),
        ("_user_tags", "TEXT"),
        ("_comments", "TEXT"),
        ("_assign", "TEXT"),
        ("_liked_by", "TEXT"),
        ("state", "VARCHAR(100)"),
        ("zip_code", "VARCHAR(20)"),
        ("country", "VARCHAR(100)")
    ]
    
    try:
        added = []
        skipped = []
        for col_name, col_type in columns_to_add:
            # Check if column exists
            res = db.execute(text(f"SHOW COLUMNS FROM lead LIKE '{col_name}'")).fetchone()
            if not res:
                db.execute(text(f"ALTER TABLE lead ADD COLUMN {col_name} {col_type}"))
                added.append(col_name)
            else:
                skipped.append(col_name)
        
        db.commit()
        return {
            "message": "Migration completed",
            "added_count": len(added),
            "added_columns": added,
            "skipped_count": len(skipped),
            "skipped_columns": skipped
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Migration failed: {str(e)}")


@router.post("/fix-data-tables", response_model=Dict[str, Any])
def fix_data_tables(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Synchronize activation_date across leads and upgrades with version-safe SQL"""
    try:
        # 1. Fix Lead Table
        res_lead = db.execute(text("SHOW COLUMNS FROM lead LIKE 'activation_date'")).fetchone()
        if not res_lead:
            db.execute(text("ALTER TABLE lead ADD COLUMN activation_date DATETIME NULL"))
        
        # 2. Fix Upgrades Table
        # activation_date
        res_upg_date = db.execute(text("SHOW COLUMNS FROM upgrades LIKE 'activation_date'")).fetchone()
        if not res_upg_date:
            db.execute(text("ALTER TABLE upgrades ADD COLUMN activation_date DATETIME NULL"))
        
        # customer_id
        res_upg_cust = db.execute(text("SHOW COLUMNS FROM upgrades LIKE 'customer_id'")).fetchone()
        if not res_upg_cust:
            db.execute(text("ALTER TABLE upgrades ADD COLUMN customer_id INT NULL"))
            db.execute(text("CREATE INDEX ix_upgrade_customer_id ON upgrades(customer_id)"))

        # lead_id
        res_upg_lead = db.execute(text("SHOW COLUMNS FROM upgrades LIKE 'lead_id'")).fetchone()
        if not res_upg_lead:
            db.execute(text("ALTER TABLE upgrades ADD COLUMN lead_id INT NULL"))
            db.execute(text("CREATE INDEX ix_upgrade_lead_id ON upgrades(lead_id)"))

        db.commit()
        return {"message": "Successfully synchronized leads and upgrades tables"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Migration failed: {str(e)}")