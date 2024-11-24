from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from db.session import get_db
from services.task import create_task, get_tasks, update_task, delete_task
from core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=TaskResponse)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return create_task(db, task, current_user)

@router.get("/", response_model=list[TaskResponse])
def read_tasks(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return get_tasks(db, current_user)

@router.put("/{task_id}", response_model=TaskResponse)
def update_existing_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return update_task(db, task_id, task, current_user)

@router.delete("/{task_id}")
def delete_existing_task(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    delete_task(db, task_id, current_user)
    return {"detail": "Task deleted"}
