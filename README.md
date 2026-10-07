# AWS Cowrie Honeypot

An internet-facing SSH honeypot deployed on AWS EC2 to capture, monitor, and analyze real-world malicious activity.

I built this project to gain hands-on experience with honeypots, Linux security monitoring, AWS infrastructure, and threat analysis. Cowrie collects SSH connections, authentication attempts, commands, file transfers, and SSH fingerprints from systems interacting with the honeypot.

I also built a public dashboard to visualize sanitized honeypot telemetry and provide access to documented threat investigations.

![Cowrie Honeypot Dashboard](images/dashboard.png)

## Live Dashboard

**Dashboard:** https://honeypot.eyoungcyber.com

The dashboard provides a live view of activity captured by the honeypot, including:

- Total SSH connections
- Unique source IPs
- Successful and failed authentication attempts
- Recent attacker commands
- Top source IPs and usernames
- HASSH fingerprints
- Captured file events
- Daily connection and authentication activity

Cowrie JSON logs are processed with Python into sanitized telemetry that is served through Nginx. Dashboard data is regenerated automatically using a systemd timer.

## Threat Analysis

The website includes a dedicated **Threat Analysis** section containing investigations based on activity captured by the honeypot.

Current investigations include:

- [Raspberry Pi SSH Worm](analysis/raspberry-pi-worm.md)
- [SSH Propagation Payload](analysis/ssh-propagation-payload.md)
- [SSH Credential Validation Activity](analysis/ssh-credential-validation.md)
- [SSH Tunneling](analysis/ssh-tunneling.md)
- [Automated Reconnaissance](analysis/automated-reconnaissance.md)
- [Credential Scanning](analysis/credential-scanning.md)
- [PIMINE Activity](analysis/pimine.md)
- [PANCHAN Investigation](analysis/panchan.md)
- [Recurring PANCHAN Activity](analysis/panchan-recurring-activity.md)

These reports document command sequences, authentication behavior, SSH fingerprints, file transfers, and captured payloads.

Captured files are treated as untrusted and analyzed statically rather than intentionally executed. Attribution is kept conservative when the available evidence does not support identifying a specific actor or malware family.

## Architecture

```text
Internet
   |
AWS EC2
   |
Public SSH :22
   |
iptables redirect
   |
Cowrie SSH :2222
   |
Cowrie JSON Logs
   |
Python Analytics
   |
Sanitized data.json
   |
Nginx
   |
Dashboard + Threat Analysis
```

Public SSH traffic is redirected to Cowrie running as an unprivileged service. Administrative SSH is separated from the honeypot and restricted using AWS Security Group rules.

## Repository Structure

```text
analysis/    Threat-analysis reports
dashboard/   Dashboard frontend and data generator
docs/        Architecture and project documentation
images/      Dashboard and investigation screenshots
scripts/     Cowrie log and session analysis tools
```

## Security

The public website exposes only sanitized telemetry. Raw Cowrie logs, captured credentials, transferred payloads, private keys, and administrative access are not publicly exposed.

## Technologies

AWS EC2 · Ubuntu Linux · Cowrie · Python · Nginx · systemd · iptables · SSH · Git · GitHub

## Disclaimer

This project is intended for cybersecurity education, defensive research, and analysis. The honeypot operates on infrastructure I control.
