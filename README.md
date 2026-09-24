# AWS Cowrie Honeypot

## Overview

This project is an AWS-hosted Cowrie SSH honeypot used to capture and analyze real-world malicious activity targeting an internet-facing SSH service.

The honeypot runs on an Ubuntu EC2 instance and provides a simulated SSH environment while keeping administrative access to the actual server separate. Cowrie collects authentication attempts, commands, SSH client information, session activity, and transferred files for analysis.

I built this project to gain hands-on experience with cloud security, Linux administration, network security, and analysis of real-world attacks.

## Architecture

```text
                         Internet
                            |
              +-------------+-------------+
              |                           |
           TCP/22                      TCP/22222
           Public                   Restricted Access
              |                           |
              v                           v
      AWS Security Group            Real OpenSSH
              |                           |
              v                           v
      iptables REDIRECT               Ubuntu EC2
         22 -> 2222
              |
              v
         Cowrie :2222
              |
      +-------+-------+
      |       |       |
     Auth   Commands  Files
     Logs     Logs    Captured
```

Cowrie runs as an unprivileged user on TCP port `2222`. Public connections to TCP port `22` are redirected to Cowrie using iptables. The real OpenSSH service runs separately on TCP port `22222` and is restricted by source IP through the AWS Security Group.

More information about the setup can be found in [`docs/architecture.md`](docs/architecture.md).

## Technologies

- AWS EC2
- Ubuntu Server
- Cowrie
- OpenSSH
- Linux
- iptables
- systemd
- Bash
- Python
- Git/GitHub
- VirusTotal
- HASSH fingerprinting

## Key Findings

Since deployment, the honeypot has captured:

- Automated SSH credential attacks
- Weak and default credential exploitation
- Post-authentication reconnaissance
- SFTP and SCP file transfers
- Malware deployment attempts
- Linux SSH worms
- Cryptojacking activity
- IRC-based command-and-control behavior
- Recurring attack patterns across different source IP addresses

Two captured payloads were identified as **Panchan** and **PIMINE**.

### Panchan

An attacker authenticated to Cowrie, transferred an ELF executable through SFTP, and attempted to execute it. Static analysis identified the sample as the Panchan Linux cryptojacking and SSH worm.

[View Panchan analysis](analysis/panchan.md)

### PIMINE

An automated attack targeting Raspberry Pi credentials transferred a Bash script through SCP and attempted to execute it. Analysis of the script identified SSH self-propagation, persistence, and IRC command-and-control functionality associated with PIMINE.

[View PIMINE analysis](analysis/pimine.md)

## Repository Structure

```text
aws-cowrie-honeypot/
├── README.md
├── analysis/
│   ├── panchan.md
│   └── pimine.md
└── docs/
    └── architecture.md
```

The `analysis/` directory contains investigations of attacks and captured malware, while `docs/` contains information about the design and configuration of the honeypot.

## Security

Because this system is intentionally exposed to malicious traffic, I separated the honeypot from administrative access to the EC2 instance.

- Cowrie runs under a dedicated unprivileged account.
- Cowrie's internal TCP port `2222` is not publicly exposed.
- Real administrative SSH uses a separate port restricted by source IP.
- Cowrie and the iptables redirect automatically return after a reboot.
- Captured malware is inspected using static analysis and is not executed on the host.
- Private keys, credentials, and malware samples are not stored in this repository.

## Future Development

Planned additions include:

- Python scripts for parsing Cowrie JSON logs
- Attack statistics and visualizations
- HASSH-based session correlation
- Additional attack case studies
- Improved honeypot network isolation and egress controls

## Disclaimer

This project is intended for cybersecurity education and defensive security research. Malware samples and sensitive credentials are not distributed through this repository.
