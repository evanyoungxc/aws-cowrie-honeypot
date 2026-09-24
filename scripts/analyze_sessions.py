import json
import sys
from collections import defaultdict


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


def build_sessions(events):
    sessions = defaultdict(lambda: {
        "src_ip": None,
        "username": None,
        "password": None,
        "hassh": None,
        "commands": [],
        "files": [],
        "login_success": False
    })

    for event in events:
        session_id = event.get("session")

        if not session_id:
            continue

        session = sessions[session_id]
        event_id = event.get("eventid", "")

        if event.get("src_ip"):
            session["src_ip"] = event["src_ip"]

        if event_id == "cowrie.client.kex":
            session["hassh"] = event.get("hassh")

        elif event_id == "cowrie.login.success":
            session["login_success"] = True
            session["username"] = event.get("username")
            session["password"] = event.get("password")

        elif event_id == "cowrie.command.input":
            command = event.get("input")

            if command:
                session["commands"].append(command)

        elif event_id in (
            "cowrie.session.file_upload",
            "cowrie.session.file_download"
        ):
            session["files"].append({
                "event": event_id,
                "filename": event.get("filename"),
                "shasum": event.get("shasum")
            })

    return sessions


def classify(session):
    findings = []

    commands = "\n".join(session["commands"]).lower()

    if session["login_success"]:
        findings.append("Successful authentication")

    if session["commands"]:
        findings.append("Post-auth command execution")

    if session["files"]:
        findings.append("File transfer detected")

    recon_terms = [
        "uname",
        "whoami",
        "ifconfig",
        "/proc/cpuinfo",
        "lspci",
        "nproc"
    ]

    if any(term in commands for term in recon_terms):
        findings.append("System reconnaissance")

    execution_terms = [
        "chmod +x",
        "nohup",
        "bash -c",
        "./"
    ]

    if any(term in commands for term in execution_terms):
        findings.append("Payload/script execution attempt")

    return findings


def print_sessions(sessions):
    interesting = 0

    for session_id, session in sessions.items():

        if not (
            session["login_success"]
            or session["commands"]
            or session["files"]
        ):
            continue

        interesting += 1

        print("\n" + "=" * 65)
        print(f"Session:   {session_id}")
        print(f"Source IP: {session['src_ip']}")

        if session["username"]:
            print(f"Username:  {session['username']}")
            print(f"Password:  {session['password']}")

        if session["hassh"]:
            print(f"HASSH:     {session['hassh']}")

        if session["commands"]:
            print("\nCommands:")

            for command in session["commands"]:
                command = " ".join(command.split())

                if len(command) > 120:
                    command = command[:120] + "..."

                print(f"  - {command}")

        if session["files"]:
            print("\nFile Events:")

            for file_event in session["files"]:
                print(
                    f"  - {file_event['event']} | "
                    f"{file_event['filename']} | "
                    f"{file_event['shasum']}"
                )

        print("\nClassification:")

        for finding in classify(session):
            print(f"  [!] {finding}")

    print("\n" + "=" * 65)
    print(f"Interesting Sessions: {interesting}")


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python3 analyze_sessions.py "
            "<cowrie.json> [more logs...]"
        )
        sys.exit(1)

    events = load_events(sys.argv[1:])

    if not events:
        print("No events were loaded.")
        sys.exit(1)

    sessions = build_sessions(events)
    print_sessions(sessions)


if __name__ == "__main__":
    main()
