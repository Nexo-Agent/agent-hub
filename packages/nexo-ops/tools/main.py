from fastmcp import FastMCP
import sys
import os

# Import existing tools
sys.path.append(os.path.dirname(__file__))
from docker_client import DockerTools
from network_utils import NetworkTools

# Initialize FastMCP Server
mcp = FastMCP("Cloud Commander")

# Initialize tool classes
docker = DockerTools()
net = NetworkTools()

# Register Docker Tools
@mcp.tool()
def docker_list(all: bool = False) -> str:
    """List all running containers"""
    return docker.list_containers(all)

@mcp.tool()
def docker_logs(container_id: str, tail: int = 20) -> str:
    """Get logs of a container"""
    return docker.get_logs(container_id, tail)

@mcp.tool()
def docker_restart(container_id: str) -> str:
    """Restart a container"""
    return docker.restart_container(container_id)

# Register Network Tools
@mcp.tool()
def check_health(url: str) -> str:
    """Check if a URL is reachable (curl)"""
    return net.check_health(url)

@mcp.tool()
def check_port(host: str, port: int) -> str:
    """Check if a TCP port is open on a host"""
    return net.check_port(host, port)

if __name__ == "__main__":
    mcp.run()
