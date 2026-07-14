#!/usr/bin/env python3
"""Read-only environment diagnostics for the textbook-to-Anki workflow."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any


REQUIRED_PACKAGES = {"pypdf": "pypdf", "PIL": "Pillow"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only check of Python packages, Node/npx, Anki, ports 3141/8765, "
            "and the harmless AnkiConnect version action."
        )
    )
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="Connection timeout in seconds (default: 0.5)",
    )
    return parser.parse_args()


def package_status() -> dict[str, bool]:
    return {
        distribution: importlib.util.find_spec(module) is not None
        for module, distribution in REQUIRED_PACKAGES.items()
    }


def command_version(name: str) -> dict[str, Any]:
    executable = shutil.which(name)
    if not executable:
        return {"available": False, "version": None}
    try:
        completed = subprocess.run(
            [executable, "--version"],
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
        version = (completed.stdout or completed.stderr).strip().splitlines()[0]
    except (OSError, subprocess.SubprocessError, IndexError):
        version = None
    return {"available": True, "version": version}


def anki_process_running() -> bool | None:
    system = platform.system()
    try:
        if system == "Windows":
            completed = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq anki.exe", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                timeout=3,
                check=False,
            )
            return '"anki.exe"' in completed.stdout.lower()
        completed = subprocess.run(
            ["pgrep", "-f", "(^|/)anki($| )"],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        return completed.returncode == 0
    except (FileNotFoundError, OSError, subprocess.SubprocessError):
        return None


def port_open(port: int, timeout: float) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True
    except OSError:
        return False


def ankiconnect_version(timeout: float) -> dict[str, Any]:
    payload = json.dumps({"action": "version", "version": 6}).encode("utf-8")
    request = urllib.request.Request(
        "http://127.0.0.1:8765",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            parsed = json.loads(response.read().decode("utf-8"))
        if parsed.get("error") is None and isinstance(parsed.get("result"), int):
            return {"ok": True, "version": parsed["result"], "error": None}
        return {"ok": False, "version": None, "error": "unexpected response"}
    except (OSError, ValueError, urllib.error.URLError) as exc:
        return {"ok": False, "version": None, "error": type(exc).__name__}


def choose_recommendation(report: dict[str, Any]) -> str:
    if report["ports"]["3141"]:
        return "Native AnkiMCP appears reachable on 127.0.0.1:3141; verify deck listing through the MCP host."
    if report["ankiconnect"]["ok"]:
        if report["commands"]["npx"]["available"]:
            return "AnkiConnect is ready; use it directly or select one stdio MCP wrapper path."
        return "AnkiConnect is ready; install Node/npx only if your chosen MCP wrapper requires it."
    if report["ports"]["8765"]:
        return "Port 8765 is open but the AnkiConnect version check failed; verify the service and add-on configuration."
    if report["anki_process_running"]:
        return "Anki is running but no supported bridge was detected; choose one setup from docs/anki-mcp-setup.md."
    return "Open Anki Desktop first, then choose one bridge from docs/anki-mcp-setup.md."


def build_report(timeout: float) -> dict[str, Any]:
    commands = {name: command_version(name) for name in ("node", "npx")}
    report: dict[str, Any] = {
        "read_only": True,
        "platform": {"system": platform.system(), "release": platform.release()},
        "python": {
            "version": platform.python_version(),
            "supported": sys.version_info >= (3, 10),
        },
        "packages": package_status(),
        "commands": commands,
        "anki_process_running": anki_process_running(),
        "ports": {"3141": port_open(3141, timeout), "8765": port_open(8765, timeout)},
        "ankiconnect": ankiconnect_version(timeout),
    }
    report["recommendation"] = choose_recommendation(report)
    return report


def print_human(report: dict[str, Any]) -> None:
    print("READ_ONLY=yes")
    print(f"OS={report['platform']['system']} {report['platform']['release']}")
    print(
        "PYTHON={version} supported={supported}".format(**report["python"])
    )
    for package, available in report["packages"].items():
        print(f"PACKAGE {package}={'ok' if available else 'missing'}")
    for command, status in report["commands"].items():
        version = status["version"] or "unknown"
        print(f"COMMAND {command}={'ok' if status['available'] else 'missing'} version={version}")
    running = report["anki_process_running"]
    print(f"ANKI_PROCESS={running if running is not None else 'unknown'}")
    print(f"PORT 3141={'open' if report['ports']['3141'] else 'closed'}")
    print(f"PORT 8765={'open' if report['ports']['8765'] else 'closed'}")
    if report["ankiconnect"]["ok"]:
        print(f"ANKICONNECT=ok version={report['ankiconnect']['version']}")
    else:
        print(f"ANKICONNECT=unavailable reason={report['ankiconnect']['error']}")
    print(f"NEXT={report['recommendation']}")


def main() -> int:
    args = parse_args()
    if args.timeout <= 0:
        print("ERROR: --timeout must be greater than zero", file=sys.stderr)
        return 2
    report = build_report(args.timeout)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
