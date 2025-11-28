# demand_simulator.py
import random
import threading
import time

# Global demand factor (imported by pricing.py)
DEMAND_LEVEL = 1.0


def start_demand_simulator():
    """
    Background thread that updates DEMAND_LEVEL every 30 seconds.
    Simulates real-world changing demand.
    """
    def run():
        global DEMAND_LEVEL
        while True:
            DEMAND_LEVEL = random.choice([0.9, 1.0, 1.1, 1.2, 1.3])
            time.sleep(30)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
