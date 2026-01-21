from playwright.sync_api import sync_playwright
import os
import time

def verify_pistol():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Start game from menu
        page.click("#start-btn")
        print("Game started.")

        # Helper to get health
        def get_p2_health():
            return page.evaluate("p2.health")

        # --- Test 1: Spawn and Collect Pistol ---
        print("\n--- Test 1: Spawn and Collect Pistol ---")

        # Force Pistol Spawn at P1 location
        page.evaluate("p1.x = 300; p1.y = 420;")
        # Set PistolDrop active and position
        page.evaluate("""
            pistolDrop.active = true;
            pistolDrop.x = 290;
            pistolDrop.y = 420;
            pistolDrop.vy = 0;
        """)

        # Update P1 to collect
        page.evaluate("p1.update()")

        has_pistol = page.evaluate("p1.hasPistol")
        ammo = page.evaluate("p1.ammo")

        print(f"Has Pistol: {has_pistol}, Ammo: {ammo}")

        if has_pistol and ammo == 6:
            print("SUCCESS: Pistol collected.")
        else:
            print("FAILURE: Pistol collection failed.")

        # --- Test 2: Shoot Enemy ---
        print("\n--- Test 2: Shoot Enemy ---")

        start_hp = get_p2_health()
        print(f"P2 Start HP: {start_hp}")

        # Move P2 into line of fire
        page.evaluate("p2.x = 600; p2.y = 420;")

        # Shoot (P1 Attack)
        # We need to simulate the attack call
        page.evaluate("p1.attack(p2, 'light')")

        # Verify Ammo Decrease
        ammo_after = page.evaluate("p1.ammo")
        print(f"Ammo after shot: {ammo_after}")
        if ammo_after == 5:
             print("SUCCESS: Ammo decreased.")
        else:
             print("FAILURE: Ammo did not decrease.")

        # Verify Bullet Hit (Need to run update loop for bullet travel)
        # Bullet speed 15. Dist 300. ~20 frames.
        # Let's verify bullet created first
        bullet_count = page.evaluate("bullets.length")
        print(f"Bullets active: {bullet_count}")

        # Advance Frames manually
        for _ in range(30):
             page.evaluate("updateBullets()")

        end_hp = get_p2_health()
        print(f"P2 End HP: {end_hp}")

        if end_hp < start_hp:
             print("SUCCESS: Target hit by bullet.")
        else:
             print("FAILURE: Target miss.")

        browser.close()

if __name__ == "__main__":
    verify_pistol()
