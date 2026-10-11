import asyncio
from datetime import datetime, timezone
from backend.app.agents.registry import AgentRegistry
from backend.app.models.execution import Execution
from backend.app.models.task import Task, TaskStatus
from backend.app.orchestrator.scheduler import Scheduler

class Orchestrator:
    def __init__(self, registry: AgentRegistry):
        self.registry=registry
        self.scheduler=Scheduler()
        self.task_map={}


    async def _execute_task(self, task: Task)->None:
        task.status=TaskStatus.Running

        while task.retry_count <= task.max_retries:
            try:
                agent=self.registry.get(task.agent)
                task_input=task.input.copy()
                task_input["dependencies"]={
                    dep_id: self.task_map[dep_id]. result for dep_id in task.dependencies
                }
                result=await agent.execute(task_input)

                task.result=result
                task.status=TaskStatus.Completed
                task.error=None
                return

            except Exception as exc:
                task.error=str(exc)

                if task.retry_count < task.max_retries:
                    task.retry_count += 1
                    task.status=TaskStatus.Retrying
                else:
                    task.status=TaskStatus.Failed
                    return


    async def run(self, execution: Execution)->Execution:
        execution.status="running"
        execution.started_at=datetime.now(timezone.utc)

        task_map={task.id: task for task in execution.tasks}
        self.task_map=task_map
        if len(task_map) !=len(execution.tasks):
            execution.status="failed"
            execution.error="Duplicate task IDs found"
            execution.completed_at=datetime.now(timezone.utc)
            return execution

        for t in execution.tasks:
            for d_id in t.dependencies:
                if d_id not in task_map:
                    execution.status="failed"
                    execution.error=(f"Task '{t.id}' depends on unknown task " f"'{d_id}'")
                    execution.completed_at=datetime.now(timezone.utc)
                    return execution

        while True:
            pending=[t for t in execution.tasks if t.status==TaskStatus.Pending]
            if not pending:
                break

            ready_tasks=self.scheduler.get_ready_tasks(execution.tasks)
            if not ready_tasks:
                execution.status="failed"
                execution.error=("Workflow is blocked. Check for circular dependencies or failed prerequisite tasks")
                break
            await asyncio.gather(*[self._execute_task(task) for task in ready_tasks])
            failed_tasks=[t for t in execution.tasks if t.status==TaskStatus.Failed]

            if failed_tasks:
                execution.status="failed"
                execution.error="; ".join(f"{task.id}: {task.error}" for task in failed_tasks)
                break
        if execution.status!="failed":
            execution.status="completed"
            execution.final_result={t.id: t.result for t in execution.tasks}

        execution.completed_at=datetime.now(timezone.utc)
        return execution