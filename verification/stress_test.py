
from playwright.sync_api import sync_playwright
import os
import time

def stress_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))

        url = f"file://{os.path.abspath('index.html')}"
        page.goto(url)

        print("Starting Robust Stress Test...")

        page.evaluate("""
            window.stressTestParams = { moves: 0 };
            window.onerror = function(message, source, lineno, colno, error) {
                console.error("GLOBAL ERROR: " + message);
            };
            window.onunhandledrejection = function(event) {
                console.error("UNHANDLED REJECTION: " + event.reason);
            };

            // Override global variables
            window.gameMode = 'pve';
            window.humanColor = 'spectator';

            const originalExecuteMove = window.executeMove;
            window.executeMove = (move) => {
                window.stressTestParams.moves++;
                console.log(`Move ${window.stressTestParams.moves}: ${move.piece} (${window.turn}) to ${move.to.x},${move.to.y}`);
                originalExecuteMove(move);
            };

            // Speed up slightly but keeping async nature
            const originalSetTimeout = window.setTimeout;
            window.setTimeout = (fn, delay) => {
                // Force delay to be small
                originalSetTimeout(fn, 50);
            };

            // Set difficulty to medium to stress 'saveState/restoreState' loop
            document.getElementById('botDifficulty').value = 'medium';

            // Random Chaos
            setInterval(() => {
                if (!window.gameOver && Math.random() < 0.3) {
                    console.log("Triggering CHAOS MODE...");
                    window.activateChaosMode();
                }
            }, 2000);

            // Auto restart
            setInterval(() => {
                if (window.gameOver) {
                    console.log('Game Over. Restarting...');
                    window.initGame('pve');
                    window.humanColor = 'spectator';
                    window.playBot();
                }
            }, 1000);

            // Start
            console.log('Triggering Bot...');
            window.initGame('pve');
            window.humanColor = 'spectator';
            window.playBot();
        """)

        start_time = time.time()
        while time.time() - start_time < 30:
            time.sleep(1)

        print("Stress Test Finished.")
        browser.close()

if __name__ == "__main__":
    stress_test()
