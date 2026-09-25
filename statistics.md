# Honeypot Statistics

This page contains statistics collected from my AWS Cowrie honeypot. I update these numbers periodically as the honeypot continues to collect activity.

**Last Updated:** September 25, 2026

## Overall Activity

| Statistic | Count |
|---|---:|
| Total SSH Connections | 840 |
| Unique Source IPs | 478 |
| Successful Logins | 43 |
| Failed Logins | 33 |
| File Transfer Events | 31 |
| Unique Captured File Hashes | 8 |
| Interesting Sessions | 43 |

## Session Activity

| Activity | Sessions |
|---|---:|
| Successful Authentication | 43 |
| Post-Auth Command Execution | 26 |
| File Transfer Detected | 20 |
| System Reconnaissance | 18 |
| Payload / Script Execution Attempt | 15 |

Session categories can overlap because a single session may contain multiple types of activity.

## Top Source IPs

| Source IP | Connections |
|---|---:|
| 150.107.36.236 | 16 |
| 139.19.117.130 | 11 |
| 36.94.137.119 | 11 |
| 13.57.33.192 | 8 |
| 2.57.122.168 | 8 |
| 137.155.241.140 | 6 |
| 77.91.71.55 | 6 |
| 80.94.92.55 | 5 |
| 40.86.229.233 | 5 |
| 2.57.122.209 | 5 |

## Most Common Usernames

| Username | Attempts |
|---|---:|
| root | 60 |
| test | 11 |
| pi | 4 |
| admin | 1 |

## Most Common Passwords

| Password | Attempts |
|---|---:|
| admin | 7 |
| test | 6 |
| ubuntu | 6 |
| root | 5 |
| password | 4 |
| 111111 | 2 |
| 123 | 2 |
| 123123 | 2 |
| raspberryraspberry993311 | 2 |
| raspberry | 2 |

## Top HASSH Fingerprints

| HASSH | Sessions |
|---|---:|
| dd9bcf093c355da7000132131cb36fd0 | 15 |
| 2ec37a7cc8daf20b10e1ad6221061ca5 | 13 |
| e54ef3ec27fe1fea7ab64d3fa05359fd | 11 |
| f1e5e9d24e5e345e8745613bde22d532 | 11 |
| 98ddc5604ef6a1006a2b49a58759fbe6 | 10 |
| 9052c4ab4164c78256e71143dcfc7eac | 9 |
| 87e3d9ffee0540b0390f8a5b9c343c08 | 8 |
| 701158e75b508e76f0410d5d22ef9df0 | 7 |
| 16443846184eafde36765c9bab2f4397 | 7 |
| f45fb203c31069bb280067b71ed92ccb | 4 |

## Notable Activity

The honeypot has captured several types of real-world malicious activity, including:

- Automated SSH credential attacks
- Post-authentication system reconnaissance
- File and payload transfers
- Malware deployment attempts
- SSH worm activity
- Cryptocurrency mining malware
- Repeated activity correlated through HASSH fingerprints and command patterns

Detailed investigations of notable activity are available in the [`analysis/`](analysis/) directory.

## Data Collection

Statistics are generated from Cowrie JSON logs using the Python analysis scripts included in this repository. The statistics represent activity observed by this honeypot and are updated periodically.

Raw Cowrie logs and captured malware binaries are not included in this repository.
