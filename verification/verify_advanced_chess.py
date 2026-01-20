
import os
import re
from playwright.sync_api import sync_playwright, expect

def verify_advanced_chess():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        file_path = os.path.abspath("index.html")
        page.goto(f"file://{file_path}")

        # Helper to click square
        def click_sq(x, y):
            page.locator(f".square[data-x='{x}'][data-y='{y}']").click()

        def assert_piece(x, y, char):
            expect(page.locator(f".square[data-x='{x}'][data-y='{y}']")).to_have_text(char)

        print("1. Testing Scholar's Mate (Coup du Berger)...")
        # 1. e4 e5
        click_sq(4, 6); click_sq(4, 4); # White e4
        click_sq(4, 1); click_sq(4, 3); # Black e5

        # 2. Bc4 Nc6
        click_sq(5, 7); click_sq(2, 4); # White Bc4
        click_sq(1, 0); click_sq(2, 2); # Black Nc6

        # 3. Qh5 Nf6
        click_sq(3, 7); click_sq(7, 3); # White Qh5
        click_sq(6, 0); click_sq(5, 2); # Black Nf6?? (Blunder allowing mate)

        # 4. Qxf7#
        click_sq(7, 3); click_sq(5, 1); # Capture f7

        # Check for Checkmate Message
        expect(page.locator("#checkMsg")).to_have_text("☠️")
        expect(page.locator("#status")).to_contain_text("ÉCHEC ET MAT")
        print("Scholar's Mate verified.")

        # Reset
        page.get_by_role("button", name="Nouvelle partie").click()

        print("2. Testing Castling (Petit Roque)...")
        # Clear path for White King Side
        # 1. e4 e5
        click_sq(4, 6); click_sq(4, 4);
        click_sq(4, 1); click_sq(4, 3);

        # 2. Nf3 Nc6
        click_sq(6, 7); click_sq(5, 5);
        click_sq(1, 0); click_sq(2, 2);

        # 3. Bc4 Bc5
        click_sq(5, 7); click_sq(2, 4);
        click_sq(5, 0); click_sq(2, 3);

        # Now White can castle (King e1 -> g1)
        click_sq(4, 7); # Select King

        # Look for move indicator on g1 (6, 7)
        g1 = page.locator(".square[data-x='6'][data-y='7']")
        expect(g1).to_have_class(re.compile(r"move"))

        # Execute Castling
        click_sq(6, 7);

        # Verify positions
        assert_piece(6, 7, "♔") # King on g1
        assert_piece(5, 7, "♖") # Rook on f1
        print("Castling verified.")

        # Reset
        page.get_by_role("button", name="Nouvelle partie").click()

        print("3. Testing Promotion UI...")
        # Cheat to clear path quickly or just play it out?
        # Let's clear board via JS to setup promotion scenario
        page.evaluate("""() => {
            board = [
                ['.','.','.','.','k','.','.','.'],
                ['.','P','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','K','.','.','.']
            ];
            turn = 'white';
            render();
            updateGameState();
        }""")

        # Select Pawn at (1, 1) -> Move to (1, 0)
        click_sq(1, 1);
        click_sq(1, 0);

        # Check Modal
        modal = page.locator("#promotionModal")
        expect(modal).to_be_visible()

        # Click Queen
        page.locator(".promo-piece").first.click() # Usually Queen is first

        # Verify Queen on board
        assert_piece(1, 0, "♕")
        print("Promotion verified.")

        # Screenshot
        page.screenshot(path="verification/advanced_chess.png")

        browser.close()

if __name__ == "__main__":
    verify_advanced_chess()
