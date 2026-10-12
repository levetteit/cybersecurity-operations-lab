# Cybersecurity Operations Lab

Hands-on, isolated cybersecurity exercises focused on Linux security monitoring, event analysis, and incident triage.

## Lab environment
- Host: HP laptop (Intel Core i5-7200U, 8 GB RAM)
- Hypervisor: Oracle VirtualBox
- Guest: Kali Linux with Xfce, 2 GB RAM, 1 vCPU, 20 GB dynamically allocated disk
- Guest hostname: `kali-soc-lab`; analyst account: `analyst`
- Networking: NAT

## Investigation index

| ID | Exercise | Status | Evidence |
| --- | --- | --- | --- |
| LAB-001 | VirtualBox graphics warning investigation | Completed | Written summary; screenshots/log excerpts pending |
| SOC-001 | Failed privileged authentication investigation | Completed | Written case report; exact timestamps/log excerpts pending |
| SOC-002 | Suspicious process investigation | Completed controlled exercise | Process metadata, ancestry, socket and package checks; four enhanced original photographs |
| SOC-003 | Network traffic investigation | Completed controlled exercise | 50-packet tcpdump capture, Wireshark protocol and TCP/TLS analysis; ten photographic evidence images |

### SOC-001: Failed privileged authentication
An authorized test of a failed `sudo` authentication followed by a successful `sudo` action. Linux journal records were reviewed to correlate the sequence and assess whether it represented a real security incident.

[Read the SOC-001 case report](investigations/SOC-001-failed-privileged-authentication.md)

### SOC-002: Suspicious process investigation
An authorized controlled simulation investigating `sleep 600` and a separate follow-up `sleep 1800` process. The report documents user-provided process metadata, ancestry, executable path, and socket and package check results, with their limitations. Disposition: authorized controlled simulation / no confirmed incident; no evidence of malware in the supplied observations.

[Read the SOC-002 case report](investigations/SOC-002-suspicious-process-investigation.md)

### SOC-003: Network traffic investigation
An authorized Kali Linux baseline exercise using tcpdump and Wireshark to analyze 50 captured packets, DNS and ICMPv6 traffic, two TCP conversations, and TLS Client Hello SNI values associated with Firefox settings services. Disposition: no confirmed security incident within the limited capture. Ten enhanced original photographs are linked in the report; the raw PCAP remains local and private.

[Read the SOC-003 case report](investigations/SOC-003-network-traffic-investigation.md)

## Skills practiced
- Linux command-line administration and journal log review
- Authentication event analysis and timeline correlation
- Differentiating controlled test activity from potentially suspicious behavior
- Network packet capture with tcpdump and protocol/conversation analysis in Wireshark
- TCP handshake, DNS, and TLS Client Hello/SNI interpretation
- Writing investigation notes with evidence limitations

## Scope and ethics
All activity was conducted in an isolated, personally controlled lab. No unauthorized access or real-world attack is claimed. This is a learning portfolio, not production SOC employment experience.

## Evidence policy
Reports distinguish confirmed exercise observations from unverified details. No fabricated timestamps, alert IDs, screenshots, or tool outputs are included. Redact usernames, addresses, credentials, and secrets as needed before publishing.

## Author
Jerai Padilla · [GitHub](https://github.com/levetteit)
