# SSH Propagation Payload Analysis

While monitoring my AWS Cowrie honeypot, I observed repeated SSH sessions that uploaded a file named `sshd`. What initially appeared to be several different payloads turned out to be repeated deployments and incomplete transfers of the same 30.3 MB Linux executable.

By correlating Cowrie session logs, SSH fingerprints, file hashes, attacker commands, and static analysis of the captured binary, I was able to reconstruct a larger pattern of automated SSH activity.

## Repeated Payload Deployment

The complete payload was captured with the following SHA-256 hash:

`94f2e4d8d4436874785cd14e6e6d403507b8750852f7f2040352069a75da4c00`

Cowrie recorded the complete payload being uploaded from seven different source IP addresses between September 17 and October 3, 2026.

![Repeated sshd payload uploads](../images/malware_upload.png)

The successful deployments followed a consistent pattern:

1. Authenticate to SSH using a weak root credential
2. Upload a file named `sshd` using SFTP
3. Make the file executable with `chmod +x`
4. Launch it in the background using `nohup`
5. Disconnect

Most successful sessions authenticated using:

`root / ubuntu`

The final observed deployment used:

`root / debian`

The first two deployments launched the binary without additional arguments. Beginning September 27, later sessions supplied roughly 50 IP addresses as command-line arguments:

```text
chmod +x ./<directory>/sshd;
nohup ./<directory>/sshd <IP1> <IP2> <IP3> ... &
