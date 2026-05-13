from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task_comment_schema import TaskCommentCreate, TaskCommentUpdate, TaskCommentResponse
from app.controllers.task_comment_controller import (
    create_task_comment,
    get_task_comments,
    get_user_comments,
    get_task_comment,
    update_task_comment,
    delete_task_comment
)


router = APIRouter(prefix="/task-comments", tags=["Task Comments"])


# CREATE
@router.post("/", response_model=TaskCommentResponse)
def route_create_task_comment(payload: TaskCommentCreate, db: Session = Depends(get_db)):
    return create_task_comment(payload, db)


# GET ALL COMMENTS FOR A TASK
@router.get("/task/{task_id}", response_model=list[TaskCommentResponse])
def route_get_task_comments(
    task_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return get_task_comments(task_id, db, skip=skip, limit=limit)


# GET ALL COMMENTS BY USER
@router.get("/user/{user_id}", response_model=list[TaskCommentResponse])
def route_get_user_comments(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return get_user_comments(user_id, db, skip=skip, limit=limit)


# GET ONE COMMENT
@router.get("/{comment_id}", response_model=TaskCommentResponse)
def route_get_task_comment(comment_id: int, db: Session = Depends(get_db)):
    return get_task_comment(comment_id, db)


# UPDATE COMMENT
@router.put("/{comment_id}", response_model=TaskCommentResponse)
def route_update_task_comment(
    comment_id: int,
    payload: TaskCommentUpdate,
    db: Session = Depends(get_db)
):
    return update_task_comment(comment_id, payload, db)


# DELETE COMMENT
@router.delete("/{comment_id}")
def route_delete_task_comment(comment_id: int, db: Session = Depends(get_db)):
    return delete_task_comment(comment_id, db)
