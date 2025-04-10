import asyncio
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright

_executor = ThreadPoolExecutor(max_workers=1)

def run_playwright_sync(query: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        url = f"https://www.youtube.com/results?search_query={query}"
        page.goto(url, timeout=10000)
        titles = page.locator("ytd-video-renderer #video-title").all_text_contents()
        browser.close()
        return titles[:5]

async def youtube_search(query: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, run_playwright_sync, query)