# TaskFlow — Multi-Agent Orchestration Engine
TaskFlow is a Python-based backend that coordinates multiple specialized agents to execute tasks, manage dependencies, and combine their results into a single workflow.

## Features
* **Agent registry:** Register agents and discover them by name or capability.
* **Asynchronous execution:** Execute independent tasks concurrently.
* **Dependency-aware scheduling:** Run dependent tasks only after their prerequisites finish successfully.
* **Retry handling:** Retry failed task executions up to the configured limit.
* **Specialized agents:** Includes calculator, data analysis, verification, and demo agents.
* **Workflow tracking:** Track task statuses, errors, timestamps, and final results.
* **REST API:** Create workflows and retrieve execution details through FastAPI.
* **Automated tests:** Unit and integration tests using pytest.

## Architecture
```text
Client
  |
  v
FastAPI
  |
  v
Orchestrator
  |
  +--> Agent Registry
  |
  +--> Dependency Scheduler
  |
  +--> Task Execution and Retry Handling
          |
          +--> Data Agent
          +--> Calculator Agent
          +--> Verification Agent
          +--> Demo Agent
  |
  v
Workflow Results
```

## Tech Stack
* Python
* FastAPI
* Pydantic
* asyncio
* pytest
* Uvicorn
