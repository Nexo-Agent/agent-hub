from typing import Dict, Any, List

class PlannerTools:
    def __init__(self):
        self.plan = []
        self.current_step = 0

    def get_tools(self) -> Dict[str, Any]:
        return {
            "create_plan": {
                "handler": self.create_plan,
                "schema": {
                    "name": "create_plan",
                    "description": "Create or overwrite the current plan",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "steps": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["steps"]
                    }
                }
            },
            "read_plan": {
                "handler": self.read_plan,
                "schema": {
                    "name": "read_plan",
                    "description": "Read the current plan and status",
                     "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
             "mark_step_done": {
                "handler": self.mark_step_done,
                 "schema": {
                    "name": "mark_step_done",
                    "description": "Mark the current step as done and advance",
                     "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        }

    def create_plan(self, steps: List[str]) -> str:
        self.plan = steps
        self.current_step = 0
        return f"Plan created with {len(steps)} steps."

    def read_plan(self) -> str:
        if not self.plan:
            return "No active plan."
        
        output = "Current Plan:\n"
        for i, step in enumerate(self.plan):
            status = "[x]" if i < self.current_step else "[ ]"
            if i == self.current_step:
                status = "[>]" # Current
            output += f"{status} {i+1}. {step}\n"
        return output

    def mark_step_done(self) -> str:
        if self.current_step < len(self.plan):
            self.current_step += 1
            return "Step marked as done. Proceeding to next."
        else:
            return "All steps already completed."
