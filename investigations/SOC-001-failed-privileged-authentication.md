# SOC-001 — Failed Privileged Authentication Investigation

**Status:** Completed controlled exercise  
**Environment:** Kali Linux VM (`kali-soc-lab`) in VirtualBox, NAT networking  
**Investigation type:** Linux authentication log review and event correlation  
**Evidence status:** Summary based on exercise notes; original timestamped log excerpts and screenshots still need to be attached.

## Objective
Generate and investigate an authorized failed privileged authentication attempt and determine whether the event should be treated as suspicious activity or expected test behavior.

## Lab context
The exercise used the `analyst` account on a personally controlled Kali Linux VM. A deliberately incorrect password was entered for a `sudo` operation, followed by a successful authorized `sudo` operation. The analyst inspected Linux journal entries to correlate the activity.

## Observed sequence
1. Initiated a privileged action with `sudo`.
2. Entered an incorrect password, producing a failed authentication event.
3. Performed a successful `sudo` authentication afterward.
4. Reviewed `journald` records and correlated the failure and success as one authorized test sequence.

**Important:** The exact command used for the test, event timestamps, journal messages, and source screenshots are not included in the available notes. They must be retrieved from the VM before adding a detailed event timeline.

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

## Evidence to add
- [ ] Redacted timestamped failed authentication entry
- [ ] Redacted successful `sudo` event
- [ ] Short event timeline using actual log timestamps
- [ ] Explanation of relevant journal fields and limitations
- [ ] Optional screenshot showing the journal query and matching results

## Lessons learned
- Authentication failures require context before escalation.
- Correlating adjacent events helps distinguish mistakes and controlled tests from potential threats.
- A defensible case report records both the finding and what evidence is missing.

## Next steps
Improve the case with real log excerpts and timestamps. Keep SOC-002 on hold until explicitly resumed.
