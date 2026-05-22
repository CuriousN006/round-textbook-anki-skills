# Crop Workflow

Use `scripts/crop_problem_images.py` after visually deciding the crop box from a rendered page image.

The script can:

- crop the relevant figure from a page image
- save it with a stable filename
- optionally copy it into Anki `collection.media`
- generate an aspect-ratio-safe HTML snippet
- optionally insert that snippet into an existing front field before or after a marker

## JSON Spec

The spec file is a JSON array:

```json
[
  {
    "note_id": 1776690818094,
    "source_image": "C:/path/to/page-007.png",
    "crop": [790, 365, 1425, 1045],
    "filename": "source_round03_q07.png",
    "front_html": "[OCR] 07. Problem prompt<br><br>1. option A<br>2. option B",
    "insert_before": "1."
  }
]
```

Required fields:

- `source_image`: absolute or relative path to the rendered page image
- `crop`: `[left, upper, right, lower]`
- `filename`: final cropped filename

Optional fields:

- `note_id`: traceability value copied into the result
- `front_html`: current front HTML
- `insert_before`: marker to insert before; when omitted, the script tries common choice markers such as `①`, `1.`, `1)`, and `(1)`
- `insert_after`: marker to insert after
- `style`: custom inline CSS for the `<img>` tag

Do not set both `insert_before` and `insert_after` in the same item.

## Usage

```powershell
python .\skills\round-textbook-anki\scripts\crop_problem_images.py `
  --spec .\work\crops.json `
  --output-dir .\work\crops `
  --media-dir "$env:ROUND_TEXTBOOK_MEDIA_DIR" `
  --results .\work\crop-results.json
```

Use `updated_front_html` from the result with Anki MCP or AnkiConnect update calls.
