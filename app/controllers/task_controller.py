from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.task_models import Task
from app.schemas.task_schemas import TaskCreate, TaskUpdate

def create_task_controller(data: TaskCreate, db: Session):
    new_task = Task(**data.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks_controller(db: Session):
    return db.query(Task).all()

def get_task_controller(task_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def update_task_controller(task_id: int, data: TaskUpdate, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    return task