from playwright.sync_api import sync_playwright
import os
import time

def verify_power_block():
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

        def is_p1_powered():
            return page.evaluate("p1.hasPower")

        # 1. Force spawn the Power Block at a specific location reachable by P1
        print("Forcing Power Block spawn...")
        page.evaluate("powerBlock.active = true")
        page.evaluate("powerBlock.x = 330") # P1 is at 300
        page.evaluate("powerBlock.y = 350") # P1 y is GROUND (420). 420-70 = 350.

        # 2. P1 attacks the block
        print("P1 attacking the block...")
        page.evaluate("p1.attack(p2, 'light')") # Target doesn't matter for block hit

        # Wait a moment for logic AND cooldown (attack lasts 200ms)
        page.wait_for_timeout(300)

        # 3. Verify P1 has power
        powered = is_p1_powered()
        print(f"P1 Powered: {powered}")

        if not powered:
             print("FAILURE: P1 did not get power.")
        else:
             print("SUCCESS: P1 got power.")

        # 4. Verify Power Block is gone
        block_active = page.evaluate("powerBlock.active")
        if block_active:
             print("FAILURE: Block should be inactive.")
        else:
             print("SUCCESS: Block destroyed.")

        # 5. P1 hits P2 with Power (Light attack normally 5, with power should be 10)
        start_health = get_p2_health()
        print(f"P2 Start Health: {start_health}")

        print("P1 attacks P2 with Power...")
        page.evaluate("p1.x = 660") # Move close to p2 (700)
        # Force invincibility off just in case
        page.evaluate("p2.invincible = false")

        page.evaluate("p1.attack(p2, 'light')")

        # Wait for frame update
        page.wait_for_timeout(100)

        mid_health = get_p2_health()
        damage = start_health - mid_health
        print(f"Damage dealt: {damage}")

        if damage != 10:
             print(f"FAILURE: Expected 10 damage, got {damage}")
        else:
             print("SUCCESS: Double damage applied.")

        # 6. Wait for power to expire (5000ms)
        # We already waited ~400ms. Wait 4700ms more.
        print("Waiting for power to expire...")
        page.wait_for_timeout(5000)

        powered_after = is_p1_powered()
        print(f"P1 Powered after wait: {powered_after}")

        if powered_after:
             print("FAILURE: Power did not expire.")
        else:
             print("SUCCESS: Power expired.")

        # 7. Check damage returns to normal
        print("P1 attacks P2 normal...")
        # Reset cooldown and invincibility
        page.evaluate("p1.attacking = false")
        page.evaluate("p2.invincible = false")

        page.evaluate("p1.attack(p2, 'light')")

        # Wait for frame update
        page.wait_for_timeout(100)

        final_health = get_p2_health()
        damage_normal = mid_health - final_health
        print(f"Normal damage: {damage_normal}")

        if damage_normal != 5:
             print(f"FAILURE: Expected 5 damage, got {damage_normal}")
        else:
             print("SUCCESS: Damage returned to normal.")

        browser.close()

if __name__ == "__main__":
    verify_power_block()
