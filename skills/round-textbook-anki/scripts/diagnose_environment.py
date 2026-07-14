#!/usr/bin/env python3
"""Read-only environment diagnostics for the textbook-to-Anki workflow."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import socket
import subprocess
import sys
from typing import Any


REQUIRED_PACKAGES = {"pypdf": "pypdf", "PIL": "Pillow"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only check of Python packages, Anki, and the native AnkiMCP "
            "endpoint at 127.0.0.1:3141."
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


def choose_recommendation(report: dict[str, Any]) -> str:
    if report["ports"]["3141"]:
        return "Native AnkiMCP appears reachable on 127.0.0.1:3141; verify deck listing through the MCP host."
    if report["anki_process_running"]:
        return "Anki is running but native AnkiMCP is not reachable on 127.0.0.1:3141; verify the add-on and restart Anki."
    return "Open Anki Desktop, then verify the native AnkiMCP add-on described in docs/anki-mcp-setup.md."


def build_report(timeout: float) -> dict[str, Any]:
    report: dict[str, Any] = {
        "read_only": True,
        "platform": {"system": platform.system(), "release": platform.release()},
        "python": {
            "version": platform.python_version(),
            "supported": sys.version_info >= (3, 10),
        },
        "packages": package_status(),
        "anki_process_running": anki_process_running(),
        "ports": {"3141": port_open(3141, timeout)},
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
    running = report["anki_process_running"]
    print(f"ANKI_PROCESS={running if running is not None else 'unknown'}")
    print(f"PORT 3141={'open' if report['ports']['3141'] else 'closed'}")
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
