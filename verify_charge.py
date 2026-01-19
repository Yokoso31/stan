
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the local file
        filepath = os.path.abspath("index.html")
        page.goto(f"file://{filepath}")

        # Hold Space for > 1 second (60 frames) to trigger Charge and Fire
        page.keyboard.down("Space")
        page.wait_for_timeout(1500) # 1.5 seconds
        page.keyboard.up("Space")

        # Wait a bit for explosion to expand
        page.wait_for_timeout(200)

        # Capture screenshot
        screenshot_path = "/home/jules/verification/charged_shot.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    run()
