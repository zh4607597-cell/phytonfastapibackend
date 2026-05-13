from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.message_model import Message
from app.models.chat_model import Chat
from app.models.chat_participant_model import ChatParticipant
from app.schemas.message_schema import MessageCreate, MessageUpdate


# SEND MESSAGE
def send_message(data: MessageCreate, db: Session):
    # Check if chat exists
    chat = db.query(Chat).filter(Chat.id == data.chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Check if sender is a participant
    participant = db.query(ChatParticipant).filter(
        ChatParticipant.chat_id == data.chat_id,
        ChatParticipant.user_id == data.sender_id
    ).first()
    if not participant:
        raise HTTPException(status_code=403, detail="User is not a participant in this chat")

    # Create message
    message = Message(**data.dict())
    db.add(message)

    # Update chat's last message
    chat.last_message = data.message_text
    chat.last_message_time = func.now()

    # Increment unread count for all participants except sender
    participants = db.query(ChatParticipant).filter(
        ChatParticipant.chat_id == data.chat_id,
        ChatParticipant.user_id != data.sender_id
    ).all()

    for p in participants:
        p.unread_count += 1

    db.commit()
    db.refresh(message)
    return message


# GET MESSAGES IN A CHAT
def get_chat_messages(chat_id: int, db: Session, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(
        Message.chat_id == chat_id
    ).order_by(Message.sent_at.asc()).offset(skip).limit(limit).all()


# GET MESSAGES FROM A USER
def get_user_messages(user_id: int, db: Session, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(
        Message.sender_id == user_id
    ).order_by(Message.sent_at.desc()).offset(skip).limit(limit).all()


# GET ONE MESSAGE
def get_message(message_id: int, db: Session):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


# UPDATE MESSAGE
def update_message(message_id: int, data: MessageUpdate, db: Session):
    message = get_message(message_id, db)
    
    # Only allow updating message text and read status
    for key, value in data.dict(exclude_unset=True).items():
        if key in ['message_text', 'is_read']:
            setattr(message, key, value)
    
    db.commit()
    db.refresh(message)
    return message


# MARK MESSAGE AS READ
def mark_message_read(message_id: int, db: Session):
    message = get_message(message_id, db)
    message.is_read = True
    db.commit()
    db.refresh(message)
    return message


# MARK ALL MESSAGES AS READ IN CHAT FOR USER
def mark_chat_messages_read(chat_id: int, user_id: int, db: Session):
    # Update all unread messages in chat for this user
    db.query(Message).filter(
        Message.chat_id == chat_id,
        Message.sender_id != user_id,
        Message.is_read == False
    ).update({"is_read": True})

    # Reset unread count for participant
    participant = db.query(ChatParticipant).filter(
        ChatParticipant.chat_id == chat_id,
        ChatParticipant.user_id == user_id
    ).first()
    if participant:
        participant.unread_count = 0
        participant.last_read_at = func.now()

    db.commit()
    return {"detail": "All messages marked as read"}


# DELETE MESSAGE
def delete_message(message_id: int, db: Session):
    message = get_message(message_id, db)
    db.delete(message)
    db.commit()
    return {"detail": "Message deleted successfully"}


# SEARCH MESSAGES
def search_messages(chat_id: int, query: str, db: Session, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(
        Message.chat_id == chat_id,
        Message.message_text.ilike(f"%{query}%")
    ).order_by(Message.sent_at.desc()).offset(skip).limit(limit).all()
