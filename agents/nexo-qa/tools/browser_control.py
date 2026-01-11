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
            from playwright_stealth import stealth_async
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                # Create a bridge between the browser and context to handle stealth better
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    viewport={'width': 1280, 'height': 720},
                    locale="en-US",
                    timezone_id="America/New_York",
                    extra_http_headers={
                        "Accept-Language": "en-US,en;q=0.9",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    }
                )
                page = await context.new_page()
                # Apply stealth
                await stealth_async(page)
                
                await page.goto(url, wait_until="domcontentloaded")
                # Wait a bit more for some dynamic content if any
                await page.wait_for_timeout(2000)
                
                title = await page.title()
                content = await page.evaluate("document.body.innerText")
                await browser.close()
                return f"Successfully navigated to {url}.\nPage title: {title}\nPage content:\n{content}"
        except ImportError:
            return "Error: Playwright or Playwright-Stealth not installed. Please run `pip install playwright playwright-stealth && playwright install`."
        except Exception as e:
            return f"Error navigating: {e}"

    async def screenshot(self, url: str, path: str) -> str:
        try:
            from playwright.async_api import async_playwright
            from playwright_stealth import stealth_async
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    viewport={'width': 1280, 'height': 720},
                    locale="en-US",
                    timezone_id="America/New_York",
                    extra_http_headers={
                        "Accept-Language": "en-US,en;q=0.9",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    }
                )
                page = await context.new_page()
                # Apply stealth
                await stealth_async(page)
                
                await page.goto(url, wait_until="networkidle")
                await page.screenshot(path=path)
                await browser.close()
                return f"Successfully saved screenshot of {url} to {path}"
        except ImportError:
            return "Error: Playwright or Playwright-Stealth not installed. Please run `pip install playwright playwright-stealth && playwright install`."
        except Exception as e:
            return f"Error taking screenshot: {e}"
