# AWS Cowrie Honeypot

A public-facing SSH honeypot deployed on AWS EC2 using Cowrie to capture and analyze real-world malicious activity.

## Project

- Ubuntu EC2 instance hosted on AWS
- Cowrie SSH honeypot exposed to the public internet
- Real administrative SSH separated from the honeypot
- Captures login attempts, commands, sessions, and transferred files
- Python scripts used to analyze Cowrie JSON logs and sessions
- Captured payloads analyzed using hashes and static analysis
- Live web dashboard for monitoring captured honeypot activity

## Live Dashboard

I built a live dashboard to monitor and analyze activity captured by the honeypot.

**Live Dashboard:** http://50.19.18.86/index.html

The dashboard is hosted on the AWS EC2 instance using Nginx. A Python script processes the Cowrie JSON logs and generates sanitized dashboard data automatically every minute.

The dashboard currently displays:

- Total connections and unique source IPs
- Successful and failed logins
- Captured file events
- Top source IPs
- Top usernames
- Top commands
- Recent commands
- HASSH fingerprints

More information can be found in the [dashboard](dashboard/) directory.

## Repository

- `analysis/` - Analysis of notable attacks and captured malware
- `dashboard/` - Live dashboard documentation
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
- Nginx
- systemd
- Git/GitHub
- VirusTotal
