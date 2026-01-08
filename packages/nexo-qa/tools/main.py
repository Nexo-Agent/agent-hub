from fastmcp import FastMCP
import sys
import os

# Import existing tools
sys.path.append(os.path.dirname(__file__))
from browser_control import BrowserTools
from visual_diff import VisualTools

# Initialize FastMCP Server
mcp = FastMCP("QA Auto-Pilot")

# Initialize tool classes
browser = BrowserTools()
visual = VisualTools()

# Register Browser Tools
@mcp.tool()
async def browser_navigate(url: str) -> str:
    """Navigate to a URL"""
    return await browser.navigate(url)

@mcp.tool()
async def browser_screenshot(url: str, path: str) -> str:
    """Take a screenshot of a URL"""
    return await browser.screenshot(url, path)

# Register Visual Tools
@mcp.tool()
def compare_images(img1: str, img2: str) -> str:
    """Compare two images and return similarity score"""
    return visual.compare_images(img1, img2)

if __name__ == "__main__":
    mcp.run()
