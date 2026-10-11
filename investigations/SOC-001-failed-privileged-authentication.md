# SOC-001 — Failed Privileged Authentication Investigation

**Status:** Completed controlled exercise  
**Environment:** Kali Linux VM (`kali-soc-lab`) in VirtualBox, NAT networking  
**Investigation type:** Linux authentication log review and event correlation  
**Evidence status:** Timestamped journal excerpts supplied and transcribed below; screenshots and independently exported raw log file remain pending.

## Objective
Generate and investigate an authorized failed privileged authentication attempt and determine whether the event should be treated as suspicious activity or expected test behavior.

## Lab context
The exercise used the `analyst` account on a personally controlled Kali Linux VM. A deliberately incorrect password was entered for a `sudo` operation, followed by a successful authorized `sudo` operation. The analyst inspected Linux journal entries to correlate the activity.

## Observed sequence
1. Initiated a privileged action with `sudo`.
2. Entered an incorrect password, producing a failed authentication event.
3. Performed a successful `sudo` authentication afterward.
4. Reviewed `journald` records and correlated the failure and success as one authorized test sequence.

## Verified event timeline (October 10, 2026)

| Recorded local time | Event | Evidence |
| --- | --- | --- |
| 13:27:49 | PAM authentication failure | `sudo[6173]`, account `analyst`, `tty=/dev/pts/0` |
| 13:28:10 | Privileged command `/usr/bin/whoami` logged | `sudo[6173]`, `USER=root`, `TTY=pts/0` |
| 13:28:10 | Root session opened then closed | `pam_unix(sudo:session)`, PID 6173 |
| 13:28:32 | Follow-up journal review | `sudo[6559]`, `COMMAND=/usr/bin/journalctl -b --no-pager` |

The failed authentication and successful privileged command occurred **21 seconds apart** and share **PID 6173**. This supports correlation to the same `sudo` process, not a separate unverified login. The supplied journal timestamps do not specify a timezone; no offset is inferred.

### Supplied journal evidence

```text
Oct 10 13:27:49 kali-soc-lab sudo[6173]: pam_unix(sudo:auth): authentication failure; logname=analyst uid=1000 euid=0 tty=/dev/pts/0 ruser=analyst rhost=  user=analyst
Oct 10 13:28:10 kali-soc-lab sudo[6173]:  analyst : TTY=pts/0 ; PWD=/home/analyst ; USER=root ; COMMAND=/usr/bin/whoami
Oct 10 13:28:10 kali-soc-lab sudo[6173]: pam_unix(sudo:session): session opened for user root(uid=0) by analyst(uid=1000)
Oct 10 13:28:10 kali-soc-lab sudo[6173]: pam_unix(sudo:session): session closed for user root
Oct 10 13:28:32 kali-soc-lab sudo[6559]:  analyst : TTY=pts/0 ; PWD=/home/analyst ; USER=root ; COMMAND=/usr/bin/journalctl -b --no-pager
```

These excerpts were supplied from the user's lab output. They have not been independently verified against an exported journal file or screenshot.

## Analysis
A single failed `sudo` authentication event can occur because of user error, an authorized test, or malicious attempts to gain elevated privileges. The nearby successful event and known testing context support classifying this sequence as authorized lab activity. The evidence described here does not establish brute-force activity, compromise, or unauthorized access.

## Disposition
**Authorized simulation / no confirmed security incident.** This disposition applies only to the controlled lab sequence described above, not to arbitrary authentication failures on production systems.

## Detection and investigation workflow
- Identify relevant `sudo` and authentication records in the Linux journal.
- Correlate event order and user context.
- Assess whether the observed sequence matches the authorized test.
- Record the conclusion and limitations.

Example commands for **future evidence collection** (not claimed as the original commands used):

```bash
sudo journalctl --no-pager | grep -Ei 'sudo|authentication failure'
sudo journalctl --since 'today' --no-pager | grep -Ei 'sudo|authentication failure'
```

These commands may require adapting the time range or journal access permissions.

## Evidence integrity and visual presentation

The timestamped log excerpts above are transcribed from the original Kali Linux journal output supplied by the lab operator. A separate phone photograph of the terminal also shows the events. An AI-generated cleaned-up visual reconstruction may be useful for presentation, but **must never be represented as an original screenshot or primary forensic evidence**. If included in this repository, label it clearly as an illustration and retain the original image and log excerpts.

**Image upload pending:** Binary image upload was not available through the connected GitHub text-editing workflow. No screenshot or reconstructed image is claimed to be stored in this repository yet.

## Evidence to add
- [x] Timestamped failed authentication excerpt (user-supplied)
- [x] Timestamped successful `sudo` excerpt (user-supplied)
- [x] Event timeline based on recorded timestamps
- [x] Correlation by PID, terminal and account; timestamp timezone not provided
- [ ] Upload the original terminal photograph as primary visual evidence
- [ ] Optionally upload the enhanced *AI-generated reconstruction* with an explicit illustration label

## Lessons learned
- Authentication failures require context before escalation.
- Correlating adjacent events helps distinguish mistakes and controlled tests from potential threats.
- A defensible case report records both the finding and what evidence is missing.

## Next steps
Improve the case with real log excerpts and timestamps. Keep SOC-002 on hold until explicitly resumed.
