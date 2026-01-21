from playwright.sync_api import sync_playwright
import os
import time

def verify_azerty():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Start game from menu
        page.click("#start-btn")

        print("Game started.")

        # --- Test 1: Move Left with 'Q' ---
        print("\n--- Test 1: Move Left with 'Q' ---")

        # Press 'q'
        page.keyboard.down('q')

        # Check Velocity
        # Wait a moment for loop to update
        page.wait_for_timeout(50)

        vx = page.evaluate("p1.vx")
        print(f"VX after 'q': {vx}")

        if vx < 0:
             print("SUCCESS: Player moved left with 'q'.")
        else:
             print("FAILURE: Player did not move left with 'q'.")

        page.keyboard.up('q')

        # --- Test 2: Jump with 'Z' ---
        print("\n--- Test 2: Jump with 'Z' ---")

        # Press 'z'
        page.keyboard.down('z')

        # Check Velocity Y
        page.wait_for_timeout(50)

        vy = page.evaluate("p1.vy")
        print(f"VY after 'z': {vy}")

        if vy < 0:
             print("SUCCESS: Player jumped with 'z'.")
        else:
             print("FAILURE: Player did not jump with 'z'.")

        page.keyboard.up('z')

        browser.close()

if __name__ == "__main__":
    verify_azerty()
