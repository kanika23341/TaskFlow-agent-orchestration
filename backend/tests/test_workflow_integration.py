import pytest
from backend.app.agents.registry import AgentRegistry
from backend.app.agents.data_agent import DataAgent
from backend.app.agents.calculator_agent import CalculatorAgent
from backend.app.agents.verification_agent import VerificationAgent
from backend.app.models.execution import Execution
from backend.app.models.task import Task, TaskStatus
from backend.app.orchestrator.orchestrator import Orchestrator

@pytest.mark.asyncio
async def test_complete_data_calculation_verification_workflow():
    registry = AgentRegistry()
    registry.register(DataAgent())
    registry.register(CalculatorAgent())
    registry.register(VerificationAgent())
    orchestrator = Orchestrator(registry)
    execution = Execution(
        id="integration-test",
        request="Analyze data and verify the total",
        tasks=[
            Task(id="analyze-data",agent="data",input={"values": [10, 20, 30, 40]},),
            Task(id="calculate-total",agent="calculator",input={"operation": "sum", "values": [10, 20, 30, 40],},),
            Task(id="verify-results",agent="verification",input={},dependencies=["analyze-data", "calculate-total"],),
        ],
    )

    result = await orchestrator.run(execution)
    assert result.status == "completed"
    assert result.final_result["analyze-data"]["total"] == 100
    assert result.final_result["calculate-total"]["result"] == 100
    assert result.final_result["verify-results"]["success"] is True
    assert result.final_result["verify-results"]["checks"]["totals_match"] is True
    assert all(task.status == TaskStatus.Completed for task in result.tasks)