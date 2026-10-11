from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.app.agents.registry import AgentRegistry
from backend.app.agents.demo_agent import DemoAgent
from backend.app.agents.calculator_agent import CalculatorAgent
from backend.app.agents.data_agent import DataAgent
from backend.app.agents.verification_agent import VerificationAgent
from backend.app.models.execution import Execution
from backend.app.models.task import Task
from backend.app.orchestrator.orchestrator import Orchestrator

app = FastAPI(title="TaskFlow",description="A dependency-aware multi-agent orchestration engine", version="1.0.0",)
registry = AgentRegistry()
registry.register(DemoAgent())
registry.register(CalculatorAgent())
registry.register(DataAgent())
registry.register(VerificationAgent())
orchestrator = Orchestrator(registry)
executions = {}

class WorkflowRequest(BaseModel):
    request: str
    tasks: list[Task]

@app.get("/")
async def home():
    return {
        "message": "TaskFlow API is running",
        "docs": "/docs",
    }

@app.get("/agents")
async def get_agents():
    return {"agents": registry.list_agents()}

@app.post("/workflows")
async def run_workflow(workflow: WorkflowRequest):
    execution = Execution(id=str(uuid4()),request=workflow.request,tasks=workflow.tasks,)
    result = await orchestrator.run(execution)
    executions[result.id] = result
    if result.status == "failed":
        raise HTTPException(
            status_code=400,
            detail={"execution_id": result.id,"error": result.error,"execution": result.model_dump(mode="json"),},
        )
    return result.model_dump(mode="json")


@app.get("/workflows/{execution_id}")
async def get_workflow(execution_id: str):
    execution = executions.get(execution_id)
    if execution is None:
        raise HTTPException(status_code=404,detail="Workflow execution not found",)
    return execution.model_dump(mode="json")