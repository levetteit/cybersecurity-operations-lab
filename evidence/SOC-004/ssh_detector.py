
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, deque
import re
import sys
LOG_FILE = (
    Path(sys.argv[1]).expanduser()
    if len(sys.argv) > 1
    else Path.home() / "SOC-004-evidence" / "ssh-repeated-failures.log"
)
THRESHOLD = 3
WINDOW = timedelta(seconds=60)

PATTERN = re.compile(
    r"^(\S+).*?Failed password for "
    r"(\S+) from (\S+) port (\d+) ssh2$"
)


def main():
    if not LOG_FILE.is_file():
        print(f"ERROR: Evidence file not found: {LOG_FILE}")
        return

    events = []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            match = PATTERN.search(line.strip())

            if match:
                timestamp, username, source_ip, port = match.groups()

                events.append({
                    "timestamp": datetime.fromisoformat(timestamp),
                    "username": username,
                    "source_ip": source_ip,
                    "port": int(port)
                })

    events.sort(key=lambda event: event["timestamp"])

    print("SOC-004 | Automated SSH Detection")
    print(f"Events parsed: {len(events)}")
    print(f"Detection threshold: {THRESHOLD} failures / 60 seconds")
    print()

    windows = defaultdict(deque)
    alerted = set()

    for event in events:
        key = (event["source_ip"], event["username"])
        current_time = event["timestamp"]
        window = windows[key]

        while window and current_time - window[0] > WINDOW:
            window.popleft()

        window.append(current_time)

        if len(window) >= THRESHOLD and key not in alerted:
            print("[ALERT] Repeated SSH Authentication Failures")
            print(f"Source IP: {event['source_ip']}")
            print(f"Target user: {event['username']}")
            print(f"Failed attempts: {len(window)}")
            print(f"Window start: {window[0].isoformat()}")
            print(f"Alert time: {current_time.isoformat()}")
            alerted.add(key)

    if not alerted:
        print("[OK] No detection thresholds exceeded.")

    print()
    print(f"Total alerts: {len(alerted)}")


if __name__ == "__main__":
    main()

