from typing import Any
from .base_agent import BaseAgent

class DemoAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="demo_agent",
            capabilities=["testing","demo"],
        )

    async def execute(self, task_input: dict[str, Any]):
        message=task_input.get("message","")
        return {
            "success": True,
            "agent": self.name,
            "message": f"Test Agent processed: {message}",
        }
    