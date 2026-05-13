import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app.database import engine
from sqlalchemy import text

def add_receiver_id_column():
    """Add receiver_id column to messages table"""
    try:
        with engine.connect() as conn:
            # Check if column already exists
            result = conn.execute(text("""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'messages' AND COLUMN_NAME = 'receiver_id'
            """))

            if result.fetchone():
                print("receiver_id column already exists")
                return

            # Add the column
            conn.execute(text("""
                ALTER TABLE messages
                ADD COLUMN receiver_id INT NULL
            """))

            # Add foreign key constraint
            try:
                conn.execute(text("""
                    ALTER TABLE messages
                    ADD CONSTRAINT fk_messages_receiver_id
                    FOREIGN KEY (receiver_id) REFERENCES users(id)
                """))
            except Exception as e:
                print(f"Warning: Could not add foreign key constraint: {e}")

            # Create index
            try:
                conn.execute(text("""
                    CREATE INDEX ix_messages_receiver_id ON messages(receiver_id)
                """))
            except Exception as e:
                print(f"Warning: Could not create index: {e}")

            conn.commit()
            print("Successfully added receiver_id column to messages table")

    except Exception as e:
        print(f"Error adding receiver_id column: {e}")

if __name__ == "__main__":
    add_receiver_id_column()