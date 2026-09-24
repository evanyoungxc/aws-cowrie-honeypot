# Recurring Automated SSH Reconnaissance

## Overview

Between September 18 and September 20, 2026, my Cowrie honeypot captured three SSH sessions from three different source IP addresses that followed the same authentication and reconnaissance pattern.

Each connection first attempted to log in using `root:root`, then successfully authenticated using `root:admin`. After authentication, the same sequence of reconnaissance commands was executed.

The three sessions also shared the same HASSH fingerprint, indicating that the SSH clients presented the same SSH algorithm configuration.

## Observed Sessions

| Date | Source IP | Session ID |
|------|-----------|------------|
| 9/18/2026 | 80.180.212.218 | 1124cb658546 |
| 9/19/2026 | 201.143.104.199 | 3768a7753abb |
| 9/20/2026 | 187.158.41.136 | e002e30d2041 |

HASSH fingerprint:

`f45fb203c31069bb280067b71ed92ccb`

## Authentication Pattern

All three sessions attempted the exact same credentials in the same order:

`root:root` - Failed

`root:admin` - Successful

The repeated credential pattern across different source IP addresses was one indicator that the activity was automated.

## Commands Executed

After successfully authenticating, each session executed the same commands:

```bash
/ip cloud print
ifconfig
uname -a
cat /proc/cpuinfo
ps | grep '[Mm]iner'
ps -ef | grep '[Mm]iner'
ls -la ~/.local/share/TelegramDesktop/tdata /home/*/.local/share/TelegramDesktop/tdata /dev/ttyGSM* /dev/ttyUSB-mod* /var/spool/sms/* /var/log/smsd.log /etc/smsd.conf* /usr/bin/qmuxd /var/qmux_connect_socket /etc/config/simman /dev/modem* /var/config/sms/*
locate D877F783D5D3EF8Cs
echo Hi | cat -n
