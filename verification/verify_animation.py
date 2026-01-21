from playwright.sync_api import sync_playwright
import os
import time

def verify_animation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Start game
        page.click("#start-btn")
        print("Game started.")

        # Helper to get animFrame
        def get_anim_frame():
            return page.evaluate("p1.animFrame")

        # --- Test 1: Animation Logic ---
        print("\n--- Test 1: Animation Logic ---")

        # Initial frame (should be 0 or small)
        f1 = get_anim_frame()
        print(f"Frame 1: {f1}")

        # Wait a bit (Idle animation increments slowly)
        page.wait_for_timeout(200)
        f2 = get_anim_frame()
        print(f"Frame 2 (Idle): {f2}")

        if f2 > f1:
             print("SUCCESS: Idle animation frame increments.")
        else:
             print("FAILURE: Idle animation frame did not increment.")

        # Move P1 (Run animation increments faster)
        page.keyboard.down('q')
        page.wait_for_timeout(200) # Let it animate

        f3 = get_anim_frame()
        print(f"Frame 3 (Run): {f3}")

        # Calculate rates
        idle_rate = f2 - f1
        run_rate = f3 - f2

        print(f"Idle Rate: {idle_rate}")
        print(f"Run Rate: {run_rate}")

        if run_rate > idle_rate:
             print("SUCCESS: Run animation is faster than idle.")
        else:
             print("FAILURE: Run animation speed issue.")

        page.keyboard.up('q')

        browser.close()

if __name__ == "__main__":
    verify_animation()
