from app.database import engine
from sqlalchemy import text

def migrate():
    print("Migrating database...")
    with engine.connect() as conn:
        try:
            # Check if column exists first to avoid error if it's already there
            conn.execute(text("ALTER TABLE messages ADD COLUMN receiver_id INT NULL"))
            conn.commit()
            print("Added receiver_id column.")
        except Exception as e:
            print(f"receiver_id column might already exist or error: {e}")
            conn.rollback()

        try:
            conn.execute(text("CREATE INDEX idx_receiver_id ON messages (receiver_id)"))
            conn.commit()
            print("Added index.")
        except Exception as e:
            print(f"Index might already exist or error: {e}")
            conn.rollback()

        try:
            conn.execute(text("ALTER TABLE messages ADD CONSTRAINT fk_messages_receiver FOREIGN KEY (receiver_id) REFERENCES users(id)"))
            conn.commit()
            print("Added foreign key constraint.")
        except Exception as e:
            print(f"Constraint might already exist or error: {e}")
            conn.rollback()

    print("Migration complete.")

if __name__ == "__main__":
    migrate()
