from datetime import datetime, timezone
from pydantic import BaseModel, Field
from .task import Task
class ExecutionStatus(str):
    Pending="pending"
    Running="running"
    Completed="completed"
    Failed="failed"

class Execution(BaseModel):
    id: str
    request: str
    status: str=ExecutionStatus.Pending
    tasks: list[Task]=Field(default_factory=list)
    created_at: datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: datetime|None=None
    completed_at: datetime|None=None
    final_result: dict|None=None
    error: str|None=None