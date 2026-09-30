# Cowrie Honeypot Dashboard

I built a web dashboard for my AWS Cowrie honeypot to make the captured activity easier to monitor and analyze.

The dashboard is hosted on the same AWS EC2 instance as the honeypot and is served using Nginx. A Python script processes the Cowrie JSON logs and creates a sanitized JSON file containing statistics and recent activity. A systemd timer runs the script every minute, while the webpage checks for updated data every 30 seconds.

## Current Features

- Total SSH connections
- Unique source IPs
- Successful and failed logins
- Captured file events
- Top source IPs
- Top usernames
- Top commands
- Recent commands
- HASSH fingerprints

## Architecture

Cowrie logs → Python parser → sanitized JSON → Nginx → web dashboard

Raw Cowrie logs, captured malware, credentials, and SSH keys are not exposed through the dashboard.

## Screenshots

Dashboard screenshots will be added here.
