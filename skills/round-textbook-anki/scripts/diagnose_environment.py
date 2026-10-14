#!/usr/bin/env python3
"""Read-only environment diagnostics for the textbook-to-Anki workflow."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import re
import socket
import subprocess
import sys
from pathlib import Path
from typing import Any


REQUIRED_PACKAGES = {"pypdf": "pypdf", "PIL": "Pillow"}
ANKIWEB_ADDON_ID = "124672614"
ADDON_PACKAGE = "anki_mcp_server"
VERSION_PATTERN = re.compile(r"""^__version__\s*=\s*["']([^"']+)["']""", re.MULTILINE)


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


def default_addons_dir() -> Path | None:
    system = platform.system()
    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        base = Path(appdata) / "Anki2" if appdata else None
    elif system == "Darwin":
        base = Path.home() / "Library" / "Application Support" / "Anki2"
    else:
        base = Path.home() / ".local" / "share" / "Anki2"
    return base / "addons21" if base else None


def is_ankimcp_folder(folder: Path) -> bool:
    if folder.name in (ANKIWEB_ADDON_ID, ADDON_PACKAGE):
        return True
    try:
        manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return isinstance(manifest, dict) and manifest.get("package") == ADDON_PACKAGE


def addon_status(addons_dir: Path | None) -> dict[str, Any]:
    """Find the AnkiMCP add-on and report its version and install source.

    Only folder names are reported so private profile paths stay out of logs.
    """
    status: dict[str, Any] = {"found": False, "version": None, "install_source": None, "folder": None}
    if addons_dir is None or not addons_dir.is_dir():
        return status
    for folder in sorted(addons_dir.iterdir()):
        if not folder.is_dir() or not is_ankimcp_folder(folder):
            continue
        status["found"] = True
        status["folder"] = folder.name
        # AnkiWeb installs live in a folder named after the add-on ID. Any other
        # folder name means a manual .ankiaddon install that Anki will not update.
        status["install_source"] = "ankiweb" if folder.name == ANKIWEB_ADDON_ID else "manual"
        try:
            match = VERSION_PATTERN.search((folder / "__init__.py").read_text(encoding="utf-8"))
        except OSError:
            match = None
        status["version"] = match.group(1) if match else None
        break
    return status


def port_open(port: int, timeout: float) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True
    except OSError:
        return False


def update_note(report: dict[str, Any]) -> str:
    addon = report.get("ankimcp_addon") or {}
    if addon.get("install_source") != "manual":
        return ""
    return (
        " The add-on was installed from a file, so Anki's Check for Updates will not "
        "update it; compare its version with "
        "https://github.com/ankimcp/anki-mcp-server-addon/releases or reinstall from AnkiWeb."
    )


def choose_recommendation(report: dict[str, Any]) -> str:
    return _base_recommendation(report) + update_note(report)


def _base_recommendation(report: dict[str, Any]) -> str:
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
        "ankimcp_addon": addon_status(default_addons_dir()),
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
    addon = report["ankimcp_addon"]
    if addon["found"]:
        print(
            "ANKIMCP_ADDON=found version={version} source={source}".format(
                version=addon["version"] or "unknown",
                source=addon["install_source"],
            )
        )
    else:
        print("ANKIMCP_ADDON=not found")
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
