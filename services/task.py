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
