import json
import sys
from collections import Counter


def load_events(filenames):
    events = []

    for filename in filenames:
        try:
            with open(filename, "r", encoding="utf-8") as log_file:
                for line in log_file:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            print(f"Warning: Could not find {filename}")

    return events


def shorten(text, length=100):
    text = " ".join(text.split())

    if len(text) > length:
        return text[:length] + "..."

    return text


def analyze(events):
    source_ips = Counter()
    usernames = Counter()
    passwords = Counter()
    commands = Counter()
    hassh_fingerprints = Counter()

    connections = 0
    successful_logins = 0
    failed_logins = 0
    file_events = 0

    for event in events:
        event_id = event.get("eventid", "")
        src_ip = event.get("src_ip")

        if event_id == "cowrie.session.connect":
            connections += 1

            if src_ip:
                source_ips[src_ip] += 1

        elif event_id in ("cowrie.login.success", "cowrie.login.failed"):
            username = event.get("username")
            password = event.get("password")

            if username:
                usernames[username] += 1

            if password:
                passwords[password] += 1

            if event_id == "cowrie.login.success":
                successful_logins += 1
            else:
                failed_logins += 1

        elif event_id == "cowrie.command.input":
            command = event.get("input")

            if command:
                commands[shorten(command)] += 1

        elif event_id == "cowrie.client.kex":
            hassh = event.get("hassh")

            if hassh:
                hassh_fingerprints[hassh] += 1

        elif event_id in (
            "cowrie.session.file_download",
            "cowrie.session.file_upload"
        ):
            file_events += 1

    print("\n=== Cowrie Honeypot Analysis ===\n")

    print(f"Total Connections:      {connections}")
    print(f"Unique Source IPs:      {len(source_ips)}")
    print(f"Successful Logins:      {successful_logins}")
    print(f"Failed Logins:          {failed_logins}")
    print(f"Captured File Events:   {file_events}")

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
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_logs.py <cowrie.json> [more logs...]")
        sys.exit(1)

    events = load_events(sys.argv[1:])

    if not events:
        print("No events were loaded.")
        sys.exit(1)

    analyze(events)


if __name__ == "__main__":
    main()
