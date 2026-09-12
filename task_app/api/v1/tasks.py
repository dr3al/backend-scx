from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()
tasks = []

class TaskIn(BaseModel):
    title: str
    priority: int = Field(default=10, ge=1, le=5)

@router.get("/tasks", status_code=200)
def get_tasks():
    return tasks


@router.post("/tasks", status_code=201)
def post_tasks(task: TaskIn) -> dict:
    task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "priority": task.priority,
    }
    tasks.append(task)

    return task

