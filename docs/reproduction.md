# Reproduction and newly proposed collection commands

## What has been tested

Offline checks use the published historical inputs and separately labeled new synthetic fixtures. Historical validation JSON records describe Python 3.14.8 on Windows; the audit used Python 3.12.14 on Windows. This sprint records its own runtime/results in the [remediation record](documentation-remediation.md). Offline scripts require Python 3.10 or newer and the standard library. Photograph conversion alone additionally requires Pillow; it is not needed to replay the detector.

The Linux commands below are **newly proposed examples**, not recovered historical command transcripts. They have not been run against a live Kali VM during remediation. A fresh run will have different timestamps, PIDs, network traffic and results. Record actual results rather than copying historical values or the example offsets into an observation report.

## Prerequisites and collection directory

Use a personally controlled Kali VM and an account authorized to run `sudo`. The documented VM uses VirtualBox NAT with outbound Internet access; it is not air-gapped. Authenticate only to this VM's loopback address. Capture only traffic from the authorized VM interface. No external target testing is required.

Required tools: Bash, sudo, systemd/journalctl, procps (`ps`), psmisc (`pstree`), iproute2 (`ip`, `ss`), coreutils, dpkg, tcpdump, Wireshark, OpenSSH client/server, and Python. Check availability first; if missing, the following is a proposed Kali/Debian package installation step requiring VM administrator privileges:

```bash
sudo apt update
sudo apt install procps psmisc iproute2 coreutils tcpdump wireshark openssh-client openssh-server python3
```

From the repository root, in one Bash session, create a new private directory. Do not reuse historical evidence paths:

```bash
umask 077
collection_dir=$(mktemp -d "$HOME/soc-lab-new-XXXXXXXX")
date --iso-8601=seconds > "$collection_dir/collection-start.txt"
uname -a > "$collection_dir/kernel.txt"
cat /etc/os-release > "$collection_dir/os-release.txt"
dpkg-query -W -f='${Package}\t${Version}\n' sudo systemd procps psmisc iproute2 coreutils tcpdump wireshark openssh-client openssh-server python3 > "$collection_dir/package-versions.txt"
python3 --version > "$collection_dir/python-version.txt"
```

Inspect command errors and record their statuses. These versions are newly recorded prerequisites, not assumed historical versions. Keep original files in this directory private.

## SOC-001: sudo cache and authentication sequence

The account must require a password for `sudo`; `NOPASSWD` or policy restrictions may change this sequence. Clear this session's cached authorization, then invoke a harmless privileged command:

```bash
soc001_start=$(date -u '+%Y-%m-%d %H:%M:%S.%6N UTC')
printf 'start=%s\n' "$soc001_start" > "$collection_dir/soc001-times.txt"
sudo -k
sudo whoami
printf 'sudo_whoami_exit=%s\n' "$?" > "$collection_dir/soc001-status.txt"
```

At the interactive prompt, enter one intentionally incorrect password, then the correct password at the next prompt. Do not type passwords into a command, script, recording, or repository file. If the policy ends the command after one failure, invoke `sudo whoami` again and authenticate correctly. Record what actually happened; no fixed 21-second interval or historical PID is expected.

```bash
soc001_end=$(date -u '+%Y-%m-%d %H:%M:%S.%6N UTC')
printf 'end=%s\n' "$soc001_end" >> "$collection_dir/soc001-times.txt"
sudo journalctl --since "$soc001_start" --until "$soc001_end" --output=short-iso-precise --no-pager > "$collection_dir/soc001-journal.log"
printf 'journal_export_exit=%s\n' "$?" >> "$collection_dir/soc001-status.txt"
grep -E 'sudo\[|authentication failure' "$collection_dir/soc001-journal.log" > "$collection_dir/soc001-selected.log"
printf 'selection_exit=%s\n' "$?" >> "$collection_dir/soc001-status.txt"
sudo -k
```

