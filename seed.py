from app.database import SessionLocal
from app.models.user_model import User
from app.models.chat_model import Chat
from app.models.message_model import Message
from app.models.chat_participant_model import ChatParticipant
from datetime import datetime

def seed():
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin = db.query(User).filter(User.id == 1).first()
        if not admin:
            print("Seeding admin user...")
            admin = User(
                id=1,
                username="admin",
                email="admin@pacetel.com",
                first_name="Admin",
                last_name="User",
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("Admin user created!")
        else:
            print("Admin user already exists.")

        # Seed initial chats if none exist
        chat_count = db.query(Chat).count()
        if chat_count == 0:
            print("Seeding initial chats...")
            
            # Chat 1: Support Channel
            support_chat = Chat(
                name="Customer Support",
                type="channel",
                last_message="Welcome to the support channel!",
                last_message_time=datetime.now()
            )
            db.add(support_chat)
            db.flush() # Get ID
            
            # Add Admin as participant
            db.add(ChatParticipant(chat_id=support_chat.id, user_id=1, role="admin"))

            # Message for Chat 1
            db.add(Message(
                chat_id=support_chat.id,
                sender_id=1,
                sender_name="System",
                message_text="Welcome to the support channel!",
                sent_at=datetime.now()
            ))

            # Chat 2: Team Alpha
            team_chat = Chat(
                name="Operations Team",
                type="group",
                last_message="New inventory update check.",
                last_message_time=datetime.now()
            )
            db.add(team_chat)
            db.flush()

            # Add Admin as participant
            db.add(ChatParticipant(chat_id=team_chat.id, user_id=1, role="admin"))

            db.add(Message(
                chat_id=team_chat.id,
                sender_id=1,
                sender_name="Admin User",
                message_text="New inventory update check.",
                sent_at=datetime.now()
            ))

            db.commit()
            print("Initial chats seeded!")
        else:
            print(f"Total chats: {chat_count}")

    except Exception as e:
        print(f"Error seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
