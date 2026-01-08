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
                    "description": "Take a screenshot of a URL",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"},
                            "path": {"type": "string"}
                        },
                        "required": ["url", "path"]
                    }
                }
            }
        }

    async def navigate(self, url: str) -> str:
        try:
            from playwright.async_api import async_playwright
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, wait_until="domcontentloaded")
                title = await page.title()
                content = await page.evaluate("document.body.innerText")
                await browser.close()
                return f"Successfully navigated to {url}.\nPage title: {title}\nPage content:\n{content}"
        except ImportError:
            return "Error: Playwright not installed. Please run `pip install playwright && playwright install`."
        except Exception as e:
            return f"Error navigating: {e}"

    async def screenshot(self, url: str, path: str) -> str:
        try:
            from playwright.async_api import async_playwright
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, wait_until="networkidle")
                await page.screenshot(path=path)
                await browser.close()
                return f"Successfully saved screenshot of {url} to {path}"
        except ImportError:
            return "Error: Playwright not installed. Please run `pip install playwright && playwright install`."
        except Exception as e:
            return f"Error taking screenshot: {e}"
