from backend.app.models.task import Task, TaskStatus
from backend.app.orchestrator.scheduler import Scheduler

def test_scheduler_finds_ready_tasks():
    tasks=[
        Task(id="task-1", agent="research",),
        Task(id="task-2", agent="calculator", dependencies=["task-1"],)
    ]
    scheduler=Scheduler()
    ready=scheduler.get_ready_tasks(tasks)
    assert len(ready)==1
    assert ready[0].id == "task-1"

def test_scheduler_unlocks_dependent_task():
    tasks=[
        Task(id="task-1", agent="research", status=TaskStatus.Completed,),
        Task(id="task-2", agent="calculator", dependencies=["task-1"],),
    ]
    scheduler=Scheduler()
    ready=scheduler.get_ready_tasks(tasks)
    assert len(ready)==1
    assert ready[0].id=="task-2"

def test_scheduler_supports_parallel_tasks():
    tasks=[
        Task(id="task-1", agent="research",),
        Task(id="task-2", agent="data",),
        Task(id="task-3", agent="verification", dependencies=["task-1", "task-2"],),
    ]
    scheduler=Scheduler()
    ready=scheduler.get_ready_tasks(tasks)
    assert len(ready)==2
    ready_ids={task.id for task in ready}
    assert ready_ids=={"task-1", "task-2"}