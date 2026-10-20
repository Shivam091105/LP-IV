
import logging
from collections import defaultdict
from datetime import datetime, timedelta

# Configure logging to store events in a file
logging.basicConfig(
    filename="system.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True
)

# Simulated system events
events = [
    ("192.168.1.10", "LOGIN_FAILED"),
    ("192.168.1.20", "LOGIN_SUCCESS"),
    ("192.168.1.10", "LOGIN_FAILED"),
    ("192.168.1.10", "LOGIN_FAILED"),
    ("192.168.1.20", "FILE_ACCESS"),
    ("192.168.1.30", "LOGIN_FAILED")
]

# Capture and store events
for ip, event in events:
    if event == "LOGIN_FAILED":
        logging.warning("%s | %s", ip, event)
    else:
        logging.info("%s | %s", ip, event)

print("Events captured and saved in system.log")

# Read log file and correlate failed login events
failed_attempts = defaultdict(list)

with open("system.log", "r", encoding="utf-8") as file:
    for line in file:
        parts = line.strip().split(" | ", 3)

        if len(parts) != 4:
            continue

        timestamp_text, severity, ip, event = parts

        if event == "LOGIN_FAILED":
            timestamp = datetime.strptime(
                timestamp_text, "%Y-%m-%d %H:%M:%S"
            )
            failed_attempts[ip].append(timestamp)

# Detect repeated failures within a time window
threshold = 3
time_window = timedelta(minutes=5)

print("\n===== SECURITY ALERTS =====")

alert_found = False

for ip, timestamps in failed_attempts.items():
    timestamps.sort()

    for i in range(len(timestamps)):
        count = 0

        for j in range(i, len(timestamps)):
            if timestamps[j] - timestamps[i] <= time_window:
                count += 1
            else:
                break

        if count >= threshold:
            print(
                f"ALERT: {ip} has {count} failed login attempts "
                f"within 5 minutes!"
            )
            alert_found = True
            break

if not alert_found:
    print("No suspicious activity detected.")

print("\nCheck system.log for recorded events.")
