from app.database import engine
from sqlalchemy import text

def recreate_table():
    with engine.connect() as conn:
        try:
            # Drop existing table to avoid conflicts
            conn.execute(text("DROP TABLE IF EXISTS customers"))
            print("Dropped existing customers table.")
            
            # Execute the exact SQL provided
            sql = """
            CREATE TABLE customers (
                id SERIAL PRIMARY KEY,
                customer_code VARCHAR(50) NOT NULL,

                policy_id INTEGER,
                cost_center_id INTEGER,
                agent_id INTEGER,

                customer_name VARCHAR(255),
                customer_type VARCHAR(100) DEFAULT 'Company',
                customer_group VARCHAR(100) DEFAULT 'Commercial',
                territory VARCHAR(100) DEFAULT 'Pakistan',
                salutation VARCHAR(100),
                gender VARCHAR(100),
                lead_name VARCHAR(255),
                opportunity_name VARCHAR(255),
                account_manager VARCHAR(255),
                image TEXT,
                default_price_list VARCHAR(255),
                default_bank_account VARCHAR(255),
                default_currency VARCHAR(50),
                is_internal_customer INTEGER DEFAULT 0,
                represents_company VARCHAR(255),
                market_segment VARCHAR(255),
                industry VARCHAR(255),
                customer_pos_id VARCHAR(255),
                website VARCHAR(255),
                language VARCHAR(50) DEFAULT 'en',
                customer_details TEXT,
                customer_primary_contact VARCHAR(255),
                mobile_no VARCHAR(50),
                email_id VARCHAR(255),
                customer_primary_address TEXT,
                primary_address TEXT,
                tax_id VARCHAR(100),
                tax_category VARCHAR(100),
                tax_withholding_category VARCHAR(100),
                payment_terms VARCHAR(255),
                loyalty_program VARCHAR(255),
                loyalty_program_tier VARCHAR(255),
                default_sales_partner VARCHAR(255),
                default_commission_rate INTEGER DEFAULT 0,
                so_required INTEGER DEFAULT 0,
                dn_required INTEGER DEFAULT 0,
                is_frozen INTEGER DEFAULT 0,
                disabled INTEGER DEFAULT 0,
                _user_tags TEXT,
                _comments TEXT,
                _assign TEXT,
                _liked_by TEXT,

                custom_ntn_number VARCHAR(255),
                custom_technical_poc VARCHAR(255),
                custom_aend_address VARCHAR(255),
                custom_bend_address VARCHAR(255),
                custom_static_ip VARCHAR(255),
                custom_vlan_id INTEGER DEFAULT 0,
                custom_handover_point VARCHAR(255),
                custom_bandwidth_type VARCHAR(255),
                custom_aggregated_port_speed VARCHAR(255),

                city VARCHAR(100),

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                created_by INTEGER
            );
            """
            conn.execute(text(sql))
            print("Successfully created customers table.")
            
            # Create index
            conn.execute(text("CREATE INDEX idx_customers_customer_code ON customers(customer_code);"))
            print("Successfully created index on customer_code.")
            
            conn.commit()
            print("All done!")
        except Exception as e:
            print(f"Error during execution: {e}")

if __name__ == "__main__":
    recreate_table()
