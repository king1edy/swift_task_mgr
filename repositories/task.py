from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate
from .base import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: Session):
        super().__init__(Task, db)

    def get_user_tasks(self, user_id: int) -> List[Task]:
        return self.db.query(Task).filter(Task.user_id == user_id).all()

    def create_user_task(self, task_in: TaskCreate, user_id: int) -> Task:
        task_data = task_in.dict()
        db_task = Task(**task_data, user_id=user_id)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def update_task(self, task_id: int, task_in: TaskUpdate) -> Optional[Task]:
        task = self.get(task_id)
        if task:
            update_data = task_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(task, field, value)
            self.db.commit()
            self.db.refresh(task)
        return task

