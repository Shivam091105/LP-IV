
# Detect repeated Wi-Fi authentication failures

MAX_ATTEMPTS = 3

# Simulated Wi-Fi authentication logs
# Format: (Device MAC Address, Authentication Status)
wifi_logs = [
    ("AA:BB:CC:11:22:33", "FAIL"),
    ("DD:EE:FF:44:55:66", "SUCCESS"),
    ("AA:BB:CC:11:22:33", "FAIL"),
    ("AA:BB:CC:11:22:33", "FAIL"),
    ("DD:EE:FF:44:55:66", "SUCCESS"),
    ("11:22:33:44:55:66", "FAIL"),
]

failed_attempts = {}
blocked_devices = set()

for mac, status in wifi_logs:

    # Ignore devices already blocked
    if mac in blocked_devices:
        continue

    if status == "FAIL":
        failed_attempts[mac] = failed_attempts.get(mac, 0) + 1

        print(f"Authentication failed: {mac}")
        print(f"Failed attempts: {failed_attempts[mac]}")

        # Block device after repeated failures
        if failed_attempts[mac] >= MAX_ATTEMPTS:
            blocked_devices.add(mac)
            print(f"ALERT: Suspicious activity detected from {mac}")
            print(f"Device {mac} blocked!\n")

    elif status == "SUCCESS":
        print(f"Authentication successful: {mac}")

print("\n===== SECURITY REPORT =====")

if blocked_devices:
    print("Blocked devices:")
    for mac in blocked_devices:
        print(mac)
else:
    print("No suspicious devices detected.")
