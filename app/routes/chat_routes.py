from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.chat_schema import ChatCreate, ChatUpdate, ChatResponse
from app.controllers.chat_controller import (
    create_chat,
    get_all_chats,
    get_chats_by_type,
    get_chat,
    update_chat,
    update_chat_last_message,
    delete_chat,
    search_chats
)
from app.controllers.chat_participant_controller import get_chat_participants


router = APIRouter(prefix="/chats", tags=["Chats"])


# CREATE
@router.post("/", response_model=ChatResponse)
def route_create_chat(payload: ChatCreate, db: Session = Depends(get_db)):
    return create_chat(payload, db)


# GET ALL
@router.get("/", response_model=list[ChatResponse])
def route_get_all_chats(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return get_all_chats(db, skip=skip, limit=limit)


# GET BY TYPE
@router.get("/type/{chat_type}", response_model=list[ChatResponse])
def route_get_chats_by_type(
    chat_type: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return get_chats_by_type(chat_type, db, skip=skip, limit=limit)


# SEARCH
@router.get("/search", response_model=list[ChatResponse])
def route_search_chats(
    q: str = Query(..., description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return search_chats(q, db, skip=skip, limit=limit)


# GET ONE
@router.get("/{chat_id}", response_model=ChatResponse)
def route_get_chat(chat_id: int, db: Session = Depends(get_db)):
    return get_chat(chat_id, db)


# GET PARTICIPANTS
@router.get("/{chat_id}/participants")
def route_get_chat_participants(chat_id: int, db: Session = Depends(get_db)):
    return get_chat_participants(chat_id, db)

# ADD PARTICIPANT
@router.post("/{chat_id}/participants")
def route_add_participant(chat_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    from app.controllers.chat_controller import add_chat_participant
    return add_chat_participant(chat_id, user_id, db)


# UPDATE
@router.put("/{chat_id}", response_model=ChatResponse)
def route_update_chat(
    chat_id: int,
    payload: ChatUpdate,
    db: Session = Depends(get_db)
):
    return update_chat(chat_id, payload, db)


# UPDATE LAST MESSAGE
@router.patch("/{chat_id}/last-message")
def route_update_last_message(
    chat_id: int,
    message: str = Query(..., description="New last message"),
    db: Session = Depends(get_db)
):
    return update_chat_last_message(chat_id, message, db)


# DELETE
@router.delete("/{chat_id}")
def route_delete_chat(chat_id: int, db: Session = Depends(get_db)):
    return delete_chat(chat_id, db)
