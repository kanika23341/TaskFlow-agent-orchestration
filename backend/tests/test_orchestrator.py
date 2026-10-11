import pytest
from backend.app.agents.registry import AgentRegistry
from backend.app.agents.demo_agent import DemoAgent
from backend.app.models.execution import Execution
from backend.app.models.task import Task, TaskStatus
from backend.app.orchestrator.orchestrator import Orchestrator

@pytest.mark.asyncio
async def test_orchestrator_runs_workflow():
    registry = AgentRegistry()
    registry.register(DemoAgent())
    execution=Execution(
        id="exec-001",
        request="Test a simple  workflow",
        tasks=[
            Task(id="task-1", agent="demo_agent", input={"messages":"Hello"},),
            Task(id="task-2", agent="demo_agent", input={"messages":"World"}, dependencies=["task-1"],),
        ],
    )
    orchestrator=Orchestrator(registry)
    result=await orchestrator.run(execution)
    assert result.status=="completed"
    assert result.tasks[0].status==TaskStatus.Completed
    assert result.tasks[1].status==TaskStatus.Completed
    assert result.final_result is not None
    assert len(result.final_result)==2

@pytest.mark.asyncio
async def test_orchestrator_handles_agent_failure():
    registry=AgentRegistry()
    execution=Execution(
        id="exec-002",
        request="Test a agent is missing",
        tasks=[Task(id="task-1", agent="unknown",),],
    )
    orchestrator=Orchestrator(registry)
    result= await orchestrator.run(execution)

    assert result.status=="failed"
    assert result.tasks[0].status==TaskStatus.Failed
    assert result.error is not None
