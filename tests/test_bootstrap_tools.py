from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "round-textbook-anki" / "scripts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


diagnose = load_module("diagnose_environment", SCRIPTS / "diagnose_environment.py")
configure = load_module("configure_local_source", SCRIPTS / "configure_local_source.py")


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.payload


class DiagnoseTests(unittest.TestCase):
    def test_ankiconnect_version_uses_read_only_action(self):
        with mock.patch.object(
            diagnose.urllib.request,
            "urlopen",
            return_value=FakeResponse({"result": 6, "error": None}),
        ) as urlopen:
            result = diagnose.ankiconnect_version(0.1)

        self.assertEqual(result, {"ok": True, "version": 6, "error": None})
        request = urlopen.call_args.args[0]
        self.assertEqual(json.loads(request.data), {"action": "version", "version": 6})

    def test_recommendation_prefers_native_mcp_when_3141_is_open(self):
        report = {
            "ports": {"3141": True, "8765": False},
            "ankiconnect": {"ok": False},
            "commands": {"npx": {"available": False}},
            "anki_process_running": True,
        }
        self.assertIn("3141", diagnose.choose_recommendation(report))


class ConfigureTests(unittest.TestCase):
    def test_writes_git_ignored_local_draft_without_pdf_contents(self):
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            source_root = temp_path / "private-pdfs"
            source_root.mkdir()
            (source_root / "sample.pdf").write_bytes(b"not a real pdf")
            details = temp_path / "source-details.local.md"
            manifest = temp_path / "source-manifest.local.json"

            configure.write_files(
                source_root,
                "Study Deck",
                "round 1",
                details,
                manifest,
                force=False,
            )

            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertTrue(payload["local_only"])
            self.assertEqual(payload["sources"][0]["relative_path"], "sample.pdf")
            self.assertNotIn("not a real pdf", manifest.read_text(encoding="utf-8"))
            self.assertIn("Study Deck", details.read_text(encoding="utf-8"))

    def test_refuses_to_replace_local_files_without_force(self):
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            details = temp_path / "source-details.local.md"
            details.write_text("existing", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                configure.write_files(
                    temp_path,
                    "Deck",
                    "all",
                    details,
                    temp_path / "source-manifest.local.json",
                    force=False,
                )


if __name__ == "__main__":
    unittest.main()
