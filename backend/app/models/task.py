from enum import Enum
from typing import Any
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    Pending="pending"
    Running="running"
    Completed="completed"
    Failed="failed"
    Retrying="retrying"

class Task(BaseModel):
    id: str
    agent: str
    input: dict[str,Any]=Field(default_factory=dict)
    status: TaskStatus=TaskStatus.Pending
    priority: int=1
    dependencies: list[str]=Field(default_factory=list)
    result: dict[str,Any] | None=None
    error: str|None =None
    retry_count: int=0
    max_retries: int=3
