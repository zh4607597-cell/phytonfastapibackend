from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.chat_participant_model import ChatParticipant
from app.models.chat_model import Chat
from app.schemas.chat_participant_schema import ChatParticipantCreate, ChatParticipantUpdate


# ADD PARTICIPANT TO CHAT
def add_participant(data: ChatParticipantCreate, db: Session):
    # Check if chat exists
    chat = db.query(Chat).filter(Chat.id == data.chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Check if user is already a participant
    existing = db.query(ChatParticipant).filter(
        ChatParticipant.chat_id == data.chat_id,
        ChatParticipant.user_id == data.user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User is already a participant in this chat")

    participant = ChatParticipant(**data.dict())
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


# GET ALL PARTICIPANTS IN A CHAT
def get_chat_participants(chat_id: int, db: Session):
    return db.query(ChatParticipant).filter(ChatParticipant.chat_id == chat_id).all()


# GET ALL CHATS FOR A USER
def get_user_chats(user_id: int, db: Session):
    return db.query(ChatParticipant).filter(ChatParticipant.user_id == user_id).all()


# GET ONE PARTICIPANT
def get_participant(participant_id: int, db: Session):
    participant = db.query(ChatParticipant).filter(ChatParticipant.id == participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Chat participant not found")
    return participant


# UPDATE PARTICIPANT
def update_participant(participant_id: int, data: ChatParticipantUpdate, db: Session):
    participant = get_participant(participant_id, db)
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(participant, key, value)
    
    db.commit()
    db.refresh(participant)
    return participant


# MARK MESSAGES AS READ
def mark_as_read(participant_id: int, db: Session):
    participant = get_participant(participant_id, db)
    participant.unread_count = 0
    participant.last_read_at = db.func.now()
    db.commit()
    db.refresh(participant)
    return participant


# INCREMENT UNREAD COUNT
def increment_unread_count(chat_id: int, exclude_user_id: int, db: Session):
    participants = db.query(ChatParticipant).filter(
        ChatParticipant.chat_id == chat_id,
        ChatParticipant.user_id != exclude_user_id
    ).all()
    
    for participant in participants:
        participant.unread_count += 1
    
    db.commit()
    return {"detail": f"Unread count incremented for {len(participants)} participants"}


# TOGGLE MUTE
def toggle_mute(participant_id: int, db: Session):
    participant = get_participant(participant_id, db)
    participant.muted = not participant.muted
    db.commit()
    db.refresh(participant)
    return participant


# REMOVE PARTICIPANT
def remove_participant(participant_id: int, db: Session):
    participant = get_participant(participant_id, db)
    db.delete(participant)
    db.commit()
    return {"detail": "Participant removed from chat successfully"}


# CHECK IF USER IS PARTICIPANT
def is_participant(chat_id: int, user_id: int, db: Session):
    participant = db.query(ChatParticipant).filter(
        ChatParticipant.chat_id == chat_id,
        ChatParticipant.user_id == user_id
    ).first()
    return participant is not None
