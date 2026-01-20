
import os
from playwright.sync_api import sync_playwright, expect

def verify_chess():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the local index.html file
        file_path = os.path.abspath("index.html")
        page.goto(f"file://{file_path}")

        # Verify Title
        expect(page).to_have_title("Fortnite Chess")

        # Verify Board exists
        board = page.locator("#board")
        expect(board).to_be_visible()

        # Verify Squares (should be 64)
        squares = page.locator(".square")
        expect(squares).to_have_count(64)

        # Verify Pieces are present (e.g. check for a Rook)
        # The code uses unicode chess pieces.
        # "♜" (black rook) is at (0,0) -> data-x=0 data-y=0
        top_left_square = page.locator(".square[data-x='0'][data-y='0']")
        expect(top_left_square).to_have_text("♜")

        # Verify "Nouvelle partie" button
        reset_button = page.get_by_role("button", name="Nouvelle partie")
        expect(reset_button).to_be_visible()

        # Take a screenshot
        screenshot_path = "verification/chess_game.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_chess()
