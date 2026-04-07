import json
from datetime import datetime
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "attacks.json")

def log_attack(prompt, reason):
    entry = {
        "time": str(datetime.now()),
        "prompt": prompt,
        "reason": reason
    }

    # Ensure logs folder exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Ensure file exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    # Read existing logs
    with open(LOG_FILE, "r") as f:
        try:
            data = json.load(f)
        except:
            data = []

    data.append(entry)

    # Write logs
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)