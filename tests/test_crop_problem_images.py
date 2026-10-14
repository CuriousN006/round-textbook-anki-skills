from __future__ import annotations

import importlib.util
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


crop = load_module("crop_problem_images", SCRIPTS / "crop_problem_images.py")

SNIPPET = "<IMG>"


class InsertSnippetTests(unittest.TestCase):
    def test_source_number_prefix_is_not_a_choice_marker(self):
        front = "[OCR] 01. 다음 중 옳은 것은?<br>1) A<br>2) B"
        self.assertEqual(
            crop.insert_snippet(front, SNIPPET, {}),
            "[OCR] 01. 다음 중 옳은 것은?<br><IMG>1) A<br>2) B",
        )

    def test_decimal_in_prompt_is_not_a_choice_marker(self):
        front = "[OCR] 07. 질량 1.5 kg 물체<br>1. 10 N<br>2. 20 N"
        self.assertEqual(
            crop.insert_snippet(front, SNIPPET, {}),
            "[OCR] 07. 질량 1.5 kg 물체<br><IMG>1. 10 N<br>2. 20 N",
        )

    def test_circled_marker_after_line_break(self):
        front = "[OCR] 03. 그림과 같은 보에서<br><br>① 10<br>② 20"
        self.assertEqual(
            crop.insert_snippet(front, SNIPPET, {}),
            "[OCR] 03. 그림과 같은 보에서<br><br><IMG>① 10<br>② 20",
        )

    def test_explicit_insert_before_also_requires_line_start(self):
        front = "[OCR] 01. prompt<br>1. A"
        self.assertEqual(
            crop.insert_snippet(front, SNIPPET, {"insert_before": "1."}),
            "[OCR] 01. prompt<br><IMG>1. A",
        )

    def test_missing_line_start_marker_raises(self):
        with self.assertRaises(ValueError):
            crop.insert_snippet("[OCR] 01. prompt with no choices", SNIPPET, {})

    def test_insert_after_uses_plain_match(self):
        self.assertEqual(
            crop.insert_snippet("prompt END choices", SNIPPET, {"insert_after": "END"}),
            "prompt END<IMG> choices",
        )


if __name__ == "__main__":
    unittest.main()
