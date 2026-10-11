from typing import Any
from .base_agent import BaseAgent

class VerificationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="verification",capabilities=["verification", "validation"],)

    async def execute(self, task_input: dict[str, Any]) -> dict[str, Any]:
        dependencies = task_input.get("dependencies", {})
        if not dependencies:
            raise ValueError("No dependency results provided to verify.")

        checks = {}
        for task_id, result in dependencies.items():
            checks[task_id] = (isinstance(result, dict) and result.get("success") is True)
        
        totals = [
            result["total"] if "total" in result else result["result"]
            for result in dependencies.values()
            if isinstance(result, dict)
            and ("total" in result or "result" in result)
        ]

        totals_match = len(totals) < 2 or all(total == totals[0] for total in totals)
        checks["totals_match"] = totals_match
        return {
            "success": all(checks.values()),
            "checks": checks,
            "verified_count": sum(checks.values()),
            "totals": totals,
        }