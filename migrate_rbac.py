from sqlalchemy import text
from app.database import engine

def run_migration():
    print("Starting migration to add missing RBAC columns...")
    
    with engine.connect() as connection:
        # 1. Update roles table
        print("Checking 'roles' table...")
        try:
            connection.execute(text("ALTER TABLE roles ADD COLUMN description TEXT AFTER role_name"))
            print("Added 'description' to 'roles'")
        except Exception as e:
            print(f"Skipped 'roles.description': {e}")
            
        try:
            connection.execute(text("ALTER TABLE roles ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
            print("Added 'created_at' to 'roles'")
        except Exception as e:
            print(f"Skipped 'roles.created_at': {e}")

        # 2. Update features table
        print("Checking 'features' table...")
        cols_to_add = [
            ("description", "TEXT"),
            ("icon", "VARCHAR(100)"),
            ("path", "VARCHAR(255)"),
            ("parent_id", "INT"),
            ("sort_order", "INT DEFAULT 0"),
            ("is_active", "BOOLEAN DEFAULT TRUE"),
            ("created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
            ("updated_at", "DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        ]
        
        for col_name, col_def in cols_to_add:
            try:
                connection.execute(text(f"ALTER TABLE features ADD COLUMN {col_name} {col_def}"))
                print(f"Added '{col_name}' to 'features'")
            except Exception as e:
                print(f"Skipped 'features.{col_name}': {e}")

        # 3. Update permissions table
        print("Checking 'permissions' table...")
        try:
            connection.execute(text("ALTER TABLE permissions ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
            print("Added 'created_at' to 'permissions'")
        except Exception as e:
            print(f"Skipped 'permissions.created_at': {e}")

        # 4. User permissions might not exist, so we let init_db handle it, 
        # but if it does exist and missed created_at:
        try:
            connection.execute(text("ALTER TABLE user_permissions ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
            print("Added 'created_at' to 'user_permissions'")
        except Exception as e:
            print(f"Skipped 'user_permissions.created_at': {e}")
            
        connection.commit()
    
    print("Migration completed!")

if __name__ == "__main__":
    run_migration()
