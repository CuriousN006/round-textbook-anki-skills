#!/usr/bin/env python3
"""Inventory PDF source sets for textbook-to-Anki workflows."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from pypdf import PdfReader
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "pypdf is required. Install it in the runtime used for this script."
    ) from exc


KEYWORD_SETS = {
    "round": ["round", "mock", "test", "회차", "모의"],
    "chapter": ["chapter", "section", "part", "단원", "챕터"],
    "answer": ["answer", "solution", "정답", "답안", "해설", "풀이"],
    "past_exam": ["exam", "past", "agency", "기출", "공사", "공단", "상반기", "하반기"],
    "interview": ["interview", "oral", "면접", "질문", "답변", "직무"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a source inventory skeleton for a folder of PDF study materials."
    )
    parser.add_argument("--root", required=True, help="Source root containing PDF files")
    parser.add_argument("--output", help="Optional JSON output path")
    parser.add_argument(
        "--sample-text",
        action="store_true",
        help="Inspect first/middle/last pages for type hints. Does not store extracted text.",
    )
    return parser.parse_args()


def source_id(path: Path) -> str:
    stem = path.stem.lower()
    cleaned = []
    for char in stem:
        if char.isalnum():
            cleaned.append(char)
        elif cleaned and cleaned[-1] != "-":
            cleaned.append("-")
    return "".join(cleaned).strip("-") or "source"


def text_sample(reader: PdfReader) -> str:
    page_count = len(reader.pages)
    indexes = sorted(
        {
            0,
            1,
            2,
            max(0, page_count // 2),
            max(0, page_count - 3),
            max(0, page_count - 2),
            max(0, page_count - 1),
        }
    )
    chunks = []
    for index in indexes:
        if 0 <= index < page_count:
            try:
                chunks.append(reader.pages[index].extract_text() or "")
            except Exception:
                pass
    return "\n".join(chunks)


def classify(path: Path, sample: str) -> tuple[list[str], str, str]:
    haystack = f"{path.name}\n{path.parent.name}\n{sample}".lower()
    signals = [
        name
        for name, words in KEYWORD_SETS.items()
        if any(word.lower() in haystack for word in words)
    ]

    if "interview" in signals:
        source_type = "interview_or_concept"
        organization = "qa_sections"
    elif "answer" in signals and ("solution" in haystack or "해설" in haystack):
        source_type = "split_problem_solution"
        organization = "unknown"
    elif "past_exam" in signals:
        source_type = "past_exam"
        organization = "exam_session"
    elif "round" in signals:
        source_type = "mock_rounds"
        organization = "round"
    elif "chapter" in signals:
        source_type = "chapter_bank"
        organization = "chapter"
    else:
        source_type = "problem_bank"
        organization = "continuous"

    return signals, source_type, organization


def inventory_pdf(path: Path, root: Path, sample_text: bool) -> dict[str, Any]:
    reader = PdfReader(str(path))
    sample = text_sample(reader) if sample_text else ""
    signals, source_type, organization = classify(path, sample)
    return {
        "source_id": source_id(path),
        "title": path.stem,
        "relative_path": path.relative_to(root).as_posix(),
        "page_count": len(reader.pages),
        "type_hint": source_type,
        "organization_hint": organization,
        "signals": signals,
        "deck": None,
        "answer_source": None,
        "notes": "Review and edit this local manifest before creating Anki notes.",
    }


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(f"ERROR: root not found: {root}", file=sys.stderr)
        return 1

    entries = []
    for path in sorted(root.rglob("*.pdf")):
        try:
            entries.append(inventory_pdf(path, root=root, sample_text=args.sample_text))
        except Exception as exc:
            entries.append(
                {
                    "source_id": source_id(path),
                    "title": path.stem,
                    "relative_path": path.relative_to(root).as_posix(),
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    payload = {"root": str(root), "sources": entries}
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