Preserve the complete private export before creating a selection. Query bounds use explicit UTC syntax accepted by journalctl; the export uses ISO timestamps with offsets. Correlate actual PID, terminal, account, command, time and offset. Grep exit 1 means no match, not an authenticated clean result. See the [sudo manual](https://manpages.debian.org/bookworm/sudo/sudo.8.en.html), [journalctl manual](https://manpages.debian.org/bookworm/systemd/journalctl.1.en.html), and [systemd time syntax](https://manpages.debian.org/bookworm/systemd/systemd.time.7.en.html).

## SOC-002: dynamic process selection and bounded checks

Create a new process in the same Bash session. Record `$!` immediately; never reuse historical PIDs 3184 or 13846:

```bash
nice -n 5 sleep 600 &
lab_pid=$!
date --iso-8601=seconds > "$collection_dir/soc002-start.txt"
ps -o pid,ppid,user,stat,ni,etime,args -p "$lab_pid" > "$collection_dir/soc002-process.txt"
pstree -sp "$lab_pid" > "$collection_dir/soc002-ancestry.txt"
readlink -f "/proc/$lab_pid/exe" > "$collection_dir/soc002-executable.txt"
sudo ss -tunap > "$collection_dir/soc002-sockets.txt" 2> "$collection_dir/soc002-sockets.stderr.txt"
printf 'ss_exit=%s\n' "$?" > "$collection_dir/soc002-status.txt"
grep -F "pid=$lab_pid," "$collection_dir/soc002-sockets.txt" > "$collection_dir/soc002-socket-selection.txt"
printf 'socket_selection_exit=%s\n' "$?" >> "$collection_dir/soc002-status.txt"
dpkg-query -W coreutils > "$collection_dir/soc002-package-version.txt"
printf 'package_version_exit=%s\n' "$?" >> "$collection_dir/soc002-status.txt"
dpkg -S /usr/bin/sleep > "$collection_dir/soc002-package-owner.txt" 2>&1
printf 'package_owner_exit=%s\n' "$?" >> "$collection_dir/soc002-status.txt"
dpkg -V coreutils > "$collection_dir/soc002-package-verification.txt" 2>&1
printf 'package_verify_exit=%s\n' "$?" >> "$collection_dir/soc002-status.txt"
sha256sum /usr/bin/sleep > "$collection_dir/soc002-sleep.sha256"
kill "$lab_pid"
wait "$lab_pid"
unset lab_pid
```

The final wait normally reflects termination by the cleanup signal. If interrupted or the process has exited, verify the PID is still your created child before signaling it. To study a separate `sleep 1800`, repeat with a newly captured PID and separate output names. Empty filtered sockets do not establish absence of all communication; local package metadata is not an independent trusted reference. The [ps](https://manpages.debian.org/bookworm/procps/ps.1.en.html), [ss](https://manpages.debian.org/bookworm/iproute2/ss.8.en.html), and [dpkg](https://manpages.debian.org/bookworm/dpkg/dpkg.1.en.html) manuals describe these checks.

## SOC-003: bounded authorized capture and analysis

Identify the VM's interface; use `eth0` only if it is actually present and in the authorized scope:

```bash
ip -br addr > "$collection_dir/soc003-interfaces.txt"
capture_iface=eth0
date --iso-8601=seconds > "$collection_dir/soc003-capture-start.txt"
sudo timeout --signal=INT 60s tcpdump -i "$capture_iface" -nn -c 50 -w "$collection_dir/soc003-new.pcap" > "$collection_dir/soc003-capture.stdout.txt" 2> "$collection_dir/soc003-capture.stderr.txt"
capture_status=$?
printf 'capture_exit=%s\n' "$capture_status" > "$collection_dir/soc003-status.txt"
date --iso-8601=seconds > "$collection_dir/soc003-capture-end.txt"
sudo chown "$(id -u):$(id -g)" "$collection_dir/soc003-new.pcap"
chmod 600 "$collection_dir/soc003-new.pcap"
sha256sum "$collection_dir/soc003-new.pcap" > "$collection_dir/soc003-pcap.sha256"
wireshark "$collection_dir/soc003-new.pcap"
```

The capture ends at 50 packets or 60 seconds; timeout status 124 indicates the time bound was reached. Check errors, captured count and drop statistics instead of assuming 50 packets or success. Ordinary VM traffic is enough; do not browse external targets to force historical results. In Wireshark, inspect the packet list, Statistics → Protocol Hierarchy, Statistics → Conversations → TCP, filter `tls.handshake.type == 1`, and check each actual stream index and SNI. Do not assume the old packet numbers, IP, hostname, count or TLS outcome will recur. See the [tcpdump manual](https://manpages.debian.org/bookworm/tcpdump/tcpdump.8.en.html).

Keep the PCAP private. Save the actual hash, absolute timestamps and offset in a new acquisition record; review any public photograph/derivative separately.

## SOC-004: dedicated loopback SSH prerequisites and collection

Offline fixture replay below needs no SSH service. For a new live exercise, use the controlled VM account with a known password, no lockout policy that would make three planned failures unsafe for that account, and a local OpenSSH server host key. Confirm the local host-key fingerprint and validate configuration. This example starts a **temporary separate loopback listener on port 2222**, without changing the existing SSH service or enabling a service at boot:

```bash
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
sudo install -d -m 755 /run/sshd
sudo /usr/sbin/sshd -t -f /dev/null -o HostKey=/etc/ssh/ssh_host_ed25519_key
sudo ss -ltnp 'sport = :2222'
```

If that port is already occupied, stop this example and choose a free loopback test port. If the key or server is absent, complete the package prerequisites first. Do not overwrite existing keys. Start the transient unit only after those checks pass:

```bash
soc004_start=$(date -u '+%Y-%m-%d %H:%M:%S.%6N UTC')
printf 'start=%s\n' "$soc004_start" > "$collection_dir/soc004-times.txt"
sudo systemd-run --unit=soc004-loopback --collect /usr/sbin/sshd -D -e -f /dev/null -p 2222 -o ListenAddress=127.0.0.1 -o HostKey=/etc/ssh/ssh_host_ed25519_key -o PasswordAuthentication=yes -o KbdInteractiveAuthentication=no -o PubkeyAuthentication=no -o UsePAM=yes -o PermitRootLogin=no
sudo systemctl status soc004-loopback --no-pager
sudo ss -ltnp 'sport = :2222'
```

Verify the listener is only `127.0.0.1:2222`. Run the following command **three times interactively**, entering one deliberately wrong password at each prompt. Compare the first host-key prompt with the local fingerprint above before accepting it. Authentication failure is an expected client error, not a successful login:

```bash
ssh -F /dev/null -4 -p 2222 -o UserKnownHostsFile="$collection_dir/known_hosts" -o PreferredAuthentications=password -o PubkeyAuthentication=no -o NumberOfPasswordPrompts=1 "$(id -un)@127.0.0.1"
```

Actual authentication delays may prevent three events from fitting in 60 seconds. Inspect the real timestamps; use synthetic fixtures to test boundary conditions deterministically rather than altering the export.

```bash
soc004_end=$(date -u '+%Y-%m-%d %H:%M:%S.%6N UTC')
printf 'end=%s\n' "$soc004_end" >> "$collection_dir/soc004-times.txt"
sudo journalctl -u soc004-loopback.service --since "$soc004_start" --until "$soc004_end" --output=short-iso-precise --no-pager > "$collection_dir/soc004-journal.log"
printf 'journal_export_exit=%s\n' "$?" > "$collection_dir/soc004-status.txt"
grep -F 'Failed password for ' "$collection_dir/soc004-journal.log" > "$collection_dir/soc004-failures.log"
printf 'selection_exit=%s\n' "$?" >> "$collection_dir/soc004-status.txt"
python3 detections/SOC-004/ssh_detector_v2.py "$collection_dir/soc004-failures.log" > "$collection_dir/soc004-detector.stdout.txt" 2> "$collection_dir/soc004-detector.stderr.txt"
printf 'detector_exit=%s\n' "$?" >> "$collection_dir/soc004-status.txt"
sudo systemctl stop soc004-loopback.service
```

Clean up the transient unit even if testing or export fails. Retain its logs privately. This guide does not claim that historical SSH acquisition used this service or port. See the [OpenSSH client manual](https://man.openbsd.org/ssh) and [sshd configuration manual](https://man.openbsd.org/sshd_config).

## Offline fixtures, output checks, hashing and cleanup

From the repository root:

```bash
python3 tests/SOC-004/generate_fixtures.py --check
python3 tests/SOC-004/run_tests.py
python3 scripts/validate_repository.py
python3 scripts/validate_repository.py --external
```

The generator defines a fixed 2000-01-01 UTC baseline for new tests and checks preserved fixture bytes. To create a separate fresh synthetic set, use `--output-dir local-output/soc004-fixtures`; this does not recover earlier preparation inputs. The runner verifies full expected stdout, both historical sources, original manifest hashes, and optional v2 behavior; no live network/authentication activity occurs.

Hash a new private collection after all files are closed. This new manifest must remain distinct from `evidence/SOC-004/SHA256SUMS.txt`:

```bash
date --iso-8601=seconds > "$collection_dir/collection-end.txt"
(cd "$collection_dir" && find . -type f ! -name SHA256SUMS-new.txt -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS-new.txt)
(cd "$collection_dir" && sha256sum -c SHA256SUMS-new.txt)
```

Retain the directory until evidence retention decisions are made. Close Wireshark, stop the transient SSH unit, terminate only the child process created for the process exercise, and clear cached sudo authorization. No recursive deletion or historical evidence replacement is required. Before publication, follow the [evidence handling checklist](evidence-handling.md).
