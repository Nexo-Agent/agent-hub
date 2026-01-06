import subprocess
import socket
from typing import Dict, Any

class NetworkTools:
    def get_tools(self) -> Dict[str, Any]:
        return {
            "check_health": {
                "handler": self.check_health,
                "schema": {
                    "name": "check_health",
                    "description": "Check if a URL is reachable (curl)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"url": {"type": "string"}},
                        "required": ["url"]
                    }
                }
            },
            "check_port": {
                "handler": self.check_port,
                "schema": {
                    "name": "check_port",
                    "description": "Check if a TCP port is open on a host",
                     "inputSchema": {
                        "type": "object",
                        "properties": {
                            "host": {"type": "string"},
                            "port": {"type": "integer"}
                        },
                        "required": ["host", "port"]
                    }
                }
            }
        }

    def check_health(self, url: str) -> str:
        try:
            # Use curl -I for headers only
            cmd = ["curl", "-I", "--max-time", "5", url]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                first_line = result.stdout.split('\n')[0]
                return f"OK: {first_line}"
            else:
                return f"FAIL: {result.stderr}"
        except Exception as e:
            return f"Error checking health: {e}"

    def check_port(self, host: str, port: int) -> str:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return f"Port {host}:{port} is OPEN."
            else:
                return f"Port {host}:{port} is CLOSED (Code: {result})."
        except Exception as e:
            return f"Error checking port: {e}"
