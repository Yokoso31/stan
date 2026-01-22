from playwright.sync_api import sync_playwright

def verify_theme_and_sprite():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Open the local file directly
        page.goto("file:///app/index.html")

        # Wait for the game canvas to load
        page.wait_for_selector("#game")

        # Take a screenshot
        page.screenshot(path="/home/jules/verification/neon_sprite_verification.png")
        print("Screenshot saved to /home/jules/verification/neon_sprite_verification.png")

        browser.close()

if __name__ == "__main__":
    verify_theme_and_sprite()
