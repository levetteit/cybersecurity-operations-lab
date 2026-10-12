"""Deterministic new synthetic fixtures, never recovered historical inputs."""
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = datetime(2000, 1, 1, tzinfo=timezone.utc)
DEFAULT_PAIR = ("127.0.0.1", "test-analyst")
# Each entry: offset seconds, source IP, username. Input order is significant.
CASES = {
    "within-window": [(x, *DEFAULT_PAIR) for x in (0, 30, 59)],
    "below-threshold-in-window": [(x, *DEFAULT_PAIR) for x in (0, 30)],
    "outside-window": [(x, *DEFAULT_PAIR) for x in (0, 30, 61)],
    "exact-boundary": [(x, *DEFAULT_PAIR) for x in (0, 30, 60)],
    "separate-pairs": [(0, "127.0.0.1", "test-analyst"), (10, "127.0.0.2", "test-analyst"), (20, "127.0.0.1", "other-user")],
    "unsorted": [(x, *DEFAULT_PAIR) for x in (59, 0, 30)],
    "two-bursts-one-alert": [(x, *DEFAULT_PAIR) for x in (0, 10, 20, 120, 130, 140)],
}
# Independent expectations; do not compute them by calling a detector.
ALERT_AT = {"within-window": 59, "exact-boundary": 60, "unsorted": 59, "two-bursts-one-alert": 20}


def fixture_bytes():
    files = {}
    for name, events in CASES.items():
        lines = [f"{(BASE + timedelta(seconds=offset)).isoformat()} synthetic-lab sshd[1000]: Failed password for {user} from {ip} port 40000 ssh2\n" for offset, ip, user in events]
        files[f"{name}.log"] = "".join(lines).encode()
        output = f"SOC-004 | Automated SSH Detection\nEvents parsed: {len(events)}\nDetection threshold: 3 failures / 60 seconds\n\n"
        if name in ALERT_AT:
            output += "[ALERT] Repeated SSH Authentication Failures\nSource IP: 127.0.0.1\nTarget user: test-analyst\nFailed attempts: 3\n"
            output += f"Window start: {BASE.isoformat()}\nAlert time: {(BASE + timedelta(seconds=ALERT_AT[name])).isoformat()}\n\nTotal alerts: 1\n"
        else:
            output += "[OK] No detection thresholds exceeded.\n\nTotal alerts: 0\n"
        files[f"{name}.expected.txt"] = output.encode()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "fixtures")
    parser.add_argument("--check", action="store_true", help="Compare preserved bytes without writing")
    args = parser.parse_args()
    files = fixture_bytes()
    if args.check:
        mismatches = [name for name, content in files.items() if not (args.output_dir / name).is_file() or (args.output_dir / name).read_bytes() != content]
        if mismatches:
            raise SystemExit(f"Fixture mismatch: {', '.join(mismatches)}")
        print(f"PASS: {len(files)} deterministic fixture/expectation files")
    else:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, content in files.items():
            (args.output_dir / name).write_bytes(content)
        print(f"Wrote {len(files)} new synthetic files to {args.output_dir}")


if __name__ == "__main__":
    main()
