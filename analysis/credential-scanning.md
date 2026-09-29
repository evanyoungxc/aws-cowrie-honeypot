# Automated SSH Credential Scanning

On September 27, 2026, my Cowrie honeypot captured a large automated SSH credential scanning attempt from a single source IP.

The scanner tested many different username and password combinations and attempted to verify whether each successful login provided a working shell.

## Attack Activity

The activity originated from:

`91.237.85.238`

The connections shared the HASSH fingerprint:

`1ecd42383b6cd16084a022b0286d41ce`

A large number of SSH sessions were created within a short period of time. The scanner tested credentials associated with Linux systems, network devices, virtual machines, and other software.

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

## Credential Validation

After a successful login, the scanner repeatedly executed:

```text
echo SSH_TEST_OK
