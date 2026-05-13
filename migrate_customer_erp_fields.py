from app.database import engine
from sqlalchemy import text

def migrate():
    columns = [
        ("customer_name", "VARCHAR(255)"),
        ("salutation", "VARCHAR(100)"),
        ("gender", "VARCHAR(100)"),
        ("lead_name", "VARCHAR(255)"),
        ("opportunity_name", "VARCHAR(255)"),
        ("image", "TEXT"),
        ("default_price_list", "VARCHAR(255)"),
        ("default_bank_account", "VARCHAR(255)"),
        ("default_currency", "VARCHAR(50)"),
        ("is_internal_customer", "INT DEFAULT 0"),
        ("represents_company", "VARCHAR(255)"),
        ("market_segment", "VARCHAR(255)"),
        ("industry", "VARCHAR(255)"),
        ("customer_pos_id", "VARCHAR(255)"),
        ("website", "VARCHAR(255)"),
        ("language", "VARCHAR(50) DEFAULT 'en'"),
        ("customer_details", "TEXT"),
        ("customer_primary_contact", "VARCHAR(255)"),
        ("mobile_no", "VARCHAR(50)"),
        ("email_id", "VARCHAR(255)"),
        ("customer_primary_address", "TEXT"),
        ("primary_address", "TEXT"),
        ("tax_id", "VARCHAR(100)"),
        ("tax_category", "VARCHAR(100)"),
        ("tax_withholding_category", "VARCHAR(100)"),
        ("payment_terms", "VARCHAR(255)"),
        ("loyalty_program", "VARCHAR(255)"),
        ("loyalty_program_tier", "VARCHAR(255)"),
        ("default_sales_partner", "VARCHAR(255)"),
        ("default_commission_rate", "INT DEFAULT 0"),
        ("so_required", "INT DEFAULT 0"),
        ("dn_required", "INT DEFAULT 0"),
        ("is_frozen", "INT DEFAULT 0"),
        ("disabled", "INT DEFAULT 0"),
        ("_user_tags", "TEXT"),
        ("_comments", "TEXT"),
        ("_assign", "TEXT"),
        ("_liked_by", "TEXT"),
        ("custom_ntn_number", "VARCHAR(255)"),
        ("custom_technical_poc", "VARCHAR(255)"),
        ("custom_aend_address", "VARCHAR(255)"),
        ("custom_bend_address", "VARCHAR(255)"),
        ("custom_static_ip", "VARCHAR(255)"),
        ("custom_vlan_id", "INT DEFAULT 0"),
        ("custom_handover_point", "VARCHAR(255)"),
        ("custom_bandwidth_type", "VARCHAR(255)"),
        ("custom_aggregated_port_speed", "VARCHAR(255)")
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
