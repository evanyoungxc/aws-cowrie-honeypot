# Panchan Malware Analysis

## Overview
On September 17, 2026, my Cowrie honeypot captured an attacker that successfully logged into the fake SSH environment and uploaded a file named `sshd` through SFTP. The attacker made the file executable and attempted to run it in the background.

Cowrie captured the file instead of allowing it to execute on the actual EC2 server. I then performed static analysis on the sample and identified it as **Panchan**, a Linux cryptojacking and SSH worm.

## Attack
The attacker logged in using:

```text
Username: root
Password: ubuntu
SSH Client: SSH-2.0-Go
```

After logging in, the attacker uploaded `sshd` and attempted to execute it from a randomly named hidden directory:

```bash
chmod +x ./<random-directory>/sshd
nohup ./<random-directory>/sshd &
```

Cowrie saved the transferred file, which allowed me to analyze it without running it.

## Captured File

| | |
|---|---|
| Filename | `sshd` |
| SHA-256 | `94f2e4d8d4436874785cd14e6e6d403507b8750852f7f2040352069a75da4c00` |
| Type | ELF 64-bit x86-64 |
| Size | ~29 MB |
| Language | Go |

I did not execute the sample. I used tools such as `file`, `strings`, hashing, and inspection of the Go metadata to investigate it.

## Identifying Panchan
One of the biggest clues was information left inside the Go binary. The executable contained the module name:

```text
panchansminingisland
```

It also contained original source file paths:

```text
panchansminingisland/killer.go
panchansminingisland/miner.go
panchansminingisland/p2p.go
panchansminingisland/rootkit.go
panchansminingisland/spreader.go
panchansminingisland/updater.go
```

Several function names were also recoverable:

```text
main.killnbminer
main.killxmrig
main.miner
main.p2p
main.p2phandleconnection
main.spreader
main.sshtry
main.startupmanager
main.updater
```

These were useful for understanding what the malware was designed to do even without executing it.

## What the Malware Does
The sample contained references to **XMRig** and **NBMiner**, along with functions such as `main.miner`, `main.killxmrig`, and `main.killnbminer`. This showed that cryptocurrency mining was part of its functionality.

It also included the Go SSH and SFTP packages:

```text
golang.org/x/crypto/ssh
github.com/pkg/sftp
```

Functions such as `main.sshtry` and `main.spreader` were consistent with its ability to spread through SSH.

Another interesting part was the number of P2P-related functions:

```text
main.p2p
main.p2phandleclient
main.p2phandleconnection
main.p2ptry
```

Together with the module name and the other behavior, these findings allowed me to identify the sample as Panchan.

## Attack Flow

```text
SSH Connection
     ↓
root / ubuntu
     ↓
SFTP upload of "sshd"
     ↓
chmod +x
     ↓
nohup execution attempt
     ↓
Cowrie captures file
     ↓
Static analysis
     ↓
Panchan identified
```

## What I Learned
This was the first captured session where I was able to follow an attack from SSH authentication to an actual malware upload. Instead of only seeing failed passwords or scanning activity, Cowrie gave me the payload the attacker attempted to deploy.

The most useful part of the analysis was seeing how much information could still be recovered from a stripped Go executable. The embedded package names, source paths, strings, and function names were enough to learn a lot about the malware without having to execute it.

The malware sample itself is **not included in this repository**.
