# SOC-004 — Automated SSH Authentication Failure Detection

**Status:** Detector validated on four new synthetic scenarios; draft publication awaiting the original evidence files  
**Investigation type:** Linux SSH journal review and Python detection validation  
**Environment:** User-controlled Kali Linux localhost SSH exercise  
**Disposition:** Authorized lab activity; no real-world compromise is established  
**Evidence basis:** Verbatim user-pasted detector source, one user-supplied terminal photograph, a user-reported pass acknowledgment, and a ten-file verification transcript. The original Kali log files and SHA256 manifest have not been supplied for this draft.

## Objective and scope

Detect repeated SSH password failures for the same source IP and target username: at least three matching events within an inclusive 60-second sliding window. Distinguish original localhost journal evidence from constructed test inputs and detector-generated results.

This is a learning exercise in a personally controlled lab. A detection alert identifies the configured pattern; it does not independently establish an attack, successful login, or compromise.

## Detector implementation

The [Python detector](../detections/SOC-004/ssh_detector.py) preserves the exact source text pasted by the user in the referenced conversation. No logic, formatting, or error-handling changes were made. The source was imported from chat text; byte-for-byte identity with the original Kali file, including its final newline, remains unverified.

- Accepts an input file as its first command-line argument; otherwise reads `~/SOC-004-evidence/ssh-repeated-failures.log`.
- Matches lines beginning with a timestamp and ending in `Failed password for <username> from <source_ip> port <port> ssh2`.
- Parses timestamps with `datetime.fromisoformat`, sorts events chronologically, and groups them by `(source_ip, username)`.
- Retains an event at exactly 60 seconds because the expiration condition is `current_time - window[0] > WINDOW`.
- Emits at most one alert per source-IP/username pair per invocation. Additional qualifying windows for that pair do not produce new alerts during the same run.

Example after the original evidence files are provided, from the repository root:

```sh
python3 detections/SOC-004/ssh_detector.py evidence/SOC-004/ssh-repeated-failures.log
```

That input file is pending; the command is a usage example, not a claim that this draft contains it.

## Evidence provenance and inventory

The following names come from the user's ten-file verification transcript. They are an inventory of requested original artifacts, not links to files already published.

| Original artifact | Role and provenance | Draft availability |
| --- | --- | --- |
| `ssh_detector.py` | Detector source | Verbatim chat source imported under `detections/SOC-004/`; original Kali bytes pending |
| `ssh-first-failure.log` | Original localhost SSH journal evidence: initial failed authentication | Original file pending |
| `ssh-repeated-failures.log` | Original localhost SSH journal evidence: repeated failed authentications | Original file pending |
| `ssh-detection-alert.log` | Detector output for the repeated-failures input; derived result, not a journal export | Original file pending |
| `ssh-negative-test.log` | Below-threshold validation input | Original file and provenance details pending; no claim that this is an original journal export |
| `ssh-negative-test-result.log` | Derived detector result for the negative input | Original file pending |
| `ssh-boundary-test.log` | Synthetic outside-window boundary input | Original synthetic fixture pending; not original SSH journal evidence |
| `ssh-boundary-test-result.log` | Derived detector result for the outside-window fixture | Original file pending |
| `ssh-exact-boundary-test.log` | Synthetic exact-60-second boundary input | Original synthetic fixture pending; not original SSH journal evidence |
| `ssh-exact-boundary-test-result.log` | Derived detector result for the exact-boundary fixture | Original file pending; a terminal photograph shows the result |

The first-failure and repeated-failures logs are designated original localhost journal evidence by the exercise context. Their contents, collection command, full timestamp range, event counts, and sanitization history cannot yet be independently inspected. Do not treat synthetic boundary records as evidence that those SSH events actually occurred.

The negative test's construction method is unavailable in the retrieved material. Its provenance will be confirmed from the original file and the user's collection notes before it is presented as journal-derived or synthetic.

No missing log has been reconstructed from the photograph or invented for this draft. The new validation run below uses different, explicitly synthetic inputs and does not replace any of these ten original artifacts.

## Observed exact-boundary photograph

A user-supplied photograph in the referenced conversation shows a detector invocation against `ssh-exact-boundary-test.log` and output reporting:

- Events parsed: **3**.
- Source IP: **127.0.0.1**; target user: **analyst**.
- Failed attempts at alert time: **3**; total alerts: **1**.
- Window start: **2026-10-12T13:58:20-04:00**.
- Alert time: **2026-10-12T13:59:20-04:00**.

The displayed timestamps span exactly 60 seconds, consistent with the inclusive boundary in the pasted source. They belong to the synthetic test shown in the photograph; they are not assigned to the original journal collection. The photograph was reviewed without regenerating log text. It is not included in this draft, and it cannot establish the bytes or hash of the underlying files.

