# AWS Cowrie Honeypot

A public-facing SSH honeypot deployed on AWS EC2 using Cowrie to capture and analyze real-world malicious activity.

## Live Dashboard

**Dashboard:** http://54.210.18.142/index.html

I built a live monitoring dashboard to visualize activity captured by the honeypot. Cowrie JSON logs are processed by a Python script into sanitized telemetry that is served through Nginx. A systemd timer updates the dashboard data automatically.

The dashboard currently displays:

- Total SSH connections
- Unique source IPs
- Successful and failed logins
- Commands captured
- File transfer events
- Daily connection and successful login activity
- Recent source IPs
- Top source IPs
- Top usernames
- Top HASSH fingerprints
- Recent commands
- Top commands

Raw logs, captured payloads, credentials, and administrative SSH access are not exposed through the dashboard.

## Project

- Ubuntu EC2 instance hosted on AWS
- Persistent Elastic IP
- Cowrie SSH honeypot exposed to the public internet
- Real administrative SSH separated from the honeypot
- Captures login attempts, commands, sessions, and transferred files
- Python scripts used to analyze Cowrie JSON logs and sessions
- Automated web dashboard for monitoring honeypot activity
- Captured payloads analyzed using hashes and static analysis

## Architecture

Internet traffic → AWS EC2 → Cowrie → JSON logs → Python parser → sanitized JSON → Nginx → live dashboard

Public SSH traffic on port 22 is redirected to Cowrie while administrative SSH is separated onto a restricted management port.

## Repository

- `analysis/` - Analysis of notable attacks and captured malware
- `dashboard/` - Dashboard documentation
- `docs/architecture.md` - Honeypot architecture and configuration
- `scripts/` - Python scripts for analyzing Cowrie logs

## Attack Analysis

The honeypot has captured credential attacks, automated reconnaissance, malware deployment, SSH worms, and SSH tunneling/proxy attempts.

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
