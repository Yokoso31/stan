import asyncio
from playwright.async_api import async_playwright
import os

async def verify_boss():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the game
        file_path = os.path.abspath("index.html")
        await page.goto(f"file://{file_path}")

        # Force level 2 (Boss Level)
        print("Forcing Level 2...")
        await page.evaluate("level = 1; nextLevel();")

        # Wait for Boss initialization (checking if 'boss' variable is not null)
        # We can also check if the canvas has specific Boss pixels, but checking state is easier.
        is_boss_active = await page.evaluate("!!boss")
        print(f"Boss active: {is_boss_active}")

        if not is_boss_active:
             print("Boss failed to spawn.")
             await browser.close()
             return

        # Wait a bit for boss to render
        await asyncio.sleep(1)

        # Take screenshot
        os.makedirs("verification", exist_ok=True)
        screenshot_path = "verification/boss_fight.png"
        await page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_boss())
