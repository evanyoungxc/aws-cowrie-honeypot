import json
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

LOG_DIR = Path("/home/cowrie/cowrie/var/log/cowrie")
OUTPUT = Path("/var/www/html/data.json")

connections = 0
successful_logins = 0
failed_logins = 0
file_events = 0

source_ips = set()

ip_counts = Counter()
usernames = Counter()
commands = Counter()
hassh = Counter()

connections_by_day = Counter()
successful_logins_by_day = Counter()

recent_connections = []
recent_logins = []
recent_commands = []
recent_files = []

log_files = sorted(LOG_DIR.glob("cowrie.json*"))

for log_file in log_files:
    try:
        with log_file.open("r", errors="ignore") as f:
            for line in f:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue

                eventid = event.get("eventid", "")
                ip = event.get("src_ip", "")
                timestamp = event.get("timestamp", "")
                day = timestamp[:10] if timestamp else ""

                if eventid == "cowrie.session.connect":
                    connections += 1

                    if day:
                        connections_by_day[day] += 1

                    if ip:
                        source_ips.add(ip)
                        ip_counts[ip] += 1

                    recent_connections.append({
                        "time": timestamp,
                        "ip": ip
                    })

                elif eventid == "cowrie.login.success":
                    successful_logins += 1

                    if day:
                        successful_logins_by_day[day] += 1

                    username = event.get("username", "")

                    if username:
                        usernames[username] += 1

                    recent_logins.append({
                        "time": timestamp,
                        "ip": ip,
                        "username": username
                    })

                elif eventid == "cowrie.login.failed":
                    failed_logins += 1

                elif eventid == "cowrie.command.input":
                    command = event.get("input", "")

                    if command:
                        commands[command] += 1

                    recent_commands.append({
                        "time": timestamp,
                        "ip": ip,
                        "command": command
                    })

                elif eventid == "cowrie.client.kex":
                    fingerprint = event.get("hassh", "")

                    if fingerprint:
                        hassh[fingerprint] += 1

                elif eventid in (
                    "cowrie.session.file_upload",
                    "cowrie.session.file_download"
                ):
                    file_events += 1

                    recent_files.append({
                        "time": timestamp,
                        "ip": ip,
                        "event": eventid,
                        "shasum": event.get("shasum", "")
                    })

    except (OSError, PermissionError):
        continue

recent_connections.sort(key=lambda x: x["time"], reverse=True)
recent_logins.sort(key=lambda x: x["time"], reverse=True)
recent_commands.sort(key=lambda x: x["time"], reverse=True)
recent_files.sort(key=lambda x: x["time"], reverse=True)

all_days = sorted(
    set(connections_by_day.keys()) |
    set(successful_logins_by_day.keys())
)

activity_by_day = [
    {
        "date": day,
        "connections": connections_by_day[day],
        "successful_logins": successful_logins_by_day[day]
    }
    for day in all_days
]

data = {
    "generated_at": datetime.now(timezone.utc).isoformat(),

    "connections": connections,
    "unique_ips": len(source_ips),
    "successful_logins": successful_logins,
    "failed_logins": failed_logins,
    "file_events": file_events,
    "commands_captured": sum(commands.values()),

    "activity_by_day": activity_by_day,

    "top_ips": ip_counts.most_common(10),
    "top_usernames": usernames.most_common(10),
    "top_commands": commands.most_common(10),
    "top_hassh": hassh.most_common(10),

    "recent_connections": recent_connections[:15],
    "recent_logins": recent_logins[:15],
    "recent_commands": recent_commands[:15],
    "recent_files": recent_files[:10]
}

with OUTPUT.open("w") as f:
    json.dump(data, f, indent=2)

print("Dashboard data generated")
print(f"Log files processed: {len(log_files)}")
print(f"Connections: {connections}")
print(f"Unique IPs: {len(source_ips)}")
print(f"Successful logins: {successful_logins}")
print(f"Failed logins: {failed_logins}")
print(f"File events: {file_events}")
print(f"Commands captured: {sum(commands.values())}")
print(f"HASSH fingerprints: {sum(hassh.values())}")
