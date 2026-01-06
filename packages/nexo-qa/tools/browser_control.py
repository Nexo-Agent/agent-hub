from typing import Dict, Any

class BrowserTools:
    def __init__(self):
        # We try to import playwright here. If it fails, the tools will report the error at runtime.
        # This keeps the agent loadable even without dependencies installed.
        pass

    def get_tools(self) -> Dict[str, Any]:
        return {
            "browser_navigate": {
                "handler": self.navigate,
                "schema": {
                    "name": "browser_navigate",
                    "description": "Navigate to a URL",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"url": {"type": "string"}},
                        "required": ["url"]
                    }
                }
            },
            "browser_screenshot": {
                "handler": self.screenshot,
                "schema": {
                    "name": "browser_screenshot",
                    "description": "Take a screenshot of the current page",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"]
                    }
                }
            }
        }

    def navigate(self, url: str) -> str:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url)
                title = page.title()
                browser.close()
                return f"Successfully navigated to {url}. Page title: {title}"
        except ImportError:
            return "Error: Playwright not installed. Please run `pip install playwright && playwright install`."
        except Exception as e:
            return f"Error navigating: {e}"

    def screenshot(self, path: str) -> str:
        # Note: In a real stateful agent, we would keep the browser open between calls.
        # For this MVP stateless implementation, we can't easily screenshot a page we just navigated away from.
        # This acts as a placeholder or needs a stateful daemon.
        return "Error: Browser session is stateless in this MVP. Cannot screenshot without active page."
