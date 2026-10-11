from backend.app.models.task import Task, TaskStatus
from backend.app.models.execution import Execution

def test_task_creation():
    task=Task(
        id="task-001",
        agent="calculator",
        input={
            "operation":"sum",
            "values":[10,20,30],
        },
    )

    assert task.id=="task-001"
    assert task.agent=="calculator"
    assert task.status==TaskStatus.Pending
    assert task.retry_count==0

def test_task_dependencies():
    task=Task(
        id="task-002",
        agent="verificatoion",
        dependencies=["task-001"],
    )

    assert "task-001" in task.dependencies

def test_execution_creation():
    execution=Execution(
        id="exec-001",
        request="Calculate the total sales",
    )
    assert execution.id == "exec-001"
    assert execution.request == "Calculate the total sales"
    assert execution.status == "pending"
    assert execution.tasks == []