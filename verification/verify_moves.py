
import os
from playwright.sync_api import sync_playwright, expect

def verify_moves():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        file_path = os.path.abspath("index.html")
        page.goto(f"file://{file_path}")

        # Helper to click a square at (x, y)
        def click_square(x, y):
            page.locator(f".square[data-x='{x}'][data-y='{y}']").click()

        def get_square_text(x, y):
            return page.locator(f".square[data-x='{x}'][data-y='{y}']").text_content()

        # 1. Test Pawn Opening (White)
        # White Pawn at (0, 6) -> Move to (0, 4) (Double step)
        print("Testing White Pawn double step...")
        click_square(0, 6) # Select Pawn
        click_square(0, 4) # Move

        # Verify Pawn moved
        expect(page.locator(".square[data-x='0'][data-y='4']")).to_have_text("♙")
        expect(page.locator(".square[data-x='0'][data-y='6']")).to_have_text("") # Empty

        # 2. Test Black Pawn Move
        # Black Pawn at (1, 1) -> Move to (1, 2)
        print("Testing Black Pawn single step...")
        click_square(1, 1)
        click_square(1, 2)

        expect(page.locator(".square[data-x='1'][data-y='2']")).to_have_text("♟")

        # 3. Test Invalid Move (Rook blocked by Pawn)
        # White Rook at (0, 7) cannot move to (0, 5) because Pawn is at (0, 6) (Wait, Pawn moved to 0,4)
        # The Pawn originally at (0,6) moved to (0,4). Square (0,6) is empty.
        # Rook at (0,7). Path to (0,5): Needs (0,6) clear. It is.
        # But (0,5) is empty.
        # Let's try to move Rook to (0, 5).
        print("Testing Rook move through clear path...")
        click_square(0, 7) # Select Rook
        click_square(0, 5) # Move

        expect(page.locator(".square[data-x='0'][data-y='5']")).to_have_text("♖")

        # 4. Test Capture
        # Setup: White Rook at (0,5). Black Pawn at (1,2).
        # Move Black Pawn (1,2) -> (1,3).
        print("Moving Black Pawn...")
        click_square(1, 2)
        click_square(1, 3)

        # Move White Rook (0,5) -> (1,5)
        print("Moving White Rook...")
        click_square(0, 5)
        click_square(1, 5) # Rook is now at (1,5)

        # Move Black Pawn (1,3) -> (1,4)
        print("Moving Black Pawn...")
        click_square(1, 3)
        click_square(1, 4) # Black Pawn is now at (1,4), right above White Pawn at (0,4) no wait, (0,4) is White Pawn. (1,4) is Black Pawn.

        # White Rook is at (1,5). Black Pawn is at (1,4).
        # White Rook captures Black Pawn?
        # Turn is White.
        print("Testing Capture...")
        click_square(1, 5) # Select Rook
        click_square(1, 4) # Capture Black Pawn

        expect(page.locator(".square[data-x='1'][data-y='4']")).to_have_text("♖")

        # 5. Test Knight Jump
        # Reset game first to be clean or continue?
        # Let's reset.
        print("Resetting game...")
        page.get_by_role("button", name="Nouvelle partie").click()

        # White Knight (1, 7) -> (0, 5) (Valid L-shape)
        print("Testing Knight Jump...")
        click_square(1, 7)
        click_square(0, 5)

        expect(page.locator(".square[data-x='0'][data-y='5']")).to_have_text("♘")

        # Take screenshot
        page.screenshot(path="verification/moves_verified.png")
        print("Verification complete.")

        browser.close()

if __name__ == "__main__":
    verify_moves()
