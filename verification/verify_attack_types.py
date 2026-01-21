from playwright.sync_api import sync_playwright
import os

def verify_attack_types():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from local file
        # Assuming index.html is in the current working directory
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        print("Game loaded.")

        # Helper to get health
        def get_p2_health():
            return page.evaluate("p2.health")

        # Initial health
        start_health = get_p2_health()
        print(f"Start Health P2: {start_health}")

        # 1. Test Light Attack (expect 5 damage)
        print("Executing Light Attack...")
        # Ensure p1 is close enough to p2.
        # p1 x=300, p2 x=700. Distance = 400. Range is 50.
        # We need to move them closer or force attack to hit by setting positions.
        page.evaluate("p1.x = 660") # p2 is at 700. Dist 40 < 50.
        page.evaluate("p1.attack(p2, 'light')")

        # Wait a bit for potential frame updates if needed, though logic is immediate
        # But health update happens in the attack call synchronously.
        mid_health = get_p2_health()
        damage_light = start_health - mid_health
        print(f"Light Attack Damage: {damage_light}")

        if damage_light != 5:
            print(f"FAILURE: Expected 5 damage, got {damage_light}")
        else:
            print("SUCCESS: Light attack correct.")

        # Wait for cooldown (200ms)
        page.wait_for_timeout(300)

        # 2. Test Heavy Attack (expect 15 damage)
        print("Executing Heavy Attack...")
        page.evaluate("p1.attack(p2, 'heavy')")

        end_health = get_p2_health()
        damage_heavy = mid_health - end_health
        print(f"Heavy Attack Damage: {damage_heavy}")

        if damage_heavy != 15:
            print(f"FAILURE: Expected 15 damage, got {damage_heavy}")
        else:
            print("SUCCESS: Heavy attack correct.")

        browser.close()

if __name__ == "__main__":
    verify_attack_types()
