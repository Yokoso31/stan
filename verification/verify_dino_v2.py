
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

        score = page.locator("#score")
        expect(score).to_be_visible()
        expect(score).to_contain_text("Score: 0")

        # Wait for the obstacle to be created and move a bit
        page.wait_for_timeout(1000)

        # Check if an obstacle exists
        obstacle = page.locator(".obstacle")
        expect(obstacle.first).to_be_visible()

        # Capture screenshot
        screenshot_path = "/home/jules/verification/dino_game_initial_v2.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    run()
