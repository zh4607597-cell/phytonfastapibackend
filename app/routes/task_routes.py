from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.schemas.task_schemas import TaskCreate, TaskOut, TaskUpdate
from app.controllers.task_controller import create_task_controller, get_tasks_controller, get_task_controller, update_task_controller

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TaskOut)
def route_create_task(data: TaskCreate, db: Session = Depends(get_db)):
    return create_task_controller(data, db)

@router.get("/", response_model=List[TaskOut])
def route_get_tasks(db: Session = Depends(get_db)):
    return get_tasks_controller(db)

@router.get("/{task_id}", response_model=TaskOut)
def route_get_task(task_id: int, db: Session = Depends(get_db)):
    return get_task_controller(task_id, db)

@router.put("/{task_id}", response_model=TaskOut)
def route_update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    return update_task_controller(task_id, data, db)