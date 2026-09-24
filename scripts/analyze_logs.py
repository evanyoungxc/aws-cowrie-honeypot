import json
import sys
from collections import Counter


def load_events(filename):
    events = []

    with open(filename, "r", encoding="utf-8") as log_file:
        for line in log_file:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return events


def analyze(events):
    source_ips = Counter()
    usernames = Counter()
    passwords = Counter()
    commands = Counter()
    hassh_fingerprints = Counter()

    connections = 0
    successful_logins = 0
    failed_logins = 0
    downloads = 0

    for event in events:
        event_id = event.get("eventid", "")
        src_ip = event.get("src_ip")

        if event_id == "cowrie.session.connect":
            connections += 1
            if src_ip:
                source_ips[src_ip] += 1

        elif event_id == "cowrie.login.success":
            successful_logins += 1

            username = event.get("username")
            password = event.get("password")

            if username:
                usernames[username] += 1
            if password:
                passwords[password] += 1

        elif event_id == "cowrie.login.failed":
            failed_logins += 1

            username = event.get("username")
            password = event.get("password")

            if username:
                usernames[username] += 1
            if password:
                passwords[password] += 1

        elif event_id == "cowrie.command.input":
            command = event.get("input")
            if command:
                commands[command] += 1

        elif event_id == "cowrie.client.fingerprint":
            hassh = event.get("hassh")
            if hassh:
                hassh_fingerprints[hassh] += 1

        elif event_id in ("cowrie.session.file_download", "cowrie.session.file_upload"):
            downloads += 1

    print("\n=== Cowrie Honeypot Analysis ===\n")

    print(f"Total Connections:      {connections}")
    print(f"Unique Source IPs:      {len(source_ips)}")
    print(f"Successful Logins:      {successful_logins}")
    print(f"Failed Logins:          {failed_logins}")
    print(f"Captured File Events:   {downloads}")

    print("\nTop Source IPs:")
    for ip, count in source_ips.most_common(10):
        print(f"  {ip:<20} {count}")

    print("\nTop Usernames:")
    for username, count in usernames.most_common(10):
        print(f"  {username:<20} {count}")

    print("\nTop Passwords:")
    for password, count in passwords.most_common(10):
        print(f"  {password:<20} {count}")

    print("\nTop Commands:")
    for command, count in commands.most_common(10):
        print(f"  {count:<5} {command}")

    print("\nTop HASSH Fingerprints:")
    for fingerprint, count in hassh_fingerprints.most_common(10):
        print(f"  {fingerprint}  {count}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_logs.py <cowrie.json>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        events = load_events(filename)
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        sys.exit(1)

    analyze(events)


if __name__ == "__main__":
    main()
