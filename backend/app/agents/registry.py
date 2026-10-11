from .base_agent import BaseAgent

class AgentRegistry:
    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent)->None:
        self._agents[agent.name] = agent

    def get(self, name: str)->BaseAgent:
        if name not in self._agents:
            raise ValueError(f"Agemt '{name}' is not registered")
        return self._agents[name]

    def find_by_capability(self, capability: str)->list[BaseAgent]:
        return [a for a in self._agents.values() if a.can_handle(capability)]

    def list_agents(self)->list[dict]:
        return[{
            "name": a.name,
            "capabilities": a.capabilities,
        } for a in self._agents.values()]
    