from typing import Any
from .base_agent import BaseAgent
class DataAgent(BaseAgent):
    def __init__(self):
         super().__init__(name="data", capabilities=["data_processing","statistics"],)
    async def execute(self, task_input: dict[str,Any])->dict[str,Any]:
         values=task_input.get("values",[])
         if not values:
              raise ValueError("Provide a non empty value list")
         if not all(isinstance(v,(int,float)) and not isinstance(v,bool) for v in values):
              raise ValueError("All values must be numbers")
         return{
              "success": True,
              "count": len(values),
              "total": sum(values),
              "minimum": min(values),
              "maximum":max(values),
              "average":sum(values)/len(values),
         }



