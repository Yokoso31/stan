from playwright.sync_api import sync_playwright
import os
import time

def verify_new_powers():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        print("Game loaded.")

        # Helper to get health
        def get_p1_health():
            return page.evaluate("p1.health")

        # --- Test 1: Health Power ---
        print("\n--- Test 1: Health Power ---")

        # Reduce P1 health
        page.evaluate("p1.health = 50")
        print(f"Start HP: {get_p1_health()}")

        # Spawn Health Block at P1
        page.evaluate("p1.x = 300; p1.y = 420;")
        page.evaluate("""
            powerBlock.active = true;
            powerBlock.type = 'health';
            powerBlock.x = 290;
            powerBlock.y = 380;
        """)

        # Collect via body
        page.evaluate("p1.update()")

        current_hp = get_p1_health()
        print(f"HP after Heal: {current_hp}")

        if current_hp == 80:
             print("SUCCESS: Health increased by 30.")
        else:
             print(f"FAILURE: Health mismatch. Expected 80, got {current_hp}")

        # --- Test 2: Shield Power ---
        print("\n--- Test 2: Shield Power ---")

        # Spawn Shield Block
        page.evaluate("""
            powerBlock.active = true;
            powerBlock.type = 'shield';
            powerBlock.x = 290;
            powerBlock.y = 380;
        """)

        # Collect
        page.evaluate("p1.update()")

        has_shield = page.evaluate("p1.hasShield")
        print(f"Has Shield: {has_shield}")
        if not has_shield:
            print("FAILURE: Shield not acquired.")

        # Get Hit by P2
        print("P2 Attacks P1 with Shield...")
        page.evaluate("p2.x = 340") # Close to P1 (300)
        page.evaluate("p2.facing = -1")
        page.evaluate("p2.attack(p1, 'light')")

        # Check damage and shield status
        final_hp = get_p1_health()
        shield_after = page.evaluate("p1.hasShield")

        print(f"Final HP: {final_hp}")
        print(f"Shield After: {shield_after}")

        if final_hp == 80 and not shield_after:
             print("SUCCESS: Shield absorbed damage and broke.")
        elif final_hp < 80:
             print("FAILURE: P1 took damage.")
        elif shield_after:
             print("FAILURE: Shield did not break.")

        browser.close()

if __name__ == "__main__":
    verify_new_powers()
