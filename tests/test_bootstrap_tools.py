from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


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


class DiagnoseTests(unittest.TestCase):
    def test_recommendation_prefers_native_mcp_when_3141_is_open(self):
        report = {
            "ports": {"3141": True},
            "anki_process_running": True,
        }
        self.assertIn("3141", diagnose.choose_recommendation(report))

    def test_recommendation_points_to_native_addon_when_port_is_closed(self):
        report = {
            "ports": {"3141": False},
            "anki_process_running": True,
        }
        self.assertIn("add-on", diagnose.choose_recommendation(report))

    def test_addon_status_reports_manual_install_version(self):
        with tempfile.TemporaryDirectory() as temp:
            addon = Path(temp) / "anki_mcp_server"
            addon.mkdir()
            (addon / "__init__.py").write_text('__version__ = "0.26.0"\n', encoding="utf-8")
            status = diagnose.addon_status(Path(temp))
        self.assertEqual(
            status,
            {"found": True, "version": "0.26.0", "install_source": "manual", "folder": "anki_mcp_server"},
        )

    def test_addon_status_detects_ankiweb_install_by_folder_id(self):
        with tempfile.TemporaryDirectory() as temp:
            addon = Path(temp) / "124672614"
            addon.mkdir()
            (addon / "__init__.py").write_text("__version__ = '0.40.0'\n", encoding="utf-8")
            status = diagnose.addon_status(Path(temp))
        self.assertEqual((status["install_source"], status["version"]), ("ankiweb", "0.40.0"))

    def test_addon_status_detects_renamed_folder_by_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            addon = Path(temp) / "renamed"
            addon.mkdir()
            (addon / "manifest.json").write_text('{"package": "anki_mcp_server"}', encoding="utf-8")
            status = diagnose.addon_status(Path(temp))
        self.assertTrue(status["found"])
        self.assertIsNone(status["version"])

    def test_addon_status_handles_missing_addons_dir(self):
        self.assertFalse(diagnose.addon_status(None)["found"])
        self.assertFalse(diagnose.addon_status(Path("does-not-exist"))["found"])

    def test_recommendation_warns_that_manual_install_does_not_auto_update(self):
        report = {
            "ports": {"3141": True},
            "anki_process_running": True,
            "ankimcp_addon": {"found": True, "install_source": "manual"},
        }
        self.assertIn("Check for Updates", diagnose.choose_recommendation(report))
        report["ankimcp_addon"]["install_source"] = "ankiweb"
        self.assertNotIn("Check for Updates", diagnose.choose_recommendation(report))

    def test_recommendation_flags_missing_pdf_renderer(self):
        report = {"ports": {"3141": True}, "anki_process_running": True, "pdf_renderer": None}
        self.assertIn("renderer", diagnose.choose_recommendation(report))
        report["pdf_renderer"] = "pdftoppm"
        self.assertNotIn("renderer", diagnose.choose_recommendation(report))

    def test_pdf_renderer_prefers_command_line_tools(self):
        original_which = diagnose.shutil.which
        try:
            diagnose.shutil.which = lambda name: "/usr/bin/mutool" if name == "mutool" else None
            self.assertEqual(diagnose.pdf_renderer(), "mutool")
        finally:
            diagnose.shutil.which = original_which


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
