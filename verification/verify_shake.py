
import os
from playwright.sync_api import sync_playwright, expect

def test_neon_stick_fight_shake():
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

        # Execute JS to trigger hit and verify variables
        result = page.evaluate("""() => {
            // Force a hit
            p1.x = p2.x - 40;
            p1.attack(p2);
            return {
                freezeFrames: freezeFrames,
                shake: shake
            };
        }""")

        print(f"Post-hit state: {result}")

        if result['freezeFrames'] != 6:
            raise Exception(f"Expected freezeFrames to be 6, got {result['freezeFrames']}")
        if result['shake'] != 10:
            raise Exception(f"Expected shake to be 10, got {result['shake']}")

        print("Variables verified successfully.")

        # Take screenshot of the shake/freeze frame?
        # It might be subtle, but let's take one.
        os.makedirs("verification", exist_ok=True)
        screenshot_path = "verification/neon_stick_fight_shake.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    test_neon_stick_fight_shake()
