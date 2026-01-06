import subprocess
from typing import Dict, Any

class TerminalTools:
    def get_tools(self) -> Dict[str, Any]:
        return {
            "run_command": {
                "handler": self.run_command,
                "schema": {
                    "name": "run_command",
                    "description": "Execute a shell command",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string"},
                            "cwd": {"type": "string", "description": "Current working directory"}
                        },
                        "required": ["command"]
                    }
                }
            }
        }

    def run_command(self, command: str, cwd: str = ".") -> str:
        try:
            # Security Note: in production, we should whitelist commands or sandbox this.
            # For this MVP, we run directly.
            result = subprocess.run(
                command,
                cwd=cwd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60 # 1 minute timeout
            )
            
            output = f"Exit Code: {result.returncode}\n"
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}\n"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}\n"
                
            return output
            
        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 60 seconds."
        except Exception as e:
            return f"Error executing command: {e}"
