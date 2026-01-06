import subprocess
from typing import Dict, Any

class DockerTools:
    def get_tools(self) -> Dict[str, Any]:
        return {
            "docker_list": {
                "handler": self.list_containers,
                "schema": {
                    "name": "docker_list",
                    "description": "List all running containers",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"all": {"type": "boolean", "default": False}},
                        "required": []
                    }
                }
            },
            "docker_logs": {
                "handler": self.get_logs,
                "schema": {
                    "name": "docker_logs",
                    "description": "Get logs of a container",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "container_id": {"type": "string"},
                            "tail": {"type": "integer", "default": 20}
                        },
                        "required": ["container_id"]
                    }
                }
            },
            "docker_restart": {
                "handler": self.restart_container,
                "schema": {
                    "name": "docker_restart",
                    "description": "Restart a container",
                    "inputSchema": {
                         "type": "object",
                        "properties": {"container_id": {"type": "string"}},
                        "required": ["container_id"]
                    }
                }
            }
        }

    def list_containers(self, all: bool = False) -> str:
        try:
            cmd = ["docker", "ps", "--format", "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"]
            if all:
                cmd.append("-a")
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error listing containers: {e}"

    def get_logs(self, container_id: str, tail: int = 20) -> str:
        try:
            cmd = ["docker", "logs", "--tail", str(tail), container_id]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return f"Logs for {container_id}:\n" + (result.stdout + result.stderr)
        except Exception as e:
            return f"Error getting logs: {e}"

    def restart_container(self, container_id: str) -> str:
        try:
            cmd = ["docker", "restart", container_id]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return f"Restarted {container_id}" if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error restarting container: {e}"
