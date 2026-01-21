from playwright.sync_api import sync_playwright
import os
import time

def verify_crouch_melee():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Start game
        page.click("#start-btn")
        print("Game started.")

        # Helper to get health
        def get_p1_health():
            return page.evaluate("p1.health")

        # --- Test 1: Crouch Dodge High Attack ---
        print("\n--- Test 1: Crouch Dodge High Attack ---")

        # Force positions
        page.evaluate("p1.x = 400; p1.y = 420;")
        page.evaluate("p2.x = 440; p2.y = 420; p2.facing = -1;")

        # P1 Crouches (Hold Key)
        page.keyboard.down('s')
        page.wait_for_timeout(100) # Wait for state to update

        hp_before = get_p1_health()

        # P2 Attacks (Standing)
        page.evaluate("p2.attack(p1, 'light')")

        page.wait_for_timeout(100)

        hp_after = get_p1_health()
        print(f"HP Before: {hp_before}, HP After: {hp_after}")

        if hp_after == hp_before:
             print("SUCCESS: High attack missed crouching player.")
        else:
             print("FAILURE: High attack hit crouching player.")

        page.keyboard.up('s') # Stand up P1

        # --- Test 2: Crouch Hit Crouch Attack ---
        print("\n--- Test 2: Crouch Hit Crouch Attack ---")

        # Reset cooldown for P2 (important!)
        page.evaluate("p2.attackCooldown = false; p2.attacking = false;")

        # P1 Crouches again
        page.keyboard.down('s')

        # P2 Crouches (Hold Key)
        page.keyboard.down('ArrowDown')
        page.wait_for_timeout(100)

        # Reset Invincibility
        page.evaluate("p1.invincible = false")

        # P2 Attacks (Low)
        page.evaluate("p2.attack(p1, 'light')")

        page.wait_for_timeout(100)

        hp_final = get_p1_health()
        print(f"HP After Low Attack: {hp_final}")

        if hp_final < hp_after:
             print("SUCCESS: Low attack hit crouching player.")
        else:
             print("FAILURE: Low attack missed crouching player.")

        page.keyboard.up('s') # Stand up P1

        # --- Test 3: Low Attack Hits Standing ---
        print("\n--- Test 3: Low Attack Hits Standing ---")

        # Reset cooldown for P2
        page.evaluate("p2.attackCooldown = false; p2.attacking = false;")

        # P1 is standing (key up)
        page.wait_for_timeout(100)
        page.evaluate("p1.invincible = false")

        # P2 is still crouching (key down)

        # P2 Attacks (Low)
        page.evaluate("p2.attack(p1, 'light')")

        page.wait_for_timeout(100)

        hp_standing = get_p1_health()
        print(f"HP Standing After Low Attack: {hp_standing}")

        if hp_standing < hp_final:
             print("SUCCESS: Low attack hit standing player.")
        else:
             print("FAILURE: Low attack missed standing player.")

        page.keyboard.up('ArrowDown')

        browser.close()

if __name__ == "__main__":
    verify_crouch_melee()
