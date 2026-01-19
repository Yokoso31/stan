
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the local file
        filepath = os.path.abspath("index.html")
        page.goto(f"file://{filepath}")

        # Wait a bit for the canvas to render
        page.wait_for_timeout(1000)

        # Capture screenshot
        screenshot_path = "/home/jules/verification/horror_theme.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    run()
