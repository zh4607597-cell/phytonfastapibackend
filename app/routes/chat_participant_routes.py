from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.chat_participant_schema import ChatParticipantCreate, ChatParticipantUpdate, ChatParticipantResponse
from app.controllers.chat_participant_controller import (
    add_participant,
    get_chat_participants,
    get_user_chats,
    get_participant,
    update_participant,
    mark_as_read,
    increment_unread_count,
    toggle_mute,
    remove_participant,
    is_participant
)


router = APIRouter(prefix="/chat-participants", tags=["Chat Participants"])


# ADD PARTICIPANT
@router.post("/", response_model=ChatParticipantResponse)
def route_add_participant(payload: ChatParticipantCreate, db: Session = Depends(get_db)):
    return add_participant(payload, db)


# GET PARTICIPANTS IN A CHAT
@router.get("/chat/{chat_id}", response_model=list[ChatParticipantResponse])
def route_get_chat_participants(chat_id: int, db: Session = Depends(get_db)):
    return get_chat_participants(chat_id, db)


# GET CHATS FOR A USER
@router.get("/user/{user_id}", response_model=list[ChatParticipantResponse])
def route_get_user_chats(user_id: int, db: Session = Depends(get_db)):
    return get_user_chats(user_id, db)


# GET ONE PARTICIPANT
@router.get("/{participant_id}", response_model=ChatParticipantResponse)
def route_get_participant(participant_id: int, db: Session = Depends(get_db)):
    return get_participant(participant_id, db)


# UPDATE PARTICIPANT
@router.put("/{participant_id}", response_model=ChatParticipantResponse)
def route_update_participant(
    participant_id: int,
    payload: ChatParticipantUpdate,
    db: Session = Depends(get_db)
):
    return update_participant(participant_id, payload, db)


# MARK AS READ
@router.patch("/{participant_id}/read")
def route_mark_as_read(participant_id: int, db: Session = Depends(get_db)):
    return mark_as_read(participant_id, db)


# INCREMENT UNREAD COUNT
@router.patch("/chat/{chat_id}/increment-unread")
def route_increment_unread_count(
    chat_id: int,
    exclude_user_id: int = Query(..., description="User ID to exclude from increment"),
    db: Session = Depends(get_db)
):
    return increment_unread_count(chat_id, exclude_user_id, db)


# TOGGLE MUTE
@router.patch("/{participant_id}/toggle-mute")
def route_toggle_mute(participant_id: int, db: Session = Depends(get_db)):
    return toggle_mute(participant_id, db)


# CHECK PARTICIPATION
@router.get("/check/{chat_id}/{user_id}")
def route_is_participant(chat_id: int, user_id: int, db: Session = Depends(get_db)):
    return {"is_participant": is_participant(chat_id, user_id, db)}


# REMOVE PARTICIPANT
@router.delete("/{participant_id}")
def route_remove_participant(participant_id: int, db: Session = Depends(get_db)):
    return remove_participant(participant_id, db)
