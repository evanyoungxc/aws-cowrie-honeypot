# Recurring PANCHAN Activity

After initially capturing PANCHAN malware on September 17, 2026, the honeypot
continued to observe SSH sessions with behavior matching the original attack.

## Initial Capture

The first PANCHAN sample was captured on September 17 and is analyzed separately
in [panchan.md](panchan.md).

## Recurring Activity

| Date | Source IP | Credential | HASSH | Uploaded File | SHA-256 |
|------|-----------|------------|-------|---------------|---------|
| Sep 17 | 146.59.99.179 | root/ubuntu | 98ddc560... | sshd | 94f2e4d8... |
| Sep 22 | 101.47.134.74 | root/ubuntu | 98ddc560... | sshd | 94f2e4d8... |
| Sep 25 | 36.163.118.108 | root/centos | 98ddc560... | sshd | c6f5414f... |
| Sep 29 | 175.100.126.149 | root/ubuntu | 98ddc560... | sshd | 8e730cdd... |

## September 29 Capture

On September 29, another SSH session authenticated using root/ubuntu and
uploaded a file named sshd through SFTP.

The captured file was a 64-bit x86-64 ELF with a size of 29,655,040 bytes.
Static analysis found several strings directly associated with PANCHAN:

- `pan-chan's mining island hi!`
- `panchansminingisland`
- `panchansminingisland/miner.go`
- `panchansminingisland/p2p.go`
- `panchansminingisland/rootkit.go`
- `panchansminingisland/spreader.go`
- `panchansminingisland/updater.go`

The file appeared incomplete because its ELF metadata referenced section headers
beyond the end of the captured file.

## Pattern

Across these sessions, several characteristics repeatedly appeared:

- SSH client identified as `SSH-2.0-Go`
- HASSH fingerprint `98ddc5604ef6a1006a2b49a58759fbe6`
- Root account authentication
- SFTP transfer of a file named `sshd`
- PANCHAN-related payloads
- Similar delivery behavior across multiple source IP addresses

The repeated behavior suggests the honeypot is encountering the same or closely
related automated PANCHAN deployment activity over time. The matching behavior
does not prove that the individual source IP addresses are controlled by the
same operator.
