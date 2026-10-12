# SOC-004 — Automated SSH Authentication Failure Detection

**Status:** Completed controlled exercise; publication retained as a draft PR for user review  
**Investigation type:** Linux SSH journal analysis and Python detection validation  
**Environment:** Kali Linux VM `kali-soc-lab`, lab account `analyst`, localhost `127.0.0.1`  
**Disposition:** Authorized lab activity; no confirmed real-world security incident  
**Evidence basis:** Ten transferred source/log/result files, their original SHA256 manifest, the exact user-pasted detector source, and independently reproduced results.

## Objective and scope

Detect at least three SSH password failures for the same source IP and target username within an inclusive 60-second sliding window. Validate the positive, negative, outside-window, and exact-boundary scenarios while keeping original localhost journal evidence distinct from synthetic tests.

The reviewed exports represent a personally controlled lab. A detector alert establishes that the configured failure pattern was present in its input; it does not establish successful access or compromise.

## Collection, preservation, and publication handling

The user transferred the existing `SOC-004-evidence` directory from Kali through a temporary VirtualBox shared folder. The ten artifacts named in the supplied `SHA256SUMS.txt` were hashed independently using `hashlib.sha256` over their raw bytes: **10 of 10 matched**. The underlying live journal and original collection commands were not independently inspected.

The supplied source, nine log/result files, and manifest are preserved byte-for-byte in [`evidence/SOC-004/`](../evidence/SOC-004/README.md). The manifest remains unchanged and uses the original filenames relative to that directory. The transferred compiled Python cache is not part of the evidence manifest and is excluded from publication.

Review of the supplied excerpts found the established lab hostname/account and loopback addresses, with no password values, credentials, or non-loopback source addresses. No additional redaction was necessary for the approved publication copies. No file text was rewritten, and the earlier sanitization or export history is not independently authenticated.

Hash matching confirms that the transferred bytes agree with the supplied manifest. It does not authenticate the original journal acquisition or prove an unbroken chain of custody before transfer.

## Detector source and behavior

The runnable [detector under `detections/SOC-004/`](../detections/SOC-004/ssh_detector.py) remains the **exact text pasted by the user**. The [transferred original `ssh_detector.py`](../evidence/SOC-004/ssh_detector.py) is also preserved with the evidence, so its original manifest entry can be verified without modifying paths or file bytes.

The transferred source equals one leading LF byte, the exact pasted text, and two trailing LF bytes. There are no other differences. Both source copies passed syntax compilation and produced the same results on all four original scenario inputs. The separate copies preserve the chat source and the original file's hash without changing either.

The detector:

- Reads the first command-line argument as an input path, or defaults to `~/SOC-004-evidence/ssh-repeated-failures.log`.
- Matches timestamped lines ending in `Failed password for <username> from <source_ip> port <port> ssh2`.
- Parses timestamps, sorts events, and maintains a deque per `(source_ip, username)`.
- Removes timestamps only when their age is **greater than 60 seconds**. An event exactly 60 seconds old remains in the window.
- Emits an alert at three retained failures and at most one alert per source-IP/username pair per invocation.

## Evidence inventory and provenance

| Artifact | Role and provenance |
| --- | --- |
| [`ssh-first-failure.log`](../evidence/SOC-004/ssh-first-failure.log) | Original localhost SSH journal excerpt: password check, PAM failure, failed password, and pre-authentication connection closure |
| [`ssh-repeated-failures.log`](../evidence/SOC-004/ssh-repeated-failures.log) | Original localhost SSH journal selection: four failed-password records |
| [`ssh-detection-alert.log`](../evidence/SOC-004/ssh-detection-alert.log) | Derived detector output for the original repeated-failures selection |
| [`ssh-negative-test.log`](../evidence/SOC-004/ssh-negative-test.log) | Journal-derived negative test subset: byte-identical records to the first two lines of the repeated-failures selection; the original extraction command was not supplied |
| [`ssh-negative-test-result.log`](../evidence/SOC-004/ssh-negative-test-result.log) | Derived detector output for the negative subset |
| [`ssh-boundary-test.log`](../evidence/SOC-004/ssh-boundary-test.log) | **Synthetic** boundary fixture with failures 61 seconds apart; not original journal evidence |
| [`ssh-boundary-test-result.log`](../evidence/SOC-004/ssh-boundary-test-result.log) | Derived detector output for the synthetic outside-window fixture |
| [`ssh-exact-boundary-test.log`](../evidence/SOC-004/ssh-exact-boundary-test.log) | **Synthetic** exact-boundary fixture with offsets 0, 30, and 60 seconds; not original journal evidence |
| [`ssh-exact-boundary-test-result.log`](../evidence/SOC-004/ssh-exact-boundary-test-result.log) | Derived detector output for the synthetic exact-boundary fixture |
| [`ssh_detector.py`](../evidence/SOC-004/ssh_detector.py) | Original transferred detector file, included in the ten-file manifest |

The two synthetic boundary fixtures reuse lab-style hostname, account, loopback address, PID, and port fields. Their timestamps are constructed test values and do not establish that those SSH events occurred at those times. Detector output is a derived result, not a journal export.

## Original journal observations and alert timeline

All timestamps below come from the supplied original journal excerpts and retain their recorded `-04:00` offset.

| Time on 2026-10-12 | Supplied observation |
| --- | --- |
| 13:58:18 | `unix_chkpwd` password-check failure and `pam_unix(sshd:auth)` authentication failure for `analyst` |
| 13:58:20 | Failed SSH password from `127.0.0.1`, port `33040`; connection closed before authentication |
| 14:06:26 | Failed SSH password from `127.0.0.1`, port `38004` |
| 14:06:35 | Failed SSH password from `127.0.0.1`, port `43684` |
| 14:06:45 | Failed SSH password from `127.0.0.1`, port `47954`; the detector reaches its threshold |

