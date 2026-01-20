
from playwright.sync_api import sync_playwright, expect

def test_chaos_mode():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load local file
        import os
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Helper to get board state
        def get_board_state():
            squares = page.query_selector_all(".square")
            state = {}
            for sq in squares:
                x = sq.get_attribute("data-x")
                y = sq.get_attribute("data-y")
                text = sq.inner_text()
                state[f"{x},{y}"] = text
            return state

        initial_state = get_board_state()
        print("Initial Board captured.")

        # Trigger Chaos Mode: Shift + A, Z, E
        page.keyboard.down("Shift")
        page.keyboard.press("a")
        page.keyboard.press("z")
        page.keyboard.press("e")
        page.keyboard.up("Shift")

        # Wait a bit for potential rendering
        page.wait_for_timeout(500)

        new_state = get_board_state()
        print("New Board captured.")

        # Verify Kings did NOT move
        # Kings are initially at 4,7 (White K) and 4,0 (Black k)
        # Unicode chars: K=♔, k=♚
        # However, text content depends on the PIECES map.
        # PIECES = { k:"♚", K:"♔" ... }

        white_king_pos = "4,7"
        black_king_pos = "4,0"

        assert initial_state[white_king_pos] == "♔", "White King should start at 4,7"
        assert initial_state[black_king_pos] == "♚", "Black King should start at 4,0"

        assert new_state[white_king_pos] == "♔", "White King should NOT move"
        assert new_state[black_king_pos] == "♚", "Black King should NOT move"
        print("Kings remained in place.")

        # Verify board actually changed
        # It's statistically impossible for a shuffle of 62 items to remain identical
        differences = 0
        for key in initial_state:
            if key in [white_king_pos, black_king_pos]:
                continue
            if initial_state[key] != new_state[key]:
                differences += 1

        print(f"Number of squares changed: {differences}")
        assert differences > 0, "Board did not change after Chaos Mode!"

        # Take screenshot
        page.screenshot(path="verification/chaos_mode.png")
        print("Screenshot saved.")

        browser.close()

if __name__ == "__main__":
    test_chaos_mode()
