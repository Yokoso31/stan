
from playwright.sync_api import sync_playwright, expect
import os

def test_antichess_rules():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        def click_square(x, y):
            page.locator(f".square[data-x='{x}'][data-y='{y}']").click()
            page.wait_for_timeout(100) # Wait for JS

        def is_move(x, y):
            classes = page.locator(f".square[data-x='{x}'][data-y='{y}']").get_attribute("class")
            return "move" in classes

        def reset_and_setup(board_setup):
            page.evaluate(f"""() => {{
                console.log("Resetting State...");
                gameOver = false;
                selectedSquare = null;
                promoting = null;
                enPassantTarget = null;
                board = {board_setup};
                turn = 'white'; // Default, override if needed in setup
                // Check if turn needs to be black
                if (arguments[0] && arguments[0].turn) turn = arguments[0].turn;

                updateGameState();
                render();
            }}""")

        print("--- TEST 1: Mandatory Capture ---")
        page.evaluate("""() => {
            gameOver = false; selectedSquare = null; promoting = null; enPassantTarget = null;
            board = [
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','p','.','.'], // 5,3
                ['.','.','.','.','P','.','.','.'], // 4,4
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['R','.','.','.','.','.','.','.']  // 0,7
            ];
            turn = 'white';
            updateGameState();
            render();
        }""")

        click_square(0, 7)
        assert not is_move(0, 6), "Rook should not be able to move"
        click_square(4, 4)
        assert is_move(5, 3), "Pawn capture move should be available"
        click_square(5, 3)
        print("Test 1 Passed.")

        print("--- TEST 2: King Capture ---")
        page.evaluate("""() => {
            gameOver = false; selectedSquare = null; promoting = null; enPassantTarget = null;
            board = [
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['k','.','.','.','.','.','.','.'], // 0,5
                ['.','.','.','.','.','.','.','.'],
                ['R','.','.','.','.','.','.','.']  // 0,7
            ];
            turn = 'white';
            updateGameState();
            render();
        }""")

        click_square(0, 7)
        assert is_move(0, 5), "King should be capturable"
        click_square(0, 5)
        print("Test 2 Passed.")

        print("--- TEST 3: Win Condition ---")
        page.evaluate("""() => {
            gameOver = false; selectedSquare = null; promoting = null; enPassantTarget = null;
            board = [
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['.','.','.','.','.','.','.','.'],
                ['P','.','.','.','.','.','.','.'], // 0,6
                ['r','.','.','.','.','.','.','.']  // 0,7
            ];
            turn = 'black';
            updateGameState();
            render();
        }""")

        click_square(0, 7)
        click_square(0, 6)

        status_text = page.locator("#status").inner_text()
        print(f"Game Status: {status_text}")
        assert "VICTOIRE" in status_text, "Game should be over"
        assert "Blancs gagnent" in status_text, "White should win (0 pieces)"
        print("Test 3 Passed.")

        page.screenshot(path="verification/antichess.png")
        browser.close()

if __name__ == "__main__":
    test_antichess_rules()
