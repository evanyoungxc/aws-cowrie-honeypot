# Automated SSH Credential Scanning

My Cowrie honeypot has captured multiple automated SSH credential scanning campaigns. These scanners tested large lists of username and password combinations and then executed simple commands after successful authentication to verify access to the system.

## September 27 Credential Scanner

On September 27, 2026, a large credential scanning attempt originated from:

`91.237.85.238`

The connections shared the HASSH fingerprint:

`1ecd42383b6cd16084a022b0286d41ce`

The scanner tested credentials associated with Linux systems, network devices, virtual machines, and other software.

Some examples included:

- `pi/raspberry`
- `ubuntu/ubuntu`
- `cisco/cisco`
- `vagrant/vagrant`
- `netscreen/netscreen`
- `admin/pfsense`
- `root/alpine`
- `root/freenas`
- `root/openvpnas`
- `Administrator/p@ssw0rd`

### Credential Validation

After a successful login, the scanner repeatedly executed:

```text
echo SSH_TEST_OK
```

This appears to have been a simple check to determine whether the tested credentials resulted in access to a working shell.

No file transfers or additional post-authentication commands were observed.

## September 29 Credential Scanner

On September 29, another automated credential scanning campaign was observed from:

`109.160.32.104`

These connections identified themselves as:

`SSH-2.0-Go`

and shared the HASSH fingerprint:

`0a07365cc01fa9fc82608ba4019af499`

The scanner rapidly tested many different credentials, including:

- `root/linux123456789`
- `tom/tom`
- `deploy/dev`
- `openvpn/openvpn`
- `worker/worker`
- `ubuntu/1qaz@WSX`
- `kali/kali`
- `azureuser/azureuser`
- `root/abc123`

### System Validation

Unlike the September 27 scanner, successful logins were followed by:

```text
uname -s -v -n -r -m
```

This command collects basic operating system and kernel information. The repeated pattern suggests the scanner was checking both whether the credentials worked and what type of system it had accessed.

The same SSH client behavior and HASSH fingerprint appeared throughout the campaign. A search of the existing honeypot logs found this HASSH only during the September 29 activity from `109.160.32.104`.

No file transfers, malware execution, or SSH forwarding were observed.

## Analysis

Both campaigns demonstrate how automated SSH scanners can move beyond simply testing passwords.

The September 27 scanner used a basic shell validation command:

```text
credential → login → echo SSH_TEST_OK
```

The September 29 scanner performed basic system identification:

```text
credential → login → uname -s -v -n -r -m
```

Although Cowrie recorded many successful authentication sessions, these should not be interpreted as separate attackers. A single automated scanner can generate a large number of sessions while working through its credential list.

## Takeaway

These captures show how exposed SSH services are continuously tested with automated credential lists. They also show how post-authentication commands can help distinguish different scanning behavior even when the overall goal of finding accessible SSH systems is similar.

