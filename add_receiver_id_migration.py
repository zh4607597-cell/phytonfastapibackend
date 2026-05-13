from sqlalchemy import create_engine, text
from app.database import DATABASE_URL

def add_receiver_id_column():
    """Add receiver_id column to messages table"""
    engine = create_engine(DATABASE_URL)

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
            ADD COLUMN receiver_id INT NULL,
            ADD CONSTRAINT fk_messages_receiver_id
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        """))

        # Create index
        conn.execute(text("""
            CREATE INDEX ix_messages_receiver_id ON messages(receiver_id)
        """))

        conn.commit()
        print("Successfully added receiver_id column to messages table")

if __name__ == "__main__":
    add_receiver_id_column()