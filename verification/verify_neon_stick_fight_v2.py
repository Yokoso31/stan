
import os
from playwright.sync_api import sync_playwright, expect

def test_neon_stick_fight_updates():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Construct absolute path to index.html
        cwd = os.getcwd()
        file_path = f"file://{cwd}/index.html"

        print(f"Loading {file_path}")
        page.goto(file_path)

        # Wait for canvas
        canvas = page.locator("#game")
        expect(canvas).to_be_visible()

        # Press 'e' (attack for P1) and take screenshot to verify attack visual
        page.keyboard.down("e")
        # Wait a bit for frame update
        page.wait_for_timeout(100)

        os.makedirs("verification", exist_ok=True)
        screenshot_path = "verification/neon_stick_fight_v2.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        page.keyboard.up("e")

        browser.close()

if __name__ == "__main__":
    test_neon_stick_fight_updates()
