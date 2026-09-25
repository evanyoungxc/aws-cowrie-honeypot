# AWS Cowrie Honeypot

A public-facing SSH honeypot deployed on AWS EC2 using Cowrie to capture and analyze real-world malicious activity.

## Project

- Ubuntu EC2 instance hosted on AWS
- Cowrie SSH honeypot exposed to the public internet
- Real administrative SSH separated from the honeypot
- Captures login attempts, commands, sessions, and transferred files
- Python scripts used to analyze Cowrie JSON logs and sessions
- Captured payloads analyzed using hashes and static analysis

## Repository

- `analysis/` - Analysis of notable attacks and captured malware
- `docs/architecture.md` - Honeypot architecture and configuration
- `scripts/` - Python scripts for analyzing Cowrie logs

## Attack Analysis

The honeypot has captured credential attacks, automated reconnaissance, malware deployment, SSH worms, and other malicious activity.

[View attack analysis](analysis/)

## Tools

- AWS EC2
- Ubuntu Linux
- Cowrie
- Python
- Git/GitHub
- VirusTotal
