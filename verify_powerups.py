
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the local file
        filepath = os.path.abspath("index.html")
        page.goto(f"file://{filepath}")

        # Wait for game to run.
        # Since drop rate is low (10%), we might not see one in a short run.
        # But this script primarily tests that the game *starts* and doesn't crash with the new code.
        page.wait_for_timeout(3000)

        # Capture screenshot
        screenshot_path = "/home/jules/verification/powerups_run.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    run()
