from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.message_schema import MessageCreate, MessageUpdate, MessageResponse
from app.controllers.message_controller import (
    send_message,
    get_chat_messages,
    get_user_messages,
    get_message,
    update_message,
    mark_message_read,
    mark_chat_messages_read,
    delete_message,
    search_messages
)


router = APIRouter(prefix="/messages", tags=["Messages"])


# SEND MESSAGE
@router.post("/", response_model=MessageResponse)
def route_send_message(payload: MessageCreate, db: Session = Depends(get_db)):
    return send_message(payload, db)


# GET MESSAGES IN A CHAT
@router.get("/chat/{chat_id}", response_model=list[MessageResponse])
def route_get_chat_messages(
    chat_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return get_chat_messages(chat_id, db, skip=skip, limit=limit)


# GET MESSAGES FROM A USER
@router.get("/user/{user_id}", response_model=list[MessageResponse])
def route_get_user_messages(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return get_user_messages(user_id, db, skip=skip, limit=limit)


# SEARCH MESSAGES IN CHAT
@router.get("/chat/{chat_id}/search", response_model=list[MessageResponse])
def route_search_messages(
    chat_id: int,
    q: str = Query(..., description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return search_messages(chat_id, q, db, skip=skip, limit=limit)


# GET ONE MESSAGE
@router.get("/{message_id}", response_model=MessageResponse)
def route_get_message(message_id: int, db: Session = Depends(get_db)):
    return get_message(message_id, db)


# UPDATE MESSAGE
@router.put("/{message_id}", response_model=MessageResponse)
def route_update_message(
    message_id: int,
    payload: MessageUpdate,
    db: Session = Depends(get_db)
):
    return update_message(message_id, payload, db)


# MARK MESSAGE AS READ
@router.patch("/{message_id}/read")
def route_mark_message_read(message_id: int, db: Session = Depends(get_db)):
    return mark_message_read(message_id, db)


# MARK ALL MESSAGES AS READ IN CHAT
@router.patch("/chat/{chat_id}/read-all")
def route_mark_chat_messages_read(
    chat_id: int,
    user_id: int = Query(..., description="User ID marking messages as read"),
    db: Session = Depends(get_db)
):
    return mark_chat_messages_read(chat_id, user_id, db)


# DELETE MESSAGE
@router.delete("/{message_id}")
def route_delete_message(message_id: int, db: Session = Depends(get_db)):
    return delete_message(message_id, db)
