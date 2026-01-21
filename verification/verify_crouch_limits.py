from playwright.sync_api import sync_playwright
import os
import time

def verify_crouch_limits():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Start game
        page.click("#start-btn")
        print("Game started.")

        # --- Test 1: Crouch Duration Limit ---
        print("\n--- Test 1: Crouch Duration Limit ---")

        # Press and Hold 's'
        page.keyboard.down('s')

        # Verify crouching initially
        page.wait_for_timeout(100)
        is_crouching = page.evaluate("p1.isCrouching")
        print(f"Initial Crouch: {is_crouching}")
        if not is_crouching:
            print("FAILURE: Did not start crouching.")

        # Wait 1.1s (Limit is 1s)
        print("Waiting 1.1s...")
        page.wait_for_timeout(1100)

        is_crouching_after = page.evaluate("p1.isCrouching")
        print(f"Crouch after 1.1s: {is_crouching_after}")

        if not is_crouching_after:
             print("SUCCESS: Forced stand up after 1s.")
        else:
             print("FAILURE: Still crouching after limit.")

        # --- Test 2: Forced Stand Key Hold Check ---
        print("\n--- Test 2: Hold Key After Force Stand ---")
        # Key is still down. Should not recrouch immediately (due to cooldown and logic).
        page.wait_for_timeout(500)
        is_crouching_hold = page.evaluate("p1.isCrouching")
        if not is_crouching_hold:
             print("SUCCESS: Remained standing while key held.")
        else:
             print("FAILURE: Recrouched while key held.")

        # Release key
        page.keyboard.up('s')

        # --- Test 3: Cooldown Logic ---
        print("\n--- Test 3: Cooldown Logic ---")

        # We released key at ~1.6s from start of crouch.
        # Forced stand happened at 1.0s.
        # Cooldown started at 1.0s (when forced stand happened).
        # Cooldown is 3s. So until 4.0s.
        # Current time approx 1.6s.

        # Try to crouch immediately
        page.keyboard.down('s')
        page.wait_for_timeout(100)
        is_crouching_cd = page.evaluate("p1.isCrouching")
        print(f"Crouch attempt during cooldown: {is_crouching_cd}")

        if not is_crouching_cd:
             print("SUCCESS: Cooldown prevented crouching.")
        else:
             print("FAILURE: Cooldown ignored.")

        page.keyboard.up('s')

        # Wait for cooldown to expire (Need total 3s from stand)
        # We are at ~1.7s since start. Stand was at 1.0s.
        # Need to wait 2.3s + buffer. Let's wait 3s.
        print("Waiting 3s for cooldown...")
        page.wait_for_timeout(3000)

        # Try to crouch again
        page.keyboard.down('s')
        page.wait_for_timeout(100)
        is_crouching_ok = page.evaluate("p1.isCrouching")
        print(f"Crouch attempt after cooldown: {is_crouching_ok}")

        if is_crouching_ok:
             print("SUCCESS: Crouch allowed after cooldown.")
        else:
             print("FAILURE: Crouch blocked after cooldown.")

        page.keyboard.up('s')

        browser.close()

if __name__ == "__main__":
    verify_crouch_limits()
