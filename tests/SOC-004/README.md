# New SOC-004 synthetic test package

These files were added for the documentation remediation sprint. They are constructed tests, not SSH journal exports or recovered inputs from the earlier preparation run. All fixtures use a 2000-01-01 UTC baseline, `synthetic-lab`, synthetic usernames and loopback IPs. They are outside the unchanged original ten-file manifest.

Run from the repository root with Python 3.10 or newer (standard library only):

```sh
python tests/SOC-004/generate_fixtures.py --check
python tests/SOC-004/run_tests.py
```

The [generator](generate_fixtures.py) preserves deterministic input/expected-output bytes and declares expectations independently of the detector. The [runner](run_tests.py) compares complete stdout, normalizing CRLF to LF only during comparison. It replays four historical inputs against both unchanged historical sources and the optional v2, plus seven new fixtures against all three sources. It verifies all ten original hashes, source-copy outer blank lines, the journal-derived negative subset, and syntax in memory. It writes no output or caches into the historical evidence directory and performs no authentication or network activity. A failure exits nonzero.

| New fixture and expected output | Purpose | Parsed events | Alerts |
| --- | --- | ---: | ---: |
| [Within-window](fixtures/within-window.log), [expected](fixtures/within-window.expected.txt) | Offsets 0/30/59 | 3 | 1 |
| [Below threshold inside window](fixtures/below-threshold-in-window.log), [expected](fixtures/below-threshold-in-window.expected.txt) | Two failures at 0/30; isolates count condition | 2 | 0 |
| [Outside-window](fixtures/outside-window.log), [expected](fixtures/outside-window.expected.txt) | Offsets 0/30/61 | 3 | 0 |
| [Exact boundary](fixtures/exact-boundary.log), [expected](fixtures/exact-boundary.expected.txt) | Offsets 0/30/60; inclusive boundary | 3 | 1 |
| [Separate pairs](fixtures/separate-pairs.log), [expected](fixtures/separate-pairs.expected.txt) | Different source/user pairs do not combine | 3 | 0 |
| [Unsorted](fixtures/unsorted.log), [expected](fixtures/unsorted.expected.txt) | Input offsets 59/0/30; chronological sorting | 3 | 1 |
| [Two bursts](fixtures/two-bursts-one-alert.log), [expected](fixtures/two-bursts-one-alert.expected.txt) | 0/10/20 and 120/130/140; one alert per pair per invocation | 6 | 1 |

To generate a separate fresh set, use `python tests/SOC-004/generate_fixtures.py --output-dir local-output/soc004-fixtures`. The four preparation-style offsets match those recorded in the old JSON, but the new bytes and generator are not claimed to recover the old inputs or historical execution.

## Optional hardened detector

The [new v2](../../detections/SOC-004/ssh_detector_v2.py) requires an explicit UTF-8 input file, accepts ordinary and `invalid user` failed-password records, and requires timezone-aware ISO timestamps. It sorts by timestamp and uses the same source/user grouping, inclusive 60-second window and per-invocation deduplication as the historical detector. Matching ordinary lines reproduce the saved historical stdout; record counts are additionally written to stderr.

Unsupported failed-password records, invalid or naive timestamps (including mixed aware/naive input), invalid UTF-8, missing files and directory inputs exit 2 and emit no detection result. Other nonmatching records are counted as skipped; empty/all-skipped files parse successfully but report zero matched records, so a negative result is limited to parsed events. The runner checks these cases and invalid-user detection separately using new temporary artificial inputs. A successful exit does not establish absence of authentication activity or host compromise.

This remains an offline teaching detector, not a production monitor, complete SSH parser, SIEM or blocking tool. Both historical source files remain unchanged for evidence replay. See the [case report](../../investigations/SOC-004-automated-ssh-detection.md) for historical limitations and the [new collection guide](../../docs/reproduction.md) for loopback prerequisites.
