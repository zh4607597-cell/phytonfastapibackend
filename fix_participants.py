from app.database import SessionLocal
from app.models.chat_model import Chat
from app.models.chat_participant_model import ChatParticipant
from app.models.user_model import User  # Crucial to import this

def fix():
    db = SessionLocal()
    try:
        chats = db.query(Chat).all()
        admin = db.query(User).filter(User.id == 1).first()
        if not admin:
            print("Admin user not found. Run seed.py first.")
            return

        for chat in chats:
            exists = db.query(ChatParticipant).filter_by(chat_id=chat.id, user_id=1).first()
            if not exists:
                print(f"Adding Admin to chat: {chat.name}")
                db.add(ChatParticipant(
                    chat_id=chat.id, 
                    user_id=1, 
                    participant_name="Admin User"
                ))
        db.commit()
        print("Success: All chats now have Admin as participant.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix()
