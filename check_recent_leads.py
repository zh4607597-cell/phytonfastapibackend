import pymysql
from app.database import DATABASE_URL

# Parse DATABASE_URL
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
    
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        print("Checking recent leads...")
        cursor.execute("SELECT id, lead_name, creation, status FROM `lead` ORDER BY id DESC LIMIT 5;")
        leads = cursor.fetchall()
        for l in leads:
            print(f"Lead ID: {l['id']}, Name: {l['lead_name']}, Created: {l['creation']}, Status: {l['status']}")
            
        print("\nChecking recent logs...")
        cursor.execute("SELECT * FROM lead_log ORDER BY id DESC LIMIT 5;")
        logs = cursor.fetchall()
        for log in logs:
            print(log)

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'connection' in locals():
        connection.close()
