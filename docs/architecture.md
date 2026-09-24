# Honeypot Architecture

## Overview
The honeypot runs on an Ubuntu AWS EC2 instance with Cowrie providing the public-facing SSH environment. I wanted connections to the normal SSH port to reach Cowrie while keeping the real administrative SSH service separate.

The final setup uses an AWS Security Group, iptables port redirection, Cowrie, and a separate OpenSSH administrative port.

## Network Design

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

## Cowrie SSH Service
Cowrie runs under its own unprivileged Linux user rather than running as root. The Cowrie SSH service listens internally on:

```text
TCP 2222
```

I did not expose port 2222 directly to the internet. Instead, public SSH traffic arrives on the normal SSH port, TCP 22.

An iptables NAT rule redirects that traffic:

```text
TCP 22 -> TCP 2222
```

This makes the honeypot appear to be a normal SSH server while allowing Cowrie to run on an unprivileged port.

## Administrative SSH
I still needed a way to securely administer the actual EC2 instance without connecting to the honeypot.

The real OpenSSH service was moved from TCP port 22 to:

```text
TCP 22222
```

Access to this port is restricted through the AWS Security Group to an authorized source IP. Public connections to port 22 therefore reach Cowrie, while administrative connections use the separate restricted port.

This separation also reduces the chance of accidentally interacting with the real server while testing the honeypot.

## AWS Security Group
The Security Group acts as the first network access control layer.

The important inbound rules are:

| Port | Purpose | Access |
|---|---|---|
| TCP 22 | Cowrie honeypot | Public |
| TCP 22222 | Real OpenSSH administration | Restricted source IP |
| TCP 2222 | Cowrie internal listener | Not publicly exposed |

I intentionally did not expose Cowrie's internal port directly.

## Persistence
The environment was configured so the honeypot would recover after an EC2 reboot.

Cowrie runs as a `systemd` service and automatically starts when the server boots. The iptables redirect is also saved using `iptables-persistent`.

After configuring persistence, I rebooted the EC2 instance and verified that:

- Cowrie automatically started on port 2222
- OpenSSH started on port 22222
- The port 22 -> 2222 redirect remained active
- Public SSH connections on port 22 still reached Cowrie
- Administrative SSH remained available through port 22222

## Data Collection
Cowrie records several types of information that I use for attack analysis:

```text
Authentication attempts
SSH client information
HASSH fingerprints
Commands entered by attackers
Session/TTY activity
SFTP and SCP transfers
Captured files
Connection source addresses
```

This data makes it possible to reconstruct individual sessions and compare activity across different attackers.

## Security Considerations
Because the honeypot is intentionally exposed to malicious traffic, I took several steps to reduce risk:

- Cowrie runs as a dedicated unprivileged user
- The real SSH service is separated from the honeypot
- Administrative SSH is restricted by source IP
- Cowrie's internal port is not directly exposed
- Captured malware is not executed on the EC2 host
- Private keys and credentials are not stored in this repository

The goal is to collect malicious activity without intentionally making the underlying Ubuntu server vulnerable.
