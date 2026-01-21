
import os
from playwright.sync_api import sync_playwright, expect

def test_neon_stick_fight():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Construct absolute path to index.html
        cwd = os.getcwd()
        file_path = f"file://{cwd}/index.html"

        print(f"Loading {file_path}")
        page.goto(file_path)

        # Verify title
        expect(page).to_have_title("Neon Stick Fight")
        print("Title verified")

        # Verify header
        header = page.locator("h1")
        expect(header).to_have_text("⚔️ NEON STICK FIGHT ⚔️")
        print("Header verified")

        # Verify UI elements
        expect(page.locator("#hp1")).to_be_visible()
        expect(page.locator("#hp2")).to_be_visible()
        print("UI verified")

        # Verify Canvas
        canvas = page.locator("#game")
        expect(canvas).to_be_visible()
        print("Canvas verified")

        # Take screenshot
        os.makedirs("verification", exist_ok=True)
        screenshot_path = "verification/neon_stick_fight.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    test_neon_stick_fight()
