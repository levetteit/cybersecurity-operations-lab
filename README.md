# Cybersecurity Operations Lab

Hands-on cybersecurity exercises in a personally controlled NAT virtual machine with outbound Internet access, focused on Linux security monitoring, event analysis, and incident triage.

## Lab environment
- Host: HP laptop (Intel Core i5-7200U, 8 GB RAM)
- Hypervisor: Oracle VirtualBox
- Guest: Kali Linux with Xfce, 2 GB RAM, 1 vCPU, 20 GB dynamically allocated disk
- Guest hostname: `kali-soc-lab`; analyst account: `analyst`
- Networking: NAT with outbound Internet access; no air gap is claimed. SOC-003 includes connections to public services.
- Historical tool versions were not recorded completely; see the [reproduction guide](docs/reproduction.md) for prerequisites and version recording.

## Investigation index

| ID | Exercise | Status | Evidence |
| --- | --- | --- | --- |
| LAB-001 | VirtualBox graphics warning investigation | Previously listed as completed; completion unverified in the published repository | No report, summary, logs, or photographs are published; see [publication status](investigations/LAB-001-publication-status.md) |
| SOC-001 | Failed privileged authentication investigation | Completed controlled exercise | Timestamped transcriptions and original terminal photograph, with provenance and an accurately named MPO copy; raw journal export unavailable |
| SOC-002 | Suspicious process investigation | Completed controlled exercise | Process metadata, ancestry, socket and package checks; four enhanced original photographs |
| SOC-003 | Network traffic investigation | Completed controlled exercise | 50-packet tcpdump capture, Wireshark protocol and TCP/TLS analysis; ten photographic evidence images |
| SOC-004 | Automated SSH authentication failure detection | Completed controlled exercise | Original localhost journal evidence, labeled synthetic fixtures, saved results, exact detector source, and verified ten-file SHA256 manifest |

### SOC-001: Failed privileged authentication
An authorized test of a failed `sudo` authentication followed by a successful `sudo` action. Linux journal records were reviewed to correlate the sequence and assess whether it represented a real security incident.

[Read the SOC-001 case report](investigations/SOC-001-failed-privileged-authentication.md)

### SOC-002: Suspicious process investigation
An authorized controlled simulation investigating `sleep 600` and a separate follow-up `sleep 1800` process. The report documents user-provided process metadata, ancestry, executable path, and socket and package check results, with their limitations. Disposition: authorized controlled simulation / no confirmed incident; no evidence of malware in the supplied observations.

[Read the SOC-002 case report](investigations/SOC-002-suspicious-process-investigation.md)

### SOC-003: Network traffic investigation
An authorized Kali Linux baseline exercise using tcpdump and Wireshark to analyze 50 captured packets, DNS and ICMPv6 traffic, two TCP conversations, and TLS Client Hello SNI values associated with Firefox settings services. Disposition: no confirmed security incident within the limited capture. Ten enhanced original photographs are linked in the report; the raw PCAP remains local and private.

[Read the SOC-003 case report](investigations/SOC-003-network-traffic-investigation.md)

### SOC-004: Automated SSH authentication failure detection
An authorized localhost SSH exercise with a Python detector for three failures from the same source IP and username within an inclusive 60-second window. The four original positive, negative, outside-window, and exact-boundary scenarios reproduce their saved outputs; all ten supplied artifact hashes match the original SHA256 manifest. The report distinguishes original journal evidence, journal-derived test subsets, synthetic boundary fixtures, and detector results.

[Read the SOC-004 case report](investigations/SOC-004-automated-ssh-detection.md)

## Skills practiced
- Linux command-line administration and journal log review
- Authentication event analysis and timeline correlation
- Differentiating controlled test activity from potentially suspicious behavior
- Network packet capture with tcpdump and protocol/conversation analysis in Wireshark
- TCP handshake, DNS, and TLS Client Hello/SNI interpretation
- Python log parsing, sliding-window detection, and threshold/boundary validation
- Writing investigation notes with evidence limitations

## Scope and ethics
The documented exercises used a personally controlled VirtualBox NAT VM with outbound Internet access. NAT does not imply an air gap; SOC-003 observes traffic to public services. Authentication simulations target the controlled VM and loopback, not external systems. No unauthorized access or real-world attack is claimed. This is a learning portfolio, not production SOC employment experience.

## Evidence policy
Reports distinguish supplied observations, transcribed records, derived output, synthetic tests, and AI illustrations. Synthetic timestamps and illustrative visuals are permitted only with explicit provenance labels; they are never represented as historical observations. Preserve private originals and review public copies for sensitive content and metadata. The existing SOC-001 JPEG/MPO retains camera metadata despite its legacy `.png` name; its accurately named MPO copy retains the same metadata. See the [evidence handling policy](docs/evidence-handling.md).

## Reproduction and validation

The [reproduction guide](docs/reproduction.md) separates offline replay from newly proposed Kali collection commands. The new examples are not historical command transcripts and have not been executed against a live VM during remediation.

From the repository root, with Python 3.10 or newer and Git:

```sh
python tests/SOC-004/run_tests.py
python scripts/validate_repository.py
```

Both checks use the standard library and preserve original files. The [SOC-004 test package](tests/SOC-004/README.md) includes newly preserved synthetic fixtures and tests an optional hardened detector separately. See the [DOC-01–DOC-14 remediation record](docs/documentation-remediation.md) for changes, known evidence gaps, and draft review status.

## Author
Jerai Padilla · [GitHub](https://github.com/levetteit)
