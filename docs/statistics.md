# Honeypot Statistics

Last updated: October 4, 2026

These statistics are generated from the Cowrie JSON logs using the Python analysis scripts included in this repository.

The dataset currently covers activity observed from **September 16 through October 4, 2026**.

## Overall Activity

| **Metric**              | **Count** |
| ----------------------- | --------- |
| Total Connections       | 1,764     |
| Unique Source IPs       | 935       |
| Successful Login Events | 217       |
| Failed Login Events     | 57        |
| Captured File Events    | 56        |
| Interesting Sessions    | 217       |

Successful login events represent Cowrie authentication events and should not be interpreted as 217 separate attackers. Automated scanners and campaigns can generate many successful sessions.

## Top Source IPs

| **Source IP**   | **Connections** |
| --------------- | --------------- |
| 91.237.85.238   | 101             |
| 109.160.32.104  | 39              |
| 150.107.36.236  | 16              |
| 139.19.117.130  | 11              |
| 36.94.137.119   | 11              |
| 36.94.123.203   | 10              |
| 2.57.122.168    | 9               |
| 35.94.132.8     | 8               |
| 139.19.117.129  | 8               |
| 13.57.33.192    | 8               |

## Most Common Usernames

| **Username**  | **Attempts** |
| ------------- | ------------ |
| root          | 180          |
| test          | 13           |
| admin         | 12           |
| pi            | 5            |
| ubuntu        | 3            |
| debian        | 3            |
| Administrator | 2            |
| misp          | 2            |
| default       | 2            |
| deploy        | 2            |

## Most Common Passwords

| **Password** | **Attempts** |
| ------------ | ------------ |
| ubuntu       | 15           |
| admin        | 14           |
| password     | 11           |
| root         | 10           |
| test         | 6            |
| debian       | 5            |
| 123          | 3            |
| raspberry    | 3            |
| video        | 3            |
| 123456       | 3            |

The credential data shows a strong focus on default and weak Linux credentials, particularly attempts targeting the `root` account.

## Most Common Commands

| **Count** | **Command / Activity** |
| --------- | ---------------------- |
| 98 | `echo SSH_TEST_OK` |
| 36 | Create, execute, and remove `filter` shell test |
| 36 | `#!/bin/bash echo "xxxxxx"` |
| 36 | `uname -s -v -n -r -m` |
| 18 | PATH setup and system information collection |
| 8 | `uname -a` |
| 6 | `exit` |
| 5 | `/ip cloud print` |
| 5 | `ifconfig` |
| 5 | `cat /proc/cpuinfo` |
| 5 | Search running processes for miners |
| 5 | Search Telegram/GSM/SMS-related files and devices |
| 5 | `locate D877F783D5D3EF8Cs` |
| 5 | `echo Hi \| cat -n` |

The large number of `echo SSH_TEST_OK` commands came from automated SSH credential scanning that tested default and product-specific credentials and verified successful shell access.

Other recurring commands show automated post-authentication reconnaissance, environment validation, and searches for specific processes, files, and services.

## Top HASSH Fingerprints

| **HASSH** | **Observations** |
| --------- | ---------------: |
| `1ecd42383b6cd16084a022b0286d41ce` | 100 |
| `0a07365cc01fa9fc82608ba4019af499` | 38 |
| `dd9bcf093c355da7000132131cb36fd0` | 27 |
| `98ddc5604ef6a1006a2b49a58759fbe6` | 27 |
| `e54ef3ec27fe1fea7ab64d3fa05359fd` | 25 |
| `2ec37a7cc8daf20b10e1ad6221061ca5` | 23 |
| `16443846184eafde36765c9bab2f4397` | 20 |
| `9052c4ab4164c78256e71143dcfc7eac` | 20 |
| `f1e5e9d24e5e345e8745613bde22d532` | 19 |
| `87e3d9ffee0540b0390f8a5b9c343c08` | 16 |

HASSH fingerprints are useful for correlating SSH clients based on their key-exchange behavior, but a fingerprint alone should not be treated as identification of a specific attacker or malware family.

## SSH Payload Campaign

One of the most significant patterns observed in the honeypot was repeated deployment of an SSH-focused Linux payload.

The associated HASSH fingerprint:

`98ddc5604ef6a1006a2b49a58759fbe6`

appeared in:

- **27 sessions**
- **22 unique source IPs**
- **18 `sshd` upload events**
- **7 complete captures of the same payload**

The complete payload had the SHA-256 hash:

`94f2e4d8d4436874785cd14e6e6d403507b8750852f7f2040352069a75da4c00`

Complete copies were uploaded from seven different source IP addresses between September 17 and October 3.

Later sessions launched the payload with large lists of IP addresses as command-line arguments, suggesting automated targeting or propagation behavior.

Several additional `sshd` files initially appeared to be different payloads because they had different SHA-256 hashes. Byte-for-byte comparison showed that these files were actually **truncated transfers of the same 30.3 MB binary**.

More details are available in the [SSH Propagation Payload Analysis](analysis/ssh-propagation-payload.md).

## Notable Activity

Analysis of the honeypot traffic has identified several types of malicious or suspicious activity:

- Repeated deployment of an SSH-focused Linux payload
- Automated SSH credential attacks and weak-password scanning
- Large-scale automated post-authentication reconnaissance
- PANCHAN-related payload activity
- PIMINE Raspberry Pi worm activity
- Credential and environment validation
- SSH tunneling and proxy attempts
- Searches for cryptocurrency mining processes
- Searches for Telegram, GSM modem, and SMS-related resources
- Repeated file transfers and payload execution attempts

Detailed investigations of selected activity are available in the [`analysis/`](analysis/) directory.

## Notes

These statistics represent activity observed by this honeypot and are not intended to represent Internet-wide attack statistics.

Several categories overlap. A single session may contain successful authentication, reconnaissance, file transfer, and payload execution attempts.

HASSH fingerprints are used as correlation indicators rather than direct attribution.

The honeypot also contains a small amount of known testing traffic from my own systems. Future versions of the analysis scripts will filter known testing activity from the public statistics.
