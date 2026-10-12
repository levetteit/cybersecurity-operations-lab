# SOC-004 evidence status

This directory currently contains:

- `user-reported-sha256-check.txt`: the ten `OK` lines pasted by the user. This is a verification transcript, **not a SHA256 manifest**.
- `publication-preparation-validation.json`: results from four new synthetic inputs generated on 2026-10-12. These results are **not the user's original Kali result logs**.

The preserved detector source is at [`detections/SOC-004/ssh_detector.py`](../../detections/SOC-004/ssh_detector.py). It was copied verbatim from the user-pasted conversation text; original file-byte identity remains pending.

Original localhost journal exports, the user's synthetic boundary fixtures, their derived outputs, and the existing SHA256 manifest are awaiting upload. No empty placeholders or reconstructed log contents are included. The [investigation report](../../investigations/SOC-004-automated-ssh-detection.md) lists the ten original artifact names and their provenance.

Keep the original loopback SSH journal records distinct from synthetic boundary test logs when adding the approved sanitized files. Record any redaction mapping and compute publication-copy hashes separately from original-file hashes. The PR remains draft pending evidence verification and explicit user approval before merge.
