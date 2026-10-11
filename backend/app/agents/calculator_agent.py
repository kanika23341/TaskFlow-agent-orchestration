from typing import Any
from .base_agent import BaseAgent

class CalculatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="calculator",capabilities=["calculation", "math"],)

    async def execute(self, task_input: dict[str, Any]) -> dict[str, Any]:
        values = task_input.get("values", [])
        operation = task_input.get("operation", "sum")
        if not values:
            raise ValueError("Provide at least one value.")

        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values):
            raise ValueError("All values must be numbers.")

        if operation == "sum":
            result = sum(values)
        elif operation == "average":
            result = sum(values) / len(values)
        elif operation == "min":
            result = min(values)
        elif operation == "max":
            result = max(values)
        else:
            raise ValueError(f"Unsupported operation: {operation}")

        return {"success": True, "operation": operation, "values": values, "result": result,}