## Four validated scenarios

The exact pasted detector was executed on four **newly generated synthetic inputs** during publication preparation on **2026-10-12**, using **Python 3.14.8 on Windows**. All inputs used the same loopback source and a synthetic `testuser` account. The baseline was deliberately artificial: `2000-01-01T00:00:00+00:00`, with host label `synthetic-validation`.

Offsets below are seconds relative to that synthetic baseline. These values describe the new validation run only; they are not asserted to be the user's unseen Kali fixture contents.

| Scenario | New input offsets | Parsed events | Expected alerts | Actual alerts | Result |
| --- | --- | ---: | ---: | ---: | --- |
| Positive: three failures within the window | 0, 30, 59 | 3 | 1 | 1 | PASS |
| Negative: fewer than three failures | 0, 30 | 2 | 0 | 0 | PASS |
| Outside-window boundary: first event expires | 0, 30, 61 | 3 | 0 | 0 | PASS |
| Exact boundary: first event remains at 60 seconds | 0, 30, 60 | 3 | 1 | 1 | PASS |

Validation checked parsed-event counts, total alerts, alert block counts, and the source, username, failed-attempt count, window start, and alert time for alerting scenarios. Non-alerting scenarios produced the detector's no-threshold-exceeded message.

[Machine-readable validation results](../evidence/SOC-004/publication-preparation-validation.json) record this new run. The original Kali result logs remain pending; the photograph corroborates only the exact-boundary result.

## Syntax and ten-file SHA256 verification

The available conversation contains a user acknowledgment, `passed`, after the detector source was pasted. The command associated with that acknowledgment is unavailable, so the original syntax-check invocation cannot be reconstructed. Independently, `py_compile.compile(..., doraise=True)` succeeded on the imported detector during this preparation run.

The [user-reported verification transcript](../evidence/SOC-004/user-reported-sha256-check.txt) preserves these ten lines verbatim:

```text
ssh_detector.py: OK
ssh-first-failure.log: OK
ssh-repeated-failures.log: OK
ssh-detection-alert.log: OK
ssh-negative-test.log: OK
ssh-negative-test-result.log: OK
ssh-boundary-test.log: OK
ssh-boundary-test-result.log: OK
ssh-exact-boundary-test.log: OK
ssh-exact-boundary-test-result.log: OK
```

The request identifies this as the ten-file SHA256 verification. The transcript reports ten successful checks, but contains **no digest values**. Neither the original manifest nor the exact command is available. This draft does not claim independent verification of those original files, provide invented hashes, or treat freshly computed hashes of imported chat text as the user's original SHA256 values.

After upload, verification must compare the supplied original file bytes with the supplied existing manifest. Repository-path changes must be documented when the detector is stored separately from the evidence logs. Sanitized publication copies require their own digest values and a documented redaction mapping; their hashes must not be presented as hashes of unmodified originals.

## Analysis and limitations

The four new synthetic scenarios support the detector's threshold and inclusive window behavior for matching lines. The exact-boundary photograph is consistent with the same behavior on the user's displayed lab test.

The preserved implementation has deliberate scope limits:

- It matches the shown password-failure format, not every SSH failure message. In particular, `Failed password for invalid user ...` does not match this pattern.
- A nonmatching line is skipped silently. No-match input can report zero alerts without proving that no authentication failures occurred.
- Matching lines with malformed timestamps can raise an exception; mixed timezone-aware and timezone-naive timestamps can also fail sorting or subtraction.
- A missing file prints an error and returns without an explicit nonzero exit status. Validation must inspect output rather than rely only on the process exit code.
- Deduplication is per invocation, not durable incident tracking. Source IP and username grouping does not detect distributed activity across different pairs.
- This is an offline text-file detector. No live journal ingestion, SIEM integration, automated blocking, or production deployment is claimed.

## Disposition and publication gate

**Authorized controlled localhost exercise.** The reproduced results demonstrate the configured detection logic within the stated test scope. The unseen original journal evidence is insufficient here to establish a full event timeline or a broader host-security conclusion.

The PR must remain **draft and unmerged** until the original approved artifacts are uploaded, provenance and sanitization are checked, the original ten-file manifest is verified, and the user explicitly approves merging. Approval to publish the draft is not merge approval.

## Lessons learned

- Validate both the event-count threshold and the inclusive time boundary.
- Separate original journal records, synthetic fixtures, and detector-derived results.
- Preserve exact source and file bytes before asserting hash integrity.
- Record evidence gaps directly and keep incomplete publication in draft review.
