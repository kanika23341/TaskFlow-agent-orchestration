import pytest
from backend.app.agents.registry import AgentRegistry
from backend.app.agents.demo_agent import DemoAgent

@pytest.mark.asyncio
async def test_agent_registration():
    registry=AgentRegistry()
    agent=DemoAgent()
    registry.register(agent)
    result=await registry.get("demo_agent").execute({"message":"Hello TaskFlow"})
    assert result["success"] is True
    assert "Hello TaskFlow" in result["message"]