# SOC-004 evidence and validation

The user transferred these existing Kali artifacts through a temporary VirtualBox shared folder. All ten files listed in the supplied [SHA256SUMS.txt](SHA256SUMS.txt) independently matched their expected hashes on 2026-10-12. Source, log, result, and manifest bytes are preserved unchanged.

## Original journal evidence

- [ssh-first-failure.log](ssh-first-failure.log): original localhost SSH journal excerpt, including password/PAM failure and pre-authentication closure.
- [ssh-repeated-failures.log](ssh-repeated-failures.log): four original failed-password records from the localhost exercise.
- [ssh-detection-alert.log](ssh-detection-alert.log): derived detector result; four parsed events and one alert.

## Test fixtures and saved results

- [ssh-negative-test.log](ssh-negative-test.log): journal-derived subset, with records byte-identical to the first two lines of the repeated-failures file; original extraction command unavailable.
- [ssh-negative-test-result.log](ssh-negative-test-result.log): two events, zero alerts.
- [ssh-boundary-test.log](ssh-boundary-test.log): **synthetic** fixture, offsets 0/61/122 seconds.
- [ssh-boundary-test-result.log](ssh-boundary-test-result.log): three events, zero alerts.
- [ssh-exact-boundary-test.log](ssh-exact-boundary-test.log): **synthetic** fixture, offsets 0/30/60 seconds.
- [ssh-exact-boundary-test-result.log](ssh-exact-boundary-test-result.log): three events, one alert.

Synthetic fixture timestamps are constructed test values. They are not original SSH journal evidence. Result logs are derived detector output.

## Source and integrity

- [ssh_detector.py](ssh_detector.py): original transferred detector bytes, covered by the manifest.
- [Exact pasted-source detector](../../detections/SOC-004/ssh_detector.py): preserved separately; the original file has one additional leading LF and two trailing LF bytes, with no other difference.
- [original-evidence-validation.json](original-evidence-validation.json): independent ten-file SHA256 verification, both syntax checks, and complete saved-output comparisons for four original scenarios.
- [user-reported-sha256-check.txt](user-reported-sha256-check.txt): historical ten-line `OK` transcript; distinct from the manifest.
- [publication-preparation-validation.json](publication-preparation-validation.json): earlier run on four newly generated artificial inputs; distinct from the original Kali scenario results.

To verify original evidence bytes from this directory:

```sh
sha256sum -c SHA256SUMS.txt
```

The manifest covers ten original artifacts; it does not cover the manifest itself or the additional report and validation files. Existing lab hostname/account and loopback values required no additional publication redaction. Hash matching confirms agreement with the supplied manifest, not independent authentication of the original collection.

Read the [SOC-004 investigation report](../../investigations/SOC-004-automated-ssh-detection.md) for the timeline, scenario interpretation, and limitations. The PR remains draft and requires explicit user approval before merge.
