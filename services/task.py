from typing import List, Optional
from fastapi import HTTPException
from ..repositories.task import TaskRepository
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create_task(self, task_data: TaskCreate, user_id: int) -> TaskResponse:
        task = self.task_repository.create_user_task(task_data, user_id)
        return TaskResponse.from_orm(task)

    def get_user_tasks(self, user_id: int) -> List[TaskResponse]:
        tasks = self.task_repository.get_user_tasks(user_id)
        return [TaskResponse.from_orm(task) for task in tasks]

    def get_task(self, task_id: int, user_id: int) -> TaskResponse:
        task = self.task_repository.get(task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskResponse.from_orm(task)

    def update_task(self, task_id: int, task_data: TaskUpdate, user_id: int) -> TaskResponse:
        task = self.task_repository.get(task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")
        updated_task = self.task_repository.update_task(task_id, task_data)
        return TaskResponse.from_orm(updated_task)

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.task_repository.get(task_id)
        if not task or task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")
        self.task_repository.delete(task_id)


from sqlalchemy.orm import Session
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException


def create_task(db: Session, task: TaskCreate, current_user: str):
    db_task = Task(**task.dict(), owner_username=current_user)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, current_user: str):
    return db.query(Task).filter(Task.owner_username == current_user).all()


def update_task(db: Session, task_id: int, task: TaskUpdate, current_user: str):
    db_task = db.query(Task).filter(Task.id == task_id, Task.owner_username == current_user).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, current_user: str):
    db_task = db.query(Task).filter(Task.id == task_id, Task.owner_username == current_user).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
