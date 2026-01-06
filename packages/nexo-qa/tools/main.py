from mcp.server.fastmcp import FastMCP
import sys
import os

# Import existing tools
sys.path.append(os.path.dirname(__file__))
from browser_control import BrowserTools
from visual_diff import VisualTools

# Initialize FastMCP Server
mcp = FastMCP("QA Auto-Pilot", dependencies=["mcp", "playwright"])

# Initialize tool classes
browser = BrowserTools()
visual = VisualTools()

# Register Browser Tools
@mcp.tool()
def browser_navigate(url: str) -> str:
    """Navigate to a URL"""
    return browser.navigate(url)

@mcp.tool()
def browser_screenshot(path: str) -> str:
    """Take a screenshot of the current page"""
    return browser.screenshot(path)

# Register Visual Tools
@mcp.tool()
def compare_images(img1: str, img2: str) -> str:
    """Compare two images and return similarity score"""
    return visual.compare_images(img1, img2)

if __name__ == "__main__":
    mcp.run()
