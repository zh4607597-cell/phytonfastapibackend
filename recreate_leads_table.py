import pymysql
from app.database import DATABASE_URL

# Parse DATABASE_URL
# mysql+pymysql://root:@localhost/crmdb
conn_str = DATABASE_URL.replace("mysql+pymysql://", "")
user_pass, host_db = conn_str.split("@")
user, password = user_pass.split(":") if ":" in user_pass else (user_pass, "")
host, db_name = host_db.split("/")

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    
    with connection.cursor() as cursor:
        print(f"Dropping existing 'lead' table if exists...")
        cursor.execute("DROP TABLE IF EXISTS `lead`;")
        
        print(f"Creating 'lead' table with FULL schema including ERP fields...")
        create_sql = """
        CREATE TABLE `lead` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            creation DATETIME DEFAULT CURRENT_TIMESTAMP,
            modified DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            modified_by VARCHAR(100),
            owner VARCHAR(100),

            docstatus INT DEFAULT 0,
            doctype VARCHAR(50) DEFAULT 'Lead',
            idx INT DEFAULT 0,

            lead_name VARCHAR(100),
            lead_owner VARCHAR(100),
            status VARCHAR(50),
            source VARCHAR(100),
            lead_type VARCHAR(50),
            request_type VARCHAR(100),

            salutation VARCHAR(50),
            first_name VARCHAR(100),
            middle_name VARCHAR(100),
            last_name VARCHAR(100),

            customer_name VARCHAR(255),
            company_name VARCHAR(255),
            customer_type VARCHAR(50) DEFAULT 'Company',
            customer_group VARCHAR(100) DEFAULT 'Commercial',

            job_title VARCHAR(100),
            gender VARCHAR(20),

            phone VARCHAR(50),
            mobile_no VARCHAR(50),
            phone_ext VARCHAR(20),
            whatsapp VARCHAR(50),
            email_id VARCHAR(150),
            website VARCHAR(255),

            address_line1 VARCHAR(255),
            address_line2 VARCHAR(255),
            city VARCHAR(100),
            state VARCHAR(100),
            country VARCHAR(100),

            territory VARCHAR(100),
            language VARCHAR(20) DEFAULT 'en',

            no_of_employees VARCHAR(50),
            annual_revenue DECIMAL(15,2) DEFAULT 0.00,
            industry VARCHAR(100),
            market_segment VARCHAR(100),

            qualification_status VARCHAR(50),
            qualified_by VARCHAR(100),
            qualified_on DATETIME,

            campaign_name VARCHAR(100),
            company VARCHAR(100),

            unsubscribed TINYINT(1) DEFAULT 0,
            blog_subscriber TINYINT(1) DEFAULT 0,
            disabled TINYINT(1) DEFAULT 0,

            image TEXT,

            -- ERP Specific & Custom Fields
            opportunity_name VARCHAR(100),
            account_manager VARCHAR(100),
            default_price_list VARCHAR(100),
            default_bank_account VARCHAR(100),
            default_currency VARCHAR(20) DEFAULT 'PKR',
            is_internal_customer INT DEFAULT 0,
            represents_company VARCHAR(100),
            customer_pos_id VARCHAR(100),
            customer_details TEXT,
            customer_primary_contact VARCHAR(100),
            customer_primary_address TEXT,
            primary_address TEXT,
            tax_id VARCHAR(100),
            tax_category VARCHAR(100),
            tax_withholding_category VARCHAR(100),
            payment_terms VARCHAR(100),
            loyalty_program VARCHAR(100),
            loyalty_program_tier VARCHAR(100),
            default_sales_partner VARCHAR(100),
            default_commission_rate FLOAT DEFAULT 0.0,
            so_required INT DEFAULT 0,
            dn_required INT DEFAULT 0,
            is_frozen INT DEFAULT 0,
            
            -- Custom Technical Fields
            custom_ntn_number VARCHAR(100),
            custom_technical_poc VARCHAR(100),
            custom_aend_address TEXT,
            custom_bend_address TEXT,
            custom_static_ip VARCHAR(100),
            custom_vlan_id INT DEFAULT 0,
            custom_handover_point VARCHAR(255),
            custom_bandwidth_type VARCHAR(100),
            custom_aggregated_port_speed VARCHAR(100),
            noc_active INT DEFAULT 0,
            custom_noc_active INT DEFAULT 0
        );
        """
        cursor.execute(create_sql)
        connection.commit()
        print("Table 'lead' recreated with full schema successfully!")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'connection' in locals():
        connection.close()
