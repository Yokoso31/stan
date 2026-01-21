from playwright.sync_api import sync_playwright
import os
import time

def verify_refinements():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        print("Game loaded.")

        # --- Test 1: Body Collision Collection ---
        print("\n--- Test 1: Body Collision Collection ---")

        # Spawn block exactly where P1 is
        page.evaluate("p1.x = 300")
        page.evaluate("p1.y = 420")
        page.evaluate("powerBlock.active = true")
        page.evaluate("powerBlock.x = 290") # Slightly off center but within body width (40)
        page.evaluate("powerBlock.y = 380") # Within body height

        page.evaluate("p1.update()")

        has_power = page.evaluate("p1.hasPower")
        block_active = page.evaluate("powerBlock.active")

        if has_power and not block_active:
             print("SUCCESS: Power collected by body collision.")
        else:
             print(f"FAILURE: Body collection failed. Power: {has_power}, Active: {block_active}")

        # --- Test 2: Directional Attack ---
        print("\n--- Test 2: Directional Attack ---")

        # Reset
        page.evaluate("p1.hasPower = false")
        page.evaluate("p1.attackCooldown = false")
        page.evaluate("p1.attacking = false")
        page.evaluate("p1.facing = 1") # Facing Right
        page.evaluate("p1.x = 300")

        # Spawn block BEHIND player (Left) BUT outside body collision range
        # P1 X=300. Body Range 40. Attack Range 80.
        # Target dist: 70.
        # Block Center = 230.
        # Block X = 210.

        page.evaluate("powerBlock.active = true")
        page.evaluate("powerBlock.x = 210")
        page.evaluate("powerBlock.y = 380")

        # Verify Body Collision doesn't trigger
        page.evaluate("p1.update()")
        has_power_early = page.evaluate("p1.hasPower")
        if has_power_early:
            print("FAILURE: Body collision triggered too early (Test invalid).")
        else:
            # Attack Light
            page.evaluate("p1.attack(p2, 'light')")

            # Should FAIL to hit because facing wrong way
            has_power = page.evaluate("p1.hasPower")
            if not has_power:
                 print("SUCCESS: Attack behind player did not hit.")
            else:
                 print("FAILURE: Attack behind player hit incorrectly.")

            # Turn around and Attack
            page.evaluate("p1.facing = -1") # Facing Left
            page.evaluate("p1.attackCooldown = false")
            page.evaluate("p1.attacking = false")

            page.evaluate("p1.attack(p2, 'light')")

            has_power = page.evaluate("p1.hasPower")
            if has_power:
                 print("SUCCESS: Attack facing block hit.")
            else:
                 print("FAILURE: Attack facing block missed.")

        browser.close()

if __name__ == "__main__":
    verify_refinements()
