import asyncio
from playwright.async_api import async_playwright
import os

async def verify_cheat():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the game
        file_path = os.path.abspath("index.html")
        await page.goto(f"file://{file_path}")

        # Wait for game to initialize
        await asyncio.sleep(1)

        # Initial check
        is_invincible = await page.evaluate("player.invincible")
        print(f"Initial Invincible: {is_invincible}")
        if is_invincible:
            print("Error: Player started invincible.")
            return

        # Simulate Cheat Code: Hold Ctrl + type "azerty"
        # We need to be careful with modifiers in playwright.

        # Method 1: dispatch events manually
        cheat_keys = ['a', 'z', 'e', 'r', 't', 'y']

        # Press Control down
        await page.keyboard.down("Control")

        for key in cheat_keys:
            await page.keyboard.press(key)
            await asyncio.sleep(0.1) # small delay

        # Release Control
        await page.keyboard.up("Control")

        # Check result
        is_invincible = await page.evaluate("player.invincible")
        print(f"After Cheat Code: {is_invincible}")

        if not is_invincible:
            print("Cheat code failed to activate.")
            await browser.close()
            return

        # Take screenshot of Gold Player
        os.makedirs("verification", exist_ok=True)
        screenshot_path = "verification/god_mode.png"
        await page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_cheat())
