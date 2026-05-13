from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.chat_model import Chat
from app.schemas.chat_schema import ChatCreate, ChatUpdate


from app.models.chat_participant_model import ChatParticipant

from app.models.user_model import User

# CREATE
def create_chat(data: ChatCreate, db: Session, creator_id: int = 1):
    # Prepare chat data excluding receiver_id which is for participants
    chat_data = data.dict(exclude={'receiver_id'})
    chat = Chat(**chat_data)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    
    # Auto-add creator as participant
    admin = db.query(User).filter(User.id == creator_id).first()
    db.add(ChatParticipant(
        chat_id=chat.id,
        user_id=creator_id,
        participant_name=admin.username if admin else "Admin"
    ))
    
    # Auto-add receiver if provided
    if data.receiver_id:
        receiver = db.query(User).filter(User.id == data.receiver_id).first()
        if receiver:
            db.add(ChatParticipant(
                chat_id=chat.id,
                user_id=data.receiver_id,
                participant_name=receiver.username
            ))
            
    db.commit()
    return chat


# GET ALL
def get_all_chats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Chat).order_by(Chat.updated_at.desc()).offset(skip).limit(limit).all()


# GET BY TYPE
def get_chats_by_type(chat_type: str, db: Session, skip: int = 0, limit: int = 100):
    return db.query(Chat).filter(Chat.type == chat_type).order_by(Chat.updated_at.desc()).offset(skip).limit(limit).all()


# GET ONE
def get_chat(chat_id: int, db: Session):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


# UPDATE
def update_chat(chat_id: int, data: ChatUpdate, db: Session):
    chat = get_chat(chat_id, db)
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(chat, key, value)
    
    db.commit()
    db.refresh(chat)
    return chat


# UPDATE LAST MESSAGE
def update_chat_last_message(chat_id: int, message: str, db: Session):
    chat = get_chat(chat_id, db)
    chat.last_message = message
    chat.last_message_time = func.now()
    db.commit()
    db.refresh(chat)
    return chat


# DELETE
def delete_chat(chat_id: int, db: Session):
    chat = get_chat(chat_id, db)
    db.delete(chat)
    db.commit()
    return {"detail": "Chat deleted successfully"}


# SEARCH CHATS
def search_chats(query: str, db: Session, skip: int = 0, limit: int = 100):
    return db.query(Chat).filter(Chat.name.ilike(f"%{query}%")).order_by(Chat.updated_at.desc()).offset(skip).limit(limit).all()

# GET PARTICIPANTS
def get_chat_participants(chat_id: int, db: Session):
    return db.query(ChatParticipant).filter(ChatParticipant.chat_id == chat_id).all()

# ADD PARTICIPANT
def add_chat_participant(chat_id: int, user_id: int, db: Session):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Check if already participant
    existing = db.query(ChatParticipant).filter_by(chat_id=chat_id, user_id=user_id).first()
    if existing:
        return existing
        
    participant = ChatParticipant(
        chat_id=chat_id,
        user_id=user_id,
        participant_name=user.username
    )
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant
