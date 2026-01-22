
from playwright.sync_api import sync_playwright, expect
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the local file
        filepath = os.path.abspath("index.html")
        page.goto(f"file://{filepath}")

        # Check title
        expect(page).to_have_title("Dino Game HTML5")

        # Check if dino and score exist
        dino = page.locator("#dino")
        expect(dino).to_be_visible()

        # Capture screenshot
        screenshot_path = "/home/jules/verification/real_dino_check.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    run()
