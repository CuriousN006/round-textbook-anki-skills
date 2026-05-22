#!/usr/bin/env python3
"""Crop problem images and prepare HTML for Anki cards."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "Pillow is required. Install it in the runtime used for this script."
    ) from exc


DEFAULT_STYLE = "max-width:100%; height:auto;"
DEFAULT_INSERT_BEFORE = "1."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Crop problem figures from page images and optionally prepare updated "
            "Anki front HTML."
        )
    )
    parser.add_argument("--spec", required=True, help="Path to the crop spec JSON file")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where cropped images should be written",
    )
    parser.add_argument(
        "--media-dir",
        help="Optional Anki collection.media directory to copy the cropped files into",
    )
    parser.add_argument(
        "--results",
        help="Optional path for the output JSON results file",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing cropped files",
    )
    return parser.parse_args()


def load_spec(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Spec root must be a JSON array.")
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Spec item {index} must be an object.")
    return data


def ensure_crop_box(raw_box: Any) -> tuple[int, int, int, int]:
    if not isinstance(raw_box, list) or len(raw_box) != 4:
        raise ValueError("crop must be a list of four integers: [left, upper, right, lower].")
    try:
        left, upper, right, lower = [int(value) for value in raw_box]
    except (TypeError, ValueError) as exc:
        raise ValueError("crop values must be integers.") from exc
    if left >= right or upper >= lower:
        raise ValueError("crop coordinates must satisfy left < right and upper < lower.")
    return left, upper, right, lower


def image_html(filename: str, style: str) -> str:
    return f'<div><img src="{filename}" style="{style}"></div><br>'


def insert_snippet(front_html: str, snippet: str, item: dict[str, Any]) -> str:
    insert_before = item.get("insert_before")
    insert_after = item.get("insert_after")
    if insert_before and insert_after:
        raise ValueError("Specify only one of insert_before or insert_after.")

    if not insert_before and not insert_after:
        insert_before = DEFAULT_INSERT_BEFORE

    if insert_before:
        marker = str(insert_before)
        idx = front_html.find(marker)
        if idx == -1:
            raise ValueError(f"insert_before marker not found: {marker!r}")
        return front_html[:idx] + snippet + front_html[idx:]

    marker = str(insert_after)
    idx = front_html.find(marker)
    if idx == -1:
        raise ValueError(f"insert_after marker not found: {marker!r}")
    idx += len(marker)
    return front_html[:idx] + snippet + front_html[idx:]


def process_item(
    item: dict[str, Any],
    output_dir: Path,
    media_dir: Path | None,
    overwrite: bool,
) -> dict[str, Any]:
    source_image = Path(str(item["source_image"]))
    filename = str(item["filename"])
    crop_box = ensure_crop_box(item["crop"])
    style = str(item.get("style", DEFAULT_STYLE))

    if not source_image.exists():
        raise FileNotFoundError(f"source_image not found: {source_image}")

    output_dir.mkdir(parents=True, exist_ok=True)
    crop_path = output_dir / filename
    if crop_path.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing crop: {crop_path}")

    with Image.open(source_image) as image:
        crop = image.crop(crop_box)
        crop.save(crop_path)

    media_path = None
    if media_dir is not None:
        media_dir.mkdir(parents=True, exist_ok=True)
        media_path = media_dir / filename
        if media_path.exists() and not overwrite:
            raise FileExistsError(f"Refusing to overwrite existing media file: {media_path}")
        shutil.copy2(crop_path, media_path)

    snippet = image_html(filename, style)
    result: dict[str, Any] = {
        "note_id": item.get("note_id"),
        "filename": filename,
        "crop_path": str(crop_path),
        "media_path": str(media_path) if media_path else None,
        "html_snippet": snippet,
    }

    front_html = item.get("front_html")
    if front_html is not None:
        result["updated_front_html"] = insert_snippet(str(front_html), snippet, item)

    return result


def main() -> int:
    args = parse_args()
    spec_path = Path(args.spec)
    output_dir = Path(args.output_dir)
    media_dir = Path(args.media_dir) if args.media_dir else None
    results_path = Path(args.results) if args.results else spec_path.with_suffix(".results.json")

    try:
        spec = load_spec(spec_path)
        results = [
            process_item(item, output_dir=output_dir, media_dir=media_dir, overwrite=args.overwrite)
            for item in spec
        ]
    except Exception as exc:  # pragma: no cover - CLI surface
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    results_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    for result in results:
        print(
            "OK|{note}|{filename}|{crop_path}".format(
                note=result.get("note_id"),
                filename=result["filename"],
                crop_path=result["crop_path"],
            )
        )
    print(f"RESULTS={results_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
