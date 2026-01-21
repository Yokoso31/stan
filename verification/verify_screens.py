from playwright.sync_api import sync_playwright
import os
import time

def verify_screens():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        print("Game loaded.")

        # --- Test 1: Start Screen Elements ---
        print("\n--- Test 1: Start Screen ---")

        # Check title - Use specific selector for Menu title
        if page.is_visible("#start-screen h1"):
            print("Title visible.")
        else:
             print("FAILURE: Title not found.")

        # Check Color Pickers
        if page.is_visible("#p1-color") and page.is_visible("#p2-color"):
             print("Color pickers visible.")
        else:
             print("FAILURE: Color pickers missing.")

        # Check Play Button
        if page.is_visible("#start-btn"):
             print("Start button visible.")
        else:
             print("FAILURE: Start button missing.")

        # --- Test 2: Change Color and Start ---
        print("\n--- Test 2: Change Color and Start ---")

        # Change P1 Color to Red (#ff0000)
        page.fill("#p1-color", "#ff0000")
        page.dispatch_event("#p1-color", "input")

        # Click Play
        page.click("#start-btn")

        # Check Game State (UI should be visible, Start Screen hidden)
        if page.is_visible("#ui") and not page.is_visible("#start-screen"):
             print("Game started (UI visible).")
        else:
             print("FAILURE: Game start transition failed.")

        # Check P1 Color in game logic
        p1_color = page.evaluate("p1.color")
        print(f"P1 Color: {p1_color}")

        if p1_color == "#ff0000":
             print("SUCCESS: P1 Color updated.")
        else:
             print(f"FAILURE: P1 Color mismatch. Expected #ff0000, got {p1_color}")

        # --- Test 3: Game Over ---
        print("\n--- Test 3: Game Over ---")

        # Force P2 death
        page.evaluate("p2.health = 0")
        # Trigger loop update (wait a bit)
        page.wait_for_timeout(100)

        # Check Game Over Screen
        if page.is_visible("#game-over-screen"):
             print("Game Over screen visible.")
        else:
             print("FAILURE: Game Over screen not shown.")

        # Check Winner Text
        winner_text = page.inner_text("#winner-text")
        print(f"Winner Text: {winner_text}")

        if "PLAYER 1 WINS" in winner_text:
             print("SUCCESS: Winner text correct.")
        else:
             print("FAILURE: Winner text incorrect.")

        # --- Test 4: Restart ---
        print("\n--- Test 4: Restart ---")

        page.click("#restart-btn")

        # Should be back to Menu
        if page.is_visible("#start-screen"):
             print("Returned to Menu.")
        else:
             print("FAILURE: Did not return to menu.")

        # Check Reset Health (Now that resetGame is called)
        p2_health = page.evaluate("p2.health")
        if p2_health == 100:
             print("SUCCESS: Health reset.")
        else:
             print(f"FAILURE: Health not reset. Got {p2_health}")

        browser.close()

if __name__ == "__main__":
    verify_screens()
