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

## Recovered original terminal photograph

On 2026-10-12, the cached user upload `IMG_2551.jpeg` was recovered and copied byte-for-byte as [SOC-004-exact-boundary-terminal-original.jpeg](SOC-004-exact-boundary-terminal-original.jpeg). The earlier SOC-004 preparation chat records viewing this same cached attachment. Both accessible cached copies are identical; the published JPEG is 749,043 bytes, 1536 × 1300 pixels, with one frame. Its embedded EXIF and ICC data remain intact.

![User-supplied Kali terminal photograph showing the synthetic exact 60-second boundary fixture and detector output](SOC-004-exact-boundary-terminal-original.jpeg)

*Exact-boundary test photograph, preserved as received: three constructed failure records at 13:58:20, 13:58:50, and 13:59:20 (`-04:00`); three parsed events and one alert. The displayed fixture and output agree with [ssh-exact-boundary-test.log](ssh-exact-boundary-test.log) and [its saved result](ssh-exact-boundary-test-result.log). These are synthetic test timestamps, not photograph capture times or proof of live authentication events.*

[Photograph provenance](photograph-provenance.json) records the original upload name, visible content, recovery scope, SHA256 digest, and authenticity limits. [photographs.sha256](photographs.sha256) is a separate inventory for all 21 supplied photograph files; it does not modify the original ten-file manifest. From this directory, verify the photographs with `sha256sum -c photographs.sha256`.

The following additional uploads now provide the SSH setup, loopback binding, journal collection, positive detector result, and individual log-hash photographs. The remaining photo gaps are identified below. Preserving supplied upload bytes does not independently authenticate camera acquisition or pre-upload editing history.

## Additional original terminal photographs

The user supplied **20 additional JPEG photographs on 2026-10-12**. Each is copied byte-for-byte under an accurately named file below. Together with the recovered exact-boundary JPEG, this directory contains **21 distinct supplied photograph files**. Their SHA256 digests, sizes, dimensions, upload names, embedded-metadata presence and captions are recorded in [photograph-provenance.json](photograph-provenance.json). Their upload sequence is preserved without asserting camera chronology. All embedded metadata remains intact.

