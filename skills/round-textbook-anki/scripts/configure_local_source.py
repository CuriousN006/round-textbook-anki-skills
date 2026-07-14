#!/usr/bin/env python3
"""Create git-ignored local source details and a manifest draft."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DETAILS = SKILL_ROOT / "references" / "source-details.local.md"
DEFAULT_MANIFEST = Path.cwd() / "source-manifest.local.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Interactively create local-only source settings and a manifest draft."
    )
    parser.add_argument("--source-root", help="Folder containing the study PDFs")
    parser.add_argument("--parent-deck", help="Desired parent Anki deck")
    parser.add_argument(
        "--scope",
        help="Target scope, such as all, chapter 3, round 2, or problems 01-20",
    )
    parser.add_argument("--details", type=Path, default=DEFAULT_DETAILS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--yes", action="store_true", help="Write without final confirmation")
    parser.add_argument("--force", action="store_true", help="Replace existing local files")
    return parser.parse_args()


def ask(value: str | None, prompt: str) -> str:
    if value and value.strip():
        return value.strip()
    if not sys.stdin.isatty():
        raise ValueError(f"missing required value: {prompt}")
    answer = input(f"{prompt}: ").strip()
    if not answer:
        raise ValueError(f"missing required value: {prompt}")
    return answer


def source_id(path: Path) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
    return slug or "source"


def find_pdfs(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() == ".pdf")


def build_manifest(root: Path, parent_deck: str, scope: str) -> dict[str, Any]:
    sources = []
    for path in find_pdfs(root):
        sources.append(
            {
                "source_id": source_id(path),
                "title": path.stem,
                "relative_path": path.relative_to(root).as_posix(),
                "type_hint": "unknown",
                "organization_hint": "unknown",
                "deck": parent_deck,
                "target_scope": scope,
                "answer_source": None,
                "notes": "Review this local draft before creating Anki notes.",
            }
        )
    return {
        "local_only": True,
        "root": str(root),
        "parent_deck": parent_deck,
        "target_scope": scope,
        "sources": sources,
    }


def render_details(root: Path, parent_deck: str, scope: str, manifest: Path) -> str:
    return f"""# Source Details Local

This file contains private machine-specific settings. Do not commit it.

## Source Set

- Local source root: {root}
- Parent deck: {parent_deck}
- Target scope: {scope}
- Local manifest path: {manifest.resolve()}
- Default note type: Basic
- Media directory: ask only when image copying is required

## Next Checks

- Review the generated manifest and classify each source.
- Confirm problem and answer page ranges from the actual PDF pages.
- Verify the Anki deck with a read-only action before writing notes.
- Create only 2-3 trial notes, then re-read their stored fields.
"""


def write_files(
    root: Path,
    parent_deck: str,
    scope: str,
    details_path: Path,
    manifest_path: Path,
    force: bool,
) -> None:
    for path in (details_path, manifest_path):
        if path.exists() and not force:
            raise FileExistsError(f"refusing to replace existing local file: {path}")
    details_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    details_path.write_text(
        render_details(root, parent_deck, scope, manifest_path), encoding="utf-8"
    )
    manifest_path.write_text(
        json.dumps(build_manifest(root, parent_deck, scope), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    try:
        root = Path(ask(args.source_root, "PDF가 들어 있는 폴더")).expanduser().resolve()
        if not root.is_dir():
            raise ValueError(f"source folder not found: {root}")
        parent_deck = ask(args.parent_deck, "만들고 싶은 상위 덱 이름")
        scope = ask(args.scope, "대상 범위(전체/교재/장/회차/문제 번호)")
        if not args.yes:
            print(f"DETAILS={args.details}")
            print(f"MANIFEST={args.manifest}")
            if input("이 로컬 전용 파일을 저장할까요? [y/N]: ").strip().lower() not in {"y", "yes"}:
                print("CANCELLED")
                return 0
        write_files(root, parent_deck, scope, args.details, args.manifest, args.force)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"DETAILS_WRITTEN={args.details}")
    print(f"MANIFEST_WRITTEN={args.manifest}")
    print("NEXT=Review the manifest, then run the read-only environment diagnosis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
