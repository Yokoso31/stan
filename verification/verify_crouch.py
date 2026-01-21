from playwright.sync_api import sync_playwright
import os
import time

def verify_crouch():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Start game from menu
        page.click("#start-btn")

        print("Game started.")

        # --- Test 1: Crouch State ---
        print("\n--- Test 1: Crouch State ---")

        # Press 's' (P1 Crouch)
        page.keyboard.down('s')
        page.wait_for_timeout(100) # Wait for game loop to process

        is_crouching = page.evaluate("p1.isCrouching")
        height = page.evaluate("p1.height")

        print(f"Is Crouching: {is_crouching}")
        print(f"Height: {height}")

        if is_crouching and height == 35:
             print("SUCCESS: Crouch state active and height reduced.")
        else:
             print("FAILURE: Crouch state or height incorrect.")

        # --- Test 2: Disable Movement while Crouching ---
        print("\n--- Test 2: Disable Movement ---")

        # Keep holding 's', press 'd' (Right)
        page.keyboard.down('d')
        page.wait_for_timeout(100)

        vx = page.evaluate("p1.vx")
        print(f"VX while crouching and moving: {vx}")

        if vx == 0:
             print("SUCCESS: Movement disabled while crouching.")
        else:
             print("FAILURE: Moved while crouching.")

        page.keyboard.up('d')

        # --- Test 3: Bullet Dodge ---
        print("\n--- Test 3: Bullet Dodge ---")

        # Setup: P1 crouches. P2 has pistol and shoots.
        # Give P2 pistol
        page.evaluate("p2.hasPistol = true; p2.ammo = 10;")
        # Position P2
        page.evaluate("p2.x = 600; p2.y = 420; p2.facing = -1;")
        # Position P1
        page.evaluate("p1.x = 400; p1.y = 420;")

        # Verify P1 HP before
        hp_before = page.evaluate("p1.health")

        # Ensure crouch is still held
        page.keyboard.down('s')
        page.wait_for_timeout(100)

        # P2 Shoot
        page.evaluate("p2.attack(p1, 'light')")

        # Wait for bullet (natural game loop)
        # 15px/frame. 200px distance. ~14 frames.
        page.wait_for_timeout(500)

        hp_after = page.evaluate("p1.health")
        print(f"HP Before: {hp_before}, HP After: {hp_after}")

        if hp_after == hp_before:
             print("SUCCESS: Bullet missed crouching player.")
        else:
             print("FAILURE: Bullet hit crouching player.")

        # Stand Up
        page.keyboard.up('s')
        page.wait_for_timeout(200) # Wait for state update

        # Verify Bullet Hit when Standing (Control Test)
        print("\n--- Control Test: Bullet Hit Standing ---")

        # Verify P1 is standing
        height_stand = page.evaluate("p1.height")
        if height_stand != 80:
            print(f"FAILURE: Player did not stand up. Height: {height_stand}")
        else:
            print("Player stood up.")

        page.evaluate("p2.attack(p1, 'light')")

        # Wait for bullet
        page.wait_for_timeout(500)

        hp_final = page.evaluate("p1.health")
        print(f"HP After Stand Shot: {hp_final}")

        if hp_final < hp_after:
             print("SUCCESS: Bullet hit standing player.")
        else:
             print("FAILURE: Bullet missed standing player.")

        browser.close()

if __name__ == "__main__":
    verify_crouch()
