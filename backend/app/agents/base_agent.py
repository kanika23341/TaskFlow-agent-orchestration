from abc import ABC, abstractmethod
from typing import Any
class BaseAgent(ABC):
    def __init__(self, name: str, capabilities: list[str]):
        self.name = name
        self.capabilities = capabilities

    @abstractmethod
    async def execute(self, task_input: dict[str, Any])-> dict[str,Any]:
        pass

    def can_handle(self, capability: str)->bool:
        return capability in self.capabilities