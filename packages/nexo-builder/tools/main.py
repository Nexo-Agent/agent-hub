from fastmcp import FastMCP
import sys
import os

# Import existing tools
# Ensure current directory is in path for imports
sys.path.append(os.path.dirname(__file__))
from fs import FileSystemTools
from terminal import TerminalTools
from planner import PlannerTools

# Initialize FastMCP Server
mcp = FastMCP("The Builder")

# Initialize tool classes
fs_tools = FileSystemTools()
term_tools = TerminalTools()
planner_tools = PlannerTools()

# Register File System Tools
@mcp.tool()
def read_file(path: str) -> str:
    """Read content of a file"""
    return fs_tools.read_file(path)

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write content to a file (overwrite)"""
    return fs_tools.write_file(path, content)

@mcp.tool()
def list_dir(path: str) -> str:
    """List files in directory"""
    return fs_tools.list_dir(path)

@mcp.tool()
def search_code(query: str, path: str = ".") -> str:
    """Search text in files (grep)"""
    return fs_tools.search_code(query, path)

# Register Terminal Tools
@mcp.tool()
def run_command(command: str, cwd: str = ".") -> str:
    """Execute a shell command"""
    return term_tools.run_command(command, cwd)

# Register Planner Tools
@mcp.tool()
def create_plan(steps: list[str]) -> str:
    """Create or overwrite the current plan"""
    return planner_tools.create_plan(steps)

@mcp.tool()
def read_plan() -> str:
    """Read the current plan and status"""
    return planner_tools.read_plan()

@mcp.tool()
def mark_step_done() -> str:
    """Mark the current step as done and advance"""
    return planner_tools.mark_step_done()

if __name__ == "__main__":
    mcp.run()
