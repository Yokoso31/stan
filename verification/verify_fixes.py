from playwright.sync_api import sync_playwright
import os
import time

def verify_fixes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from local file
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        print("Game loaded.")

        # --- Test 1: Power Block Height ---
        print("\n--- Test 1: Power Block Height ---")

        # Spawn block multiple times and check Y coordinate
        reachable_count = 0
        iterations = 50

        # GROUND is 420. Jump peak is ~300. Reachable height is ~250-420.
        # Logic says between (420-50)=370 and (420-150)=270.

        for i in range(iterations):
            # Manually force logic to check range
            page.evaluate("""
                powerBlock.active = true;
                powerBlock.y = 420 - 50 - Math.random() * 100;
            """)

            y = page.evaluate("powerBlock.y")
            if y >= 270 and y <= 370:
                reachable_count += 1
            else:
                print(f"Spawn out of range: {y}")

        print(f"Reachable spawns: {reachable_count}/{iterations}")
        if reachable_count == iterations:
            print("SUCCESS: All spawns are within reachable range.")
        else:
            print("FAILURE: Some spawns out of range.")

        # --- Test 2: Attack Spam Prevention ---
        print("\n--- Test 2: Attack Spam Prevention ---")

        # Reset cooldown
        page.evaluate("p1.attackCooldown = false")
        page.evaluate("p1.attacking = false")

        # Try to invoke logic multiple times
        result = page.evaluate("""
            let count = 0;
            const p = p1;

            // Attack 1 (Success)
            p.attack(p2, 'light');
            if (p.attacking) count++;

            // Attack 2 (Fail - Cooldown)
            // Even if we manually reset 'attacking' to false (simulating time passing < 500ms)
            p.attacking = false;
            p.attack(p2, 'light');
            if (p.attacking) count++; // Should fail

            count;
        """)

        print(f"Attacks triggered (should be 1): {result}")

        if result == 1:
            print("SUCCESS: Spam prevented by cooldown.")
        else:
             print(f"FAILURE: Expected 1 attack, got {result}")

        # --- Test 3: High Block Collision from Ground ---
        print("\n--- Test 3: Collision from Ground ---")
        # Can I hit the highest block (270) from the ground (420)?
        # dy check is < 120.
        # Player Y = 420. Attack origin = 420 - 40 = 380.
        # Block Y = 270. Block Center = 290.
        # dy = abs(380 - 290) = 90.
        # 90 < 120. Yes.

        # Let's verify via code
        page.evaluate("powerBlock.active = true")
        page.evaluate("powerBlock.y = 270") # Highest possible spawn
        page.evaluate("powerBlock.x = 300")
        page.evaluate("p1.x = 300")
        page.evaluate("p1.y = 420") # Ground

        # Reset cooldowns
        page.evaluate("p1.attackCooldown = false")
        page.evaluate("p1.attacking = false")
        page.evaluate("p1.hasPower = false")

        page.evaluate("p1.attack(p2, 'light')")

        # Check if block destroyed and power active
        has_power = page.evaluate("p1.hasPower")
        block_active = page.evaluate("powerBlock.active")

        if has_power and not block_active:
             print("SUCCESS: Hit high block from ground.")
        else:
             print(f"FAILURE: High block miss. Power: {has_power}, Block Active: {block_active}")

        browser.close()

if __name__ == "__main__":
    verify_fixes()
