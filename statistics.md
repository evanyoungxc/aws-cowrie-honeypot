# Honeypot Statistics

Last updated: September 29, 2026

These statistics are generated from the Cowrie JSON logs using the Python analysis scripts included in this repository.

## Overall Activity

| Metric | Count |
|---|---:|
| Total Connections | 1,305 |
| Unique Source IPs | 691 |
| Successful Login Events | 153 |
| Failed Login Events | 39 |
| Captured File Events | 41 |
| Interesting Sessions | 153 |

Successful login events represent Cowrie authentication events and should not be interpreted as 153 separate attackers. Automated scanners can create many successful sessions during a single campaign.

## Top Source IPs

| Source IP | Connections |
|---|---:|
| 91.237.85.238 | 101 |
| 150.107.36.236 | 16 |
| 139.19.117.130 | 11 |
| 36.94.137.119 | 11 |
| 36.94.123.203 | 10 |
| 2.57.122.168 | 9 |
| 13.57.33.192 | 8 |
| 137.155.241.140 | 6 |
| 77.91.71.55 | 6 |
| 80.94.92.55 | 5 |

`137.155.241.140` is known testing traffic from my own system and is included in the raw statistics above.

## Most Common Usernames

| Username | Attempts |
|---|---:|
| root | 123 |
| test | 11 |
| admin | 11 |
| pi | 5 |
| debian | 3 |
| Administrator | 2 |
| misp | 2 |
| default | 2 |
| pyimagesearch | 1 |
| nao | 1 |

## Most Common Passwords

| Password | Attempts |
|---|---:|
| ubuntu | 12 |
| admin | 12 |
| password | 10 |
| root | 9 |
| test | 6 |
| raspberry | 3 |
| debian | 3 |
| video | 3 |
| 111111 | 2 |
| 123 | 2 |

## Most Common Commands

| Count | Command |
|---:|---|
| 98 | `echo SSH_TEST_OK` |
| 26 | Create and execute `filter` shell test |
| 26 | `#!/bin/bash echo "xxxxxx"` |
| 13 | System information / environment collection |
| 8 | `uname -a` |
| 5 | `whoami` |
| 5 | `exit` |
| 5 | `/ip cloud print` |
| 5 | `ifconfig` |
| 5 | `cat /proc/cpuinfo` |

The large number of `echo SSH_TEST_OK` commands came from an automated SSH credential scanner that tested many default and product-specific credentials and verified successful shell access.

## Top HASSH Fingerprints

| HASSH | Observations |
|---|---:|
| `1ecd42383b6cd16084a022b0286d41ce` | 100 |
| `dd9bcf093c355da7000132131cb36fd0` | 19 |
| `e54ef3ec27fe1fea7ab64d3fa05359fd` | 17 |
| `2ec37a7cc8daf20b10e1ad6221061ca5` | 17 |
| `98ddc5604ef6a1006a2b49a58759fbe6` | 16 |
| `9052c4ab4164c78256e71143dcfc7eac` | 13 |
| `f1e5e9d24e5e345e8745613bde22d532` | 11 |
| `16443846184eafde36765c9bab2f4397` | 8 |
| `87e3d9ffee0540b0390f8a5b9c343c08` | 8 |
| `701158e75b508e76f0410d5d22ef9df0` | 7 |

## Notable Activity

Analysis of the honeypot traffic has identified several different types of activity:

- PANCHAN malware deployment and recurring PANCHAN-related payload transfers
- PIMINE Raspberry Pi worm activity
- Automated post-authentication system reconnaissance
- Automated default and weak credential scanning
- Credential and environment validation
- SSH tunneling and proxy attempts
- Repeated file transfers and payload execution attempts

More detailed investigation of these events is available in the [`analysis/`](analysis/) directory.

## Notes

These statistics represent activity observed by this honeypot and are not intended to represent Internet-wide attack statistics.

Several categories overlap. For example, one session may contain successful authentication, reconnaissance, file transfer, and payload execution.

The honeypot also contains a small amount of known testing traffic from my own systems. Future versions of the analysis scripts will filter this traffic from the public statistics.
