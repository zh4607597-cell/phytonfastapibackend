from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.task_comment_model import TaskComment
from app.schemas.task_comment_schema import TaskCommentCreate, TaskCommentUpdate


# CREATE
def create_task_comment(data: TaskCommentCreate, db: Session):
    comment = TaskComment(**data.dict())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


# GET ALL COMMENTS FOR A TASK
def get_task_comments(task_id: int, db: Session, skip: int = 0, limit: int = 100):
    return db.query(TaskComment).filter(
        TaskComment.task_id == task_id
    ).offset(skip).limit(limit).all()


# GET ALL COMMENTS BY USER
def get_user_comments(user_id: int, db: Session, skip: int = 0, limit: int = 100):
    return db.query(TaskComment).filter(
        TaskComment.user_id == user_id
    ).offset(skip).limit(limit).all()


# GET ONE COMMENT
def get_task_comment(comment_id: int, db: Session):
    comment = db.query(TaskComment).filter(TaskComment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Task comment not found")
    return comment


# UPDATE COMMENT
def update_task_comment(comment_id: int, data: TaskCommentUpdate, db: Session):
    comment = get_task_comment(comment_id, db)
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(comment, key, value)
    
    db.commit()
    db.refresh(comment)
    return comment


# DELETE COMMENT
def delete_task_comment(comment_id: int, db: Session):
    comment = get_task_comment(comment_id, db)
    db.delete(comment)
    db.commit()
    return {"detail": "Task comment deleted successfully"}
