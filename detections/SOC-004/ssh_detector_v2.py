"""New offline detector; historical sources and evidence remain unchanged."""
import argparse
from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path
import re
import sys

PATTERN = re.compile(
    r"^(\S+).*?Failed password for (?:invalid user )?"
    r"(\S+) from (\S+) port (\d+) ssh2$"
)
THRESHOLD = 3
WINDOW = timedelta(seconds=60)


def read_events(path):
    events = []
    records = skipped = 0
    with path.open(encoding="utf-8") as source:
        for records, line in enumerate(source, 1):
            match = PATTERN.search(line.strip())
            if not match:
                if "Failed password for " in line:
                    raise ValueError(f"line {records}: unsupported failed-password record")
                skipped += 1
                continue
            timestamp_text, username, source_ip, port = match.groups()
            try:
                timestamp = datetime.fromisoformat(timestamp_text)
            except ValueError as error:
                raise ValueError(f"line {records}: invalid ISO timestamp") from error
            if timestamp.utcoffset() is None:
                raise ValueError(f"line {records}: timestamp requires a UTC offset")
            events.append((timestamp, source_ip, username, int(port)))
    events.sort(key=lambda event: event[0])
    return events, records, skipped


def print_results(events):
    print("SOC-004 | Automated SSH Detection")
    print(f"Events parsed: {len(events)}")
    print(f"Detection threshold: {THRESHOLD} failures / 60 seconds")
    print()
    windows = defaultdict(deque)
    alerted = set()
    for timestamp, source_ip, username, _port in events:
        key = (source_ip, username)
        window = windows[key]
        while window and timestamp - window[0] > WINDOW:
            window.popleft()
        window.append(timestamp)
        if len(window) >= THRESHOLD and key not in alerted:
            print("[ALERT] Repeated SSH Authentication Failures")
            print(f"Source IP: {source_ip}")
            print(f"Target user: {username}")
            print(f"Failed attempts: {len(window)}")
            print(f"Window start: {window[0].isoformat()}")
            print(f"Alert time: {timestamp.isoformat()}")
            alerted.add(key)
    if not alerted:
        print("[OK] No detection thresholds exceeded.")
    print()
    print(f"Total alerts: {len(alerted)}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 log with ISO timestamps including UTC offsets")
    args = parser.parse_args(argv)
    try:
        events, records, skipped = read_events(args.input.expanduser())
    except (OSError, UnicodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(f"Records read: {records}; matched: {len(events)}; skipped: {skipped}", file=sys.stderr)
    print_results(events)
    return 0


if __name__ == "__main__":
    sys.exit(main())
