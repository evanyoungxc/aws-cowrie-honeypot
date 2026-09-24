# PIMINE Raspberry Pi Worm Analysis

## Overview
On September 23, 2026, my Cowrie honeypot captured an automated attack targeting Raspberry Pi systems. The attacker logged into the fake SSH environment using common Raspberry Pi credentials, transferred a Bash script through SCP, and attempted to execute it.

Cowrie captured the script, allowing me to inspect the source code without executing it. The behavior and indicators in the script matched **PIMINE**, a Raspberry Pi-focused SSH worm and backdoor.

## Attack
The source repeatedly attempted to authenticate as `pi` using:

```text
pi / raspberry
pi / raspberryraspberry993311
```

After successfully authenticating to Cowrie, it used SCP to transfer a file into `/tmp` and then attempted to run:

```bash
cd /tmp && chmod +x r1xbtALS && bash -c ./r1xbtALS
```

The uploaded script was captured by Cowrie before it could actually execute.

## Captured File

| | |
|---|---|
| Type | Bash shell script |
| Size | ~4.7 KB |
| SHA-256 | `6d1fe6ab3cd04ca5d1ab790339ee2b6577553bc042af3b7587ece0c195267c9b` |
| Delivery | SCP |

Because this was a readable Bash script, I was able to inspect most of its functionality directly.

## What the Script Does
One of the first things I found was an attempt to gain persistence. If the script was not already running as root, it attempted to use `sudo`, copy itself into `/opt`, modify `/etc/rc.local`, and reboot the machine.

The script also attempted to change the `pi` user's password and add a hard-coded SSH public key to:

```text
/root/.ssh/authorized_keys
```

This would give the attacker another way to maintain access to a successfully compromised machine.

## IRC Command and Control
The script creates another Bash process that connects to IRC servers over TCP port `6667` and joins:

```text
#biret
```

It listens for IRC `PRIVMSG` messages and verifies received data using an embedded RSA public key. If the verification succeeds, the decoded command is passed to Bash:

```bash
CMD=`echo $privmsg_data | base64 -d -i`
RES=`bash -c "$CMD" | base64 -w 0`
```

The command output is then sent back through IRC. This gives the malware remote command execution functionality.

## Self-Propagation
The part I found most interesting was that the script contained the exact behavior I had just observed against my honeypot.

It installs `zmap` and `sshpass`, then repeatedly scans for systems with TCP port 22 open:

```bash
zmap -p 22 -o $FILE -n 100000
```

For discovered systems, it tries the same Raspberry Pi credentials seen in my Cowrie logs. If authentication works, it uses SCP to copy itself to the new system and SSH to execute the copy.

The basic propagation process is:

```text
Scan for TCP/22
      ↓
Try pi credentials
      ↓
SCP script to /tmp
      ↓
SSH into target
      ↓
Make script executable
      ↓
Run script
      ↓
New infected host repeats process
```

This was especially useful because I could directly compare the malware's source code with what Cowrie recorded. The SSH credentials, SCP transfer, `/tmp` location, `chmod`, and execution attempt seen in the logs all matched the propagation code inside the captured script.

## What I Learned
This attack gave me a good example of how a self-propagating worm works from both sides. Cowrie showed what the attack looked like from the target's perspective, while the captured Bash script showed what the attacking system was programmed to do.

Instead of only identifying that a malicious file had been uploaded, I was able to trace the process from credential exploitation and payload delivery to persistence, command and control, and propagation.

The malicious script itself is **not included in this repository**.
