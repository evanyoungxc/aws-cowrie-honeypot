# AWS Cowrie Honeypot
## Overview
This project is an AWS-hosted Cowrie SSH honeypot designed to capture and analyze real-world malicious activity targeting an internet-facing SSH service.
The honeypot runs on an Ubuntu EC2 instance and exposes a simulated SSH environment to the public internet while keeping administrative access to the actual server separate. Cowrie records authentication attempts, attacker commands, SSH client information, session activity, and transferred files for later analysis.
The goal of this project is to gain hands-on experience with cloud security, Linux administration, network security, threat analysis, and malware analysis using real-world attack data.
## Architecture
                    Internet
                       |
                    TCP/22
                       |
                       v
               AWS Security Group
                       |
                       v
                iptables REDIRECT
                   22 -> 2222
                       |
                       v
                 Cowrie Honeypot
                       |
          +------------+------------+
          |            |            |
     Auth Logs     Command Logs   File Capture
          |            |            |
          +------------+------------+
                       |
                       v
                    Analysis

Administrative Access
        |
        | TCP/22222
        | Restricted by source IP
        v
    Real OpenSSH
        |
        v
    Ubuntu EC2
```
Cowrie runs as an unprivileged user on TCP port `2222`. Incoming connections to the standard SSH port (`22`) are redirected to Cowrie using an iptables rule.
The real OpenSSH service uses a separate administrative port and is restricted at the AWS Security Group level.

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
Since deployment, the honeypot has captured multiple forms of real-world malicious activity, including:
- Automated SSH credential attacks
- Weak and default credential exploitation
- Post-authentication system reconnaissance
- SFTP and SCP file transfers
- Malware deployment attempts
- Linux SSH worm activity
- Cryptojacking malware
- IRC-based command-and-control behavior
- Recurring automated attack patterns across different source IP addresses

Captured activity has included identifiable malware families such as **Panchan** and **PIMINE**.
Detailed investigations are documented separately in the `analysis/` directory.

## Repository Structure
```text
aws-cowrie-honeypot/
│
├── README.md
│
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   └── security.md
│
├── analysis/
│   ├── panchan.md
│   ├── pimine.md
│   └── ssh-attack-analysis.md
│
├── screenshots/
│
└── scripts/
    └── analyze_logs.py
```

### `docs/`
Contains documentation covering the design, deployment, and security configuration of the honeypot.

### `analysis/`
Contains detailed investigations of attacks and malware captured by the honeypot.

### `screenshots/`
Contains sanitized screenshots demonstrating the honeypot configuration and captured activity.

### `scripts/`
Contains scripts developed to process and analyze Cowrie logs and attack data.

## Security Design
Several precautions were taken to separate the honeypot from administrative access to the underlying server.
- Cowrie runs under a dedicated unprivileged Linux account.
- Cowrie listens internally on TCP port `2222`.
- Public TCP port `22` is redirected to Cowrie using iptables.
- The actual OpenSSH administrative service uses a separate port.
- Administrative SSH access is restricted by source IP through the AWS Security Group.
- Cowrie and the network redirect are configured to persist across reboots.
- Captured malware is analyzed statically rather than executed on the host.

## Project Goals
This project was created to develop practical experience in:
- Deploying and securing an internet-facing cloud server
- Linux system administration
- AWS networking and security controls
- Honeypot deployment and monitoring
- SSH attack analysis
- Log analysis
- Malware identification and static analysis
- Identifying patterns across attacker sessions
- Developing tools to automate security-data analysis

## Future Development
Future additions to the project may include:
- Automated parsing of Cowrie JSON logs
- Attack statistics and visualizations
- Source IP and authentication-attempt analysis
- Automated session correlation using HASSH fingerprints
- Malware hash and file analysis
- Additional attack case studies
- Improved network isolation and egress controls

## Disclaimer
This project is intended solely for cybersecurity education and defensive security research.
Malware samples, private keys, AWS credentials, administrative IP addresses, and other sensitive information are not included in this repository. Captured malicious files are analyzed in an isolated and controlled manner and are not distributed through this project.