| Upload | Original photograph | Visible content and limits |
| --- | --- | --- |
| Photo 1 | [SSH service initially inactive](SOC-004-01-ssh-inactive-original.jpg) | The initial systemctl status shows ssh.service loaded but inactive (dead) and disabled. |
| Photo 2 | [SSH service started with wildcard listeners](SOC-004-02-ssh-started-wildcard-original.jpg) | systemctl start/status shows the service active since 2026-10-12 13:33:54 EDT; its journal records wildcard IPv4 and IPv6 listeners. This precedes loopback restriction. |
| Photo 3 | [Initial wildcard socket check](SOC-004-03-wildcard-socket-check-original.jpg) | The ss output shows 0.0.0.0:22 and [::]:22 with sshd PID 111930. These are initial wildcard bindings, not the later loopback-only state. |
| Photo 4 | [Configuration before the loopback edit](SOC-004-04-sshd-config-before-change-original.jpg) | GNU nano 9.2 displays sshd_config, its Include directive, and commented ListenAddress defaults. The photograph does not show an active loopback directive. |
| Photo 5 | [Configuration backup and syntax check](SOC-004-05-config-backup-and-syntax-original.jpg) | The terminal shows a backup to sshd_config.soc004.bak, an editor invocation, and sshd -t followed by SSH configuration valid. Syntax validity does not establish loopback binding. |
| Photo 6 | [Effective configuration still wildcard](SOC-004-06-effective-wildcard-config-original.jpg) | After the syntax check, sshd -T reports [::]:22 and 0.0.0.0:22. The initial edit had not established loopback-only listening. |
| Photo 7 | [ListenAddress investigation](SOC-004-07-listenaddress-investigation-original.jpg) | The terminal shows searches for active ListenAddress directives and numbered commented defaults in sshd_config, while the effective configuration above still shows wildcard addresses. |
| Photo 8 | [Loopback configuration and socket verified](SOC-004-08-loopback-binding-verified-original.jpg) | The terminal shows an active ListenAddress 127.0.0.1 directive, successful sshd -t, effective 127.0.0.1:22, service restart, and an ss listener at 127.0.0.1:22 with sshd PID 122186. |
| Photo 9 | [SSH service restart journal](SOC-004-09-ssh-service-journal-original.jpg) | journalctl displays the initial wildcard startup at 13:33:54 and restart at 13:54:58 with a listener on 127.0.0.1 port 22. The short timestamp display omits an explicit offset. |
| Photo 10 | [First localhost login failure](SOC-004-10-first-localhost-login-failure-original.jpg) | The localhost password-only SSH attempt shows host-key acceptance, a password prompt with no password value displayed, and Permission denied (publickey,password). |
| Photo 11 | [First failure journal context](SOC-004-11-first-failure-journal-original.jpg) | Filtered journal output shows password/PAM failure at 13:58:18 and failed password plus pre-authentication closure at 13:58:20, for analyst from 127.0.0.1 port 33040. |
| Photo 12 | [Bounded first-failure journal export](SOC-004-12-first-failure-export-original.jpg) | The terminal shows journalctl --since 2026-10-12 13:57:00 --until 2026-10-12 14:00:00 with short-iso output redirected to ssh-first-failure.log, then wc/cat displaying four records with -04:00 timestamps. |
| Photo 13 | [First-failure hash and repeated attempts](SOC-004-13-first-failure-hash-and-attempts-original.jpg) | The displayed SHA256 of ssh-first-failure.log matches the preserved file and original manifest. Three further localhost SSH commands end in Permission denied; password values are not displayed. |
| Photo 14 | [Journal command error preserved](SOC-004-14-journal-command-error-original.jpg) | An attempted journal query uses --no pager and returns an ambiguous --no option error. This failed query is preserved as photographed and is not evidence of a successful export. |
| Photo 15 | [Corrected journal query](SOC-004-15-corrected-failure-query-original.jpg) | The corrected --no-pager query displays four failed-password events at 13:58:20, 14:06:26, 14:06:35 and 14:06:45 (-04:00). The earlier command error remains visible above it. |
| Photo 16 | [Repeated-failure export](SOC-004-16-repeated-failures-export-original.jpg) | The corrected journal query is redirected to ssh-repeated-failures.log; wc/cat displays four records agreeing with the preserved original selection. |
| Photo 17 | [Repeated-failure hash, Python version and early detector](SOC-004-17-repeated-hash-and-python-original.jpg) | The displayed SHA256 of ssh-repeated-failures.log matches the preserved file and manifest. python3 --version shows 3.14.7. An earlier detector stage prints SSH Threat Detection and Log records loaded: 4; it is not the final saved detector output. |
| Photo 18 | [Intermediate parser development](SOC-004-18-parser-development-stage-original.jpg) | The photograph shows four parsed timestamp/user/source/port records and earlier SSH Threat Detection output. It records an intermediate detector stage; that version of the source has not been recovered. |
| Photo 19 | [Positive detector test](SOC-004-19-positive-detector-alert-original.jpg) | The final Automated SSH Detection display reports four parsed events, threshold 3 failures / 60 seconds, and one alert with three failures from 14:06:26 to 14:06:45 (-04:00), matching ssh-detection-alert.log. |
| Photo 20 | [Saved positive result displayed](SOC-004-20-saved-positive-result-original.jpg) | cat ssh-detection-alert.log displays four parsed events and one alert for the three failures from 14:06:26 to 14:06:45 (-04:00), agreeing with the preserved saved result. |

Photos 2–7 document the initial wildcard configuration; Photo 8 shows the later loopback configuration and listener. Photos 12 and 16 show the original export commands and displayed records. Photos 13 and 17 show individual log hashes matching the unchanged original manifest. Photos 17–18 depict intermediate detector stages whose source versions are unavailable; Photos 19–20 show the final positive result. The photographed Kali Python version is **3.14.7**, distinct from the historical Windows replay version.

The negative and outside-window detector-test photographs and the final detector syntax/complete ten-file checksum photograph remain unavailable. Individual hashes in Photos 13 and 17 do not establish the complete ten-file check. The preserved negative/outside-window fixtures, outputs and independent integrity records remain their public basis.

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

The [new synthetic test package](../../tests/SOC-004/README.md) and optional [hardened detector](../../detections/SOC-004/ssh_detector_v2.py) are separate additions outside this directory and the original manifest. The earlier preparation JSON remains unchanged; its old exact artificial inputs are unavailable. The supplied terminal photographs are documented above and have their own integrity inventory.

Read the [SOC-004 investigation report](../../investigations/SOC-004-automated-ssh-detection.md) for the timeline, scenario interpretation, and limitations. The user explicitly approved merging this publication on **2026-10-12**, after the draft and its completed verification were presented for review.
