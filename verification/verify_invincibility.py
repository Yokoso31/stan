from playwright.sync_api import sync_playwright
import os
import time

def verify_invincibility():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        print("Game loaded.")

        # Helper to get health
        def get_p2_health():
            return page.evaluate("p2.health")

        def is_p2_invincible():
            return page.evaluate("p2.invincible")

        # Initial Setup
        # Move p1 closer
        page.evaluate("p1.x = 660") # p2 is at 700

        start_health = get_p2_health()
        print(f"Start Health P2: {start_health}")

        # 1. P1 hits P2 (Light attack)
        print("P1 attacks P2...")
        page.evaluate("p1.attack(p2, 'light')")

        mid_health = get_p2_health()
        print(f"Health after first hit: {mid_health}")

        if mid_health >= start_health:
             print("FAILURE: P2 should have taken damage.")

        # 2. Check Invincibility
        invincible = is_p2_invincible()
        print(f"P2 Invincible: {invincible}")
        if not invincible:
            print("FAILURE: P2 should be invincible.")
        else:
            print("SUCCESS: P2 is invincible.")

        # 3. P1 hits P2 again immediately
        print("P1 attacks P2 again immediately...")
        # Reset p1 attacking state manually if cooldown is an issue, but we want to simulate rapid attacks
        # The cooldown for p1 attacking is 200ms. We can wait 300ms.
        page.wait_for_timeout(300)
        page.evaluate("p1.attack(p2, 'light')")

        current_health = get_p2_health()
        print(f"Health after second hit (should be same): {current_health}")

        if current_health != mid_health:
            print(f"FAILURE: P2 took damage while invincible. Diff: {mid_health - current_health}")
        else:
            print("SUCCESS: P2 took no damage while invincible.")

        # 4. P2 tries to attack (should fail)
        print("P2 tries to attack while invincible...")
        page.evaluate("p2.attack(p1, 'light')")
        p2_attacking = page.evaluate("p2.attacking")
        print(f"P2 Attacking State: {p2_attacking}")

        if p2_attacking:
            print("FAILURE: P2 should not be able to attack.")
        else:
             print("SUCCESS: P2 cannot attack while invincible.")

        # 5. Wait for invincibility to expire (total 2000ms)
        # We already waited 300ms. Wait another 1800ms to be safe.
        print("Waiting for invincibility to expire...")
        page.wait_for_timeout(1800)

        invincible_after = is_p2_invincible()
        print(f"P2 Invincible after wait: {invincible_after}")

        if invincible_after:
            print("FAILURE: Invincibility did not expire.")
        else:
            print("SUCCESS: Invincibility expired.")

        # 6. Verify P2 can be hit again
        print("P1 attacks P2 again...")
        page.evaluate("p1.attack(p2, 'light')")
        final_health = get_p2_health()
        print(f"Health after expiry hit: {final_health}")

        if final_health >= current_health:
            print("FAILURE: P2 should take damage again.")
        else:
            print("SUCCESS: P2 took damage after invincibility.")

        browser.close()

if __name__ == "__main__":
    verify_invincibility()
