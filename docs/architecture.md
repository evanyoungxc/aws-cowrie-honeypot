# Honeypot Architecture

## Overview

The honeypot runs on an Ubuntu AWS EC2 instance with Cowrie providing the public-facing SSH environment. I wanted traffic sent to the normal SSH port to reach Cowrie while keeping the real administrative SSH service separate.

The setup uses an AWS Security Group, iptables port redirection, Cowrie, OpenSSH, and Nginx. I also added a Python-based dashboard pipeline so I can monitor activity without exposing the raw Cowrie logs.

## Network Design

```text
Internet
   |
   |---- TCP 22 (Public)
   |        |
   |        v
   |    iptables redirect
   |      22 -> 2222
   |        |
   |        v
   |    Cowrie SSH
   |
   |---- TCP 22222 (Restricted)
   |        |
   |        v
   |    Real OpenSSH
   |
   |---- TCP 80 (Public)
            |
            v
          Nginx
            |
            v
      Honeypot Dashboard
```

All three services run on the same Ubuntu EC2 instance, but they serve different purposes. Port 22 is used as the public honeypot, port 22222 is used for administration, and port 80 serves the monitoring dashboard.

## Cowrie SSH Service

Cowrie runs under its own unprivileged Linux user rather than running as root.

Internally, Cowrie listens on:

```text
TCP 2222
```

I did not expose port 2222 directly through the AWS Security Group. Instead, SSH traffic reaches the EC2 instance through the normal SSH port:

```text
TCP 22
```

An iptables NAT rule redirects that traffic internally:

```text
TCP 22 -> TCP 2222
```

This allows the honeypot to look like a normal SSH server from the internet while still allowing Cowrie to run on an unprivileged port.

## Administrative SSH

I needed a way to administer the actual Ubuntu server without connecting to Cowrie.

The real OpenSSH service was moved from port 22 to:

```text
TCP 22222
```

Port 22222 is restricted through the AWS Security Group to my current authorized source IP.

This keeps administrative SSH separate from honeypot traffic. Normal internet traffic hitting port 22 reaches Cowrie, while I connect directly to OpenSSH through the restricted management port.

## AWS Security Group

The AWS Security Group provides the first layer of inbound access control.

| Port | Purpose | Access |
|---|---|---|
| TCP 22 | Cowrie honeypot | Public |
| TCP 80 | Monitoring dashboard | Public |
| TCP 22222 | Real OpenSSH administration | Restricted source IP |
| TCP 2222 | Cowrie internal listener | Not publicly exposed |

Cowrie's actual listening port is never directly exposed to the internet.

The administrative port is also not open to the public internet. When my public IP changes, I update the Security Group rule rather than allowing unrestricted access to port 22222.

## Data Collection

Cowrie generates JSON logs containing events from the SSH honeypot.

Some of the information I use for analysis includes:

- Connection source IPs
- Authentication attempts
- Successful Cowrie logins
- SSH client information
- HASSH fingerprints
- Commands entered during sessions
- Session and TTY activity
- SFTP and SCP transfers
- Captured files

The JSON format makes it possible to analyze individual sessions as well as activity across multiple days of rotated logs.

## Dashboard Pipeline

I added a web dashboard so I could monitor the honeypot without manually reading the Cowrie logs every time.

The dashboard uses the following data flow:

```text
Cowrie JSON logs
       |
       v
Python parser
       |
       v
Sanitized data.json
       |
       v
Nginx
       |
       v
Web dashboard
```

The Python script reads the current and rotated Cowrie JSON logs and calculates statistics such as connection counts, unique source IPs, authentication activity, commands, HASSH fingerprints, and file events.

It also groups connections and successful logins by day for the activity graph.

The script writes the results to a separate `data.json` file. Nginx serves this sanitized file along with the HTML dashboard.

The browser never needs direct access to the original Cowrie logs.

## Dashboard Updates

Dashboard generation is automated with a `systemd` service and timer.

The timer runs the Python parser every minute:

```text
Cowrie logs
     |
     | every minute
     v
generate_data.py
     |
     v
data.json
```

The dashboard frontend requests updated data every 30 seconds.

This means new honeypot activity normally appears on the dashboard shortly after it is recorded without requiring me to manually regenerate the data.

## Persistence

I configured the main parts of the environment to survive an EC2 reboot.

Cowrie runs as a `systemd` service and starts automatically when the server boots. The dashboard data generator also uses a `systemd` timer.

The iptables redirect is saved using `iptables-persistent`.

After configuring persistence, I rebooted the instance and verified that:

- Cowrie automatically started on port 2222
- OpenSSH started on port 22222
- The port 22 to 2222 redirect remained active
- Public SSH connections on port 22 reached Cowrie
- Administrative SSH remained available on port 22222
- Nginx served the dashboard
- Dashboard data continued updating automatically

## Separation of Public and Administrative Traffic

One of the main goals of the design was keeping honeypot traffic separate from actual server administration.

```text
Attacker / Scanner
       |
     TCP 22
       |
       v
     Cowrie


Administrator
       |
   TCP 22222
       |
       v
    OpenSSH
```

Someone scanning the normal SSH port interacts with the Cowrie environment rather than the actual Ubuntu SSH service.

## Security Considerations

Because the EC2 instance intentionally accepts untrusted internet traffic, I took several steps to reduce risk:

- Cowrie runs as a dedicated unprivileged Linux user
- Real OpenSSH is separated from the honeypot
- Administrative SSH is restricted by source IP
- Cowrie's internal port is not publicly exposed
- Raw Cowrie logs are not served by Nginx
- Captured passwords are not displayed on the public dashboard
- Captured malware and transferred files are not publicly hosted
- Captured malware is not intentionally executed
- SSH private keys are not stored in the GitHub repository
- Dashboard data is sanitized before being made publicly accessible

The public dashboard only receives the information that the Python parser specifically places into `data.json`.

## Current Architecture

The complete setup currently looks like this:

```text
                         AWS EC2
                            |
          +-----------------+-----------------+
          |                 |                 |
       TCP 22           TCP 22222          TCP 80
       Public           Restricted          Public
          |                 |                 |
          v                 v                 v
      iptables           OpenSSH            Nginx
      22 -> 2222                              |
          |                                   |
          v                                   v
        Cowrie                         Dashboard Files
          |
          v
      JSON Logs
          |
          v
     Python Parser
          |
          v
    Sanitized JSON
          |
          +-------------------------------> Nginx
```

This keeps the honeypot, administrative access, and public monitoring interface logically separated while still allowing them to run on a single EC2 instance.
