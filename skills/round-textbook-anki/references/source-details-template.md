# Source Details Local Template

Copy this file to `source-details.local.md` and fill it with private local details. Do not commit the local copy.

## Source Set

- Source set nickname:
- Local source root:
- Parent deck:
- Default note type:
- Default tags:
- Media directory:
- Rendered page directory:
- Local manifest path:

Environment variable options:

```powershell
$env:TEXTBOOK_ANKI_SOURCE_ROOT = "C:\path\to\source-root"
$env:TEXTBOOK_ANKI_SOURCE_MANIFEST = "C:\path\to\source-manifest.local.json"
$env:TEXTBOOK_ANKI_PARENT_DECK = "Mechanical Exam Prep"
$env:TEXTBOOK_ANKI_MEDIA_DIR = "C:\path\to\Anki2\Profile\collection.media"
```

Backward-compatible single-source options:

```powershell
$env:ROUND_TEXTBOOK_PROBLEM_PDF = "C:\path\to\problem.pdf"
$env:ROUND_TEXTBOOK_SOLUTION_PDF = "C:\path\to\solution.pdf"
$env:ROUND_TEXTBOOK_RENDERED_IMAGE_DIR = "C:\path\to\rendered-pages"
```

## Source Manifest Skeleton

Keep the real manifest local. A source entry can use this shape:

```json
{
  "source_id": "machine-design-bank",
  "title": "Private local title",
  "type": "problem_bank",
  "organization": "chapter",
  "files": {
    "problem_pdf": "C:/private/path/problem.pdf",
    "solution_pdf": null
  },
  "deck": "Parent::Source Name",
  "numbering": {
    "style": "zero_padded",
    "problem_count": null,
    "restarts_by_scope": false
  },
  "answer_source": {
    "kind": "same_pdf",
    "pages": "local-only note"
  },
  "tags": ["source:machine-design-bank"],
  "notes": "Local-only setup hints"
}
```

## Source Mapping

For each source, record:

- Problem pages:
- Solution or answer pages:
- Page banner/header pattern:
- Scope labels: chapter, topic, round, year, agency, or continuous range:
- How to distinguish problem pages from explanation pages:
- Whether problem numbers restart within each scope:

## Deck Mapping

- Parent deck:
- Per-source deck shape:
- Per-scope subdeck shape:
- Example local deck:
- Tags to apply:
- Source trace field convention:

## Verification Checklist

- Source type classified:
- Target scope verified from source page:
- Matching answer or solution section verified:
- Existing Anki notes checked:
- Saved note fields re-read after creation:
- Saved answers compared against answer source:

## Notes

Keep only local setup hints here. Do not paste copyrighted problem text, full answer lists, or large solution excerpts.
