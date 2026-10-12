# Documentation remediation record — October 12, 2026

This sprint follows the supplied read-only documentation audit (DOC-01 through DOC-14). Before editing, GitHub main and a fresh checkout both resolved to `2728239bf6f4dd942baf855ef6a9120e9959a256`, the audit's 38-file baseline. The audit attachment was retrieved from the referenced conversation; the conversation cache did not expose earlier assistant content or historical source/upload text.

This is new documentation and offline validation work. It does not create historical acquisition records, missing photographs, or proof of an event that was not supplied. The remediation is proposed in a **new draft PR** and requires user review before merge. Historical approval for SOC-004 PR #10 does not authorize this sprint to merge.

## Findings and disposition

| Audit ID | Remediation | Remaining boundary |
| --- | --- | --- |
| DOC-01 | Refreshed SOC-001 index/status, linked original photograph with provenance and accurately named MPO copy, removed obsolete evidence/hold language. | Raw journal export, authentic acquisition and original event timezone unavailable. |
| DOC-02 | Added [LAB-001 publication status](../investigations/LAB-001-publication-status.md) and corrected the completion/summary claim in the index. | No evidence-backed investigation report can be supplied from available materials. |
| DOC-03 | Replaced blanket exclusion of synthetic content with explicit original/derived/synthetic/AI provenance rules. | Synthetic fixtures and illustrations do not establish historical observations. |
| DOC-04 | Linked SOC-002 ZIP, listed all four members and explained byte-identical redundant packaging. | ZIP contains enhanced photographs, not unedited originals or raw evidence. |
| DOC-05 | Added [newly proposed collection guide](reproduction.md): prerequisites/version recording, sudo sequence, dynamic process PID, bounded capture, loopback SSH, ISO exports, hashing and cleanup. | Fresh live-Kali commands were not executed during this sprint; historical tool versions/commands are not inferred. |
| DOC-06 | Added generator, 14 preserved synthetic input/expected-output files and full-output runner, including two failures within 30 seconds. | Old preparation JSON remains unchanged; exact old generator/input bytes are unavailable. New fixtures are not a recovery of that run. |
| DOC-07 | Explicitly documented the missing SOC-004 photograph; retained fixtures and saved output as public basis. | No actual photograph was available to publish or reauthenticate. |
| DOC-08 | Inspected stale [PR #3](https://github.com/levetteit/cybersecurity-operations-lab/pull/3), whose old patch says no image is published. This sprint supersedes its remaining original-photo/provenance work; it must not be merged unchanged. | Reconciliation is recorded in GitHub PR metadata; the new draft remains subject to review. |
| DOC-09 | Retained legacy JPEG/MPO original bytes and both frames; added an accurately named byte-identical MPO copy and [copy provenance](../evidence/SOC-001/display-provenance.json). Documented retained camera metadata. | Original public metadata and Git history remain; MPO copy retains original metadata and is not a privacy removal. |
| DOC-10 | Removed AI illustration from evidence display, kept archived bytes and documented `dodo[6559]` versus photographed `sudo[6559]`. | Archived image has no embedded label; accompanying provenance is required for sharing. |
| DOC-11 | Added future acquisition/publication checklist and separate [32-artifact snapshot inventory](historical-artifacts.sha256). | Missing historical raw logs, versions, exit statuses, timestamps and PCAP hash cannot be backfilled. |
| DOC-12 | Added optional [new hardened v2](../detections/SOC-004/ssh_detector_v2.py), nonzero errors, skip counts, invalid-user support and explicit timezone handling, with separate tests. | Both historical sources remain unchanged and retain documented limitations; v2 is an offline teaching detector. |
| DOC-13 | Added [ignore rules](../.gitignore), checklist, private output guidance and in-memory syntax checks. | Ignore rules do not sanitize files or erase tracked history. |
| DOC-14 | Clarified NAT/outbound Internet scope and refreshed SOC-003 gallery/photograph wording. | NAT is not an air gap; the raw PCAP remains private. |

## Validation scope

Run with Python **3.14.8 on Windows** during this sprint. The package also requires only Python 3.10+ features, but no minimum-version compatibility run is claimed. Pillow **12.3.0** was used solely for image inspection. The correctly named MPO copy reuses original bytes and requires no image conversion. Repository link/hash checks additionally require Git; external URL checks require network access.

The [test runner](../tests/SOC-004/run_tests.py) passes seven test groups: all ten original manifest hashes, historical source relationship and negative-subset bytes, in-memory syntax, **8/8** complete historical-source replay outputs, **4/4** v2 replay outputs, **21/21** new synthetic complete outputs, invalid-user and skipped-record reporting, and error/empty-input behavior. Full output comparisons normalize CRLF to LF only in memory; no historical files are rewritten. The new below-threshold-in-window fixture isolates two failures within 30 seconds.

The [repository validator](../scripts/validate_repository.py) checks exact-case Markdown paths and heading fragments, Python syntax, both integrity inventories, SOC-001 original/copy provenance hashes, SOC-002 ZIP CRC/member equality and ignored publication by-products. It checks current published paths and can include external HTTP requests. Run these commands from the root:

```sh
python tests/SOC-004/generate_fixtures.py --check
python tests/SOC-004/run_tests.py
python scripts/validate_repository.py --external --report local-output/repository-validation.json
git diff --check
```

The original ten-file SHA256 manifest, both historical detector files, both historical validation JSON files, original logs/results/checksum transcript and all historical images/ZIP are unchanged. The broader inventory checks **32/32** unchanged non-Markdown artifacts against the pinned baseline. All four ZIP members match the root images and pass CRC checks. Both JPEG/MPO frames decode; the accurately named copy is byte-identical to the legacy original and retains its metadata. This checks publication bytes rather than journal acquisition authenticity.

No live authentication, packet capture, service change or external-target test was performed. No CI success is claimed: the baseline has no workflow files, and current GitHub checks must be assessed separately from local results. Final PR metadata and fresh validation output are recorded in the draft description and handoff report.
