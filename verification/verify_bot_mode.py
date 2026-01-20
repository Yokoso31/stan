import os
import time
import re
from playwright.sync_api import sync_playwright, expect

def test_bot_mode():
    file_path = os.path.abspath("index.html")
    file_url = f"file://{file_path}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(file_url)

        # 1. Verify Buttons Exist
        print("Verifying buttons...")
        pvp_btn = page.get_by_role("button", name="Joueur vs Joueur")
        pve_btn = page.get_by_role("button", name="Joueur vs Bot")

        expect(pvp_btn).to_be_visible()
        expect(pve_btn).to_be_visible()

        # 2. Start PvE Game
        print("Starting PvE Game...")
        pve_btn.click()

        # Verify status is White's turn
        status = page.locator("#status")
        expect(status).to_have_text("Tour : Blanc")

        # 3. Make a White Move (Pawn e2 -> e4)
        # Coordinates: x=4, y=6 (White Pawn) -> x=4, y=4
        print("Making White move...")

        # Select Pawn
        # We use a CSS selector based on data attributes
        white_pawn = page.locator('.square[data-x="4"][data-y="6"]')
        white_pawn.click()

        # Verify it's selected (class contains 'selected')
        expect(white_pawn).to_have_class(re.compile(r"selected"))

        # Click Target Square
        target_square = page.locator('.square[data-x="4"][data-y="4"]')
        target_square.click()

        # 4. Verify Turn Switches to Black
        print("Waiting for turn switch to Black...")
        expect(status).to_have_text("Tour : Noir")

        # 5. Wait for Bot to Move (Turn switches back to White)
        print("Waiting for Bot to move...")
        # The bot has a 500ms delay
        # We wait for the status to become "Tour : Blanc" again
        expect(status).to_have_text("Tour : Blanc", timeout=5000)

        print("Bot moved successfully!")

        # 6. Take Screenshot
        page.screenshot(path="verification/bot_mode.png")
        print("Screenshot saved to verification/bot_mode.png")

        browser.close()

if __name__ == "__main__":
    test_bot_mode()
