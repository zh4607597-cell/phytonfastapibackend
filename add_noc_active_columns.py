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
        print("Checking for 'noc_active' column...")
        cursor.execute("SHOW COLUMNS FROM `lead` LIKE 'noc_active';")
        if not cursor.fetchone():
            print("Adding 'noc_active' column...")
            cursor.execute("ALTER TABLE `lead` ADD COLUMN `noc_active` INT DEFAULT 0;")
        else:
            print("'noc_active' column already exists.")

        print("Checking for 'custom_noc_active' column...")
        cursor.execute("SHOW COLUMNS FROM `lead` LIKE 'custom_noc_active';")
        if not cursor.fetchone():
            print("Adding 'custom_noc_active' column...")
            cursor.execute("ALTER TABLE `lead` ADD COLUMN `custom_noc_active` INT DEFAULT 0;")
        else:
            print("'custom_noc_active' column already exists.")
            
        connection.commit()
        print("Migration completed successfully!")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'connection' in locals():
        connection.close()