The positive input contains **four** matching events. The first event is 486 seconds before the next and expires from the active window. The final three failures occur over **19 seconds**, producing one alert with window start **14:06:26-04:00** and alert time **14:06:45-04:00**.

The initial password/PAM records and connection closure provide context, but only the matching `Failed password` line is counted by this detector. No successful authentication is shown in the supplied excerpts; they do not establish the full session or host history.

## Four validated original scenarios

On **2026-10-12**, the transferred original inputs were replayed with **Python 3.14.8 on Windows**, using both the exact pasted-source copy and the transferred-source copy. Both passed all four scenarios.

| Scenario | Supplied input | Parsed events | Expected / actual alerts | Result |
| --- | --- | ---: | ---: | --- |
| Positive: threshold reached | Four original journal failures; final three at 14:06:26, 14:06:35, and 14:06:45 | 4 | 1 / 1 | PASS |
| Negative: fewer than three failures | First two original failure records, 486 seconds apart | 2 | 0 / 0 | PASS |
| Outside-window boundary | Synthetic timestamps 13:58:20, 13:59:21, 14:00:22; offsets 0, 61, 122 seconds | 3 | 0 / 0 | PASS |
| Exact 60-second boundary | Synthetic timestamps 13:58:20, 13:58:50, 13:59:20; offsets 0, 30, 60 seconds | 3 | 1 / 1 | PASS |

The original negative fixture is below threshold and also outside the window; it does not isolate the count condition inside a single 60-second window. The earlier preparation run separately checked two failures at offsets 0 and 30 seconds.

For each original scenario, parsed counts and alert totals were checked, and **the complete rerun output matched the saved Kali result log** after normalizing CRLF to LF for comparison. The published original evidence bytes were not normalized or edited.

[Original-evidence validation results](../evidence/SOC-004/original-evidence-validation.json) record all ten hashes, both syntax results, source-copy differences, and the four replay comparisons. The user-supplied exact-boundary terminal photograph reviewed earlier also showed three parsed events and one alert from 13:58:20 to 13:59:20, consistent with the transferred synthetic fixture and result.

The [earlier preparation-run results](../evidence/SOC-004/publication-preparation-validation.json) remain separately labeled. They used freshly generated artificial inputs with a 2000-01-01 baseline and do not replace the user's Kali evidence or its saved outputs.

## Syntax and ten-file SHA256 verification

Both source copies passed `py_compile.compile(..., doraise=True)`. The original [`SHA256SUMS.txt`](../evidence/SOC-004/SHA256SUMS.txt) contains ten supplied digest values, and all ten independently matched the transferred raw bytes.

The [user-reported ten-line check](../evidence/SOC-004/user-reported-sha256-check.txt) is retained as a historical transcript. It is distinct from the manifest and from the new independent verification results.

From the repository root, the following Linux commands reproduce syntax and original-file integrity checks:

```sh
python3 -m py_compile detections/SOC-004/ssh_detector.py evidence/SOC-004/ssh_detector.py
(
  cd evidence/SOC-004
  sha256sum -c SHA256SUMS.txt
)
```

The manifest covers the **original evidence-directory detector**, not the separate pasted-source copy, report, manifest itself, or newly generated validation JSON. The two source files have different hashes because of their documented outer blank lines.

Replay the original scenarios with:

```sh
python3 detections/SOC-004/ssh_detector.py evidence/SOC-004/ssh-repeated-failures.log
python3 detections/SOC-004/ssh_detector.py evidence/SOC-004/ssh-negative-test.log
python3 detections/SOC-004/ssh_detector.py evidence/SOC-004/ssh-boundary-test.log
python3 detections/SOC-004/ssh_detector.py evidence/SOC-004/ssh-exact-boundary-test.log
```

The expected alert totals are **1, 0, 0, 1**, respectively.

## Analysis and limitations

The original positive case and two synthetic boundary fixtures validate the configured threshold and inclusive window behavior for matching lines. Original and pasted-source copies reproduce the saved outputs without logic changes.

The preserved detector has a limited scope:

- It does not match every SSH authentication message. In particular, `Failed password for invalid user ...` does not match the supplied pattern.
- Nonmatching lines are silently skipped. Zero alerts do not prove that an input contains no authentication failures.
- Malformed matched timestamps can raise an exception; mixing timezone-aware and timezone-naive timestamps can also fail.
- A missing file prints an error and returns without an explicit nonzero exit status. A process exit status alone is insufficient to validate a run.
- Deduplication lasts only for the invocation. Grouping by source IP and username does not detect distributed activity across different pairs.
- This is an offline text-file detector. No live journal ingestion, SIEM integration, automated blocking, or production deployment is claimed.

The report covers the supplied localhost excerpts and fixture results. It does not establish the full journal history, independently authenticate collection, or assess the entire host for compromise.

## Disposition and merge gate

**Authorized controlled localhost exercise / no confirmed real-world security incident.** The transferred artifacts pass ten-file integrity verification, both syntax checks, and all four original scenario replays within the documented scope.

The evidence, detector, results, report, and README index are prepared in a separate **draft PR**. The PR remains **unmerged** until the user explicitly approves merging. Approval to publish these artifacts does not authorize merge.

## Lessons learned

- Validate both the event-count threshold and the inclusive time boundary.
- Keep original journal records, synthetic fixtures, and detector-derived output distinct.
- Preserve original bytes and manifest paths when asserting hash integrity.
- Compare complete outputs, document source-format differences, and state collection limitations.
