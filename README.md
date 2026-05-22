# Textbook Problem Bank Anki Skills

Public, source-neutral Codex skill for turning mixed textbook, workbook, problem-bank, mock-test, past-exam, interview, or concept PDF material into verified Anki notes.

This repository intentionally does not contain PDFs, rendered pages, Anki exports, collection media, answer keys, or local machine paths. Keep real source details in `source-details.local.md`, which is ignored by Git.

## What This Skill Covers

- Inventory a source folder and classify PDFs before deciding deck shape.
- Verify the requested source, round, test, chapter, topic, agency exam, or problem batch from the source pages before writing cards.
- Keep independent numbering straight when rounds, chapters, or exam sessions restart at problem `01`.
- Build study-friendly Anki fronts and backs with OCR cleanup, MathJax, image crops, answer checks, and fresh explanations.
- Re-read saved Anki notes through MCP or AnkiConnect after creation so the final report reflects the actual collection state.
- Compare saved answers against the matching answer key or solution section before declaring a batch complete.

## Layout

```text
skills/
  round-textbook-anki/
    SKILL.md
    agents/openai.yaml
    references/
      card-patterns.md
      crop-workflow.md
      source-taxonomy.md
      source-details-template.md
    scripts/
      crop_problem_images.py
      inventory_pdf_sources.py
```

## Local Install

From this repository root:

```powershell
Copy-Item -Recurse -Force .\skills\round-textbook-anki "$env:USERPROFILE\.codex\skills\round-textbook-anki"
```

Then start a new Codex session so the skill list can refresh. In prompts, ask for `$round-textbook-anki` when working on a source folder, textbook, chapter, round, exam packet, or numbered problem batch.

## Private Source Configuration

Copy `skills/round-textbook-anki/references/source-details-template.md` to:

```text
skills/round-textbook-anki/references/source-details.local.md
```

Fill it with local file paths, deck names, media directories, and source-specific notes. Do not commit that file.

For a first-pass local manifest:

```powershell
python .\skills\round-textbook-anki\scripts\inventory_pdf_sources.py `
  --root "C:\path\to\study-pdfs" `
  --output ".\source-manifest.local.json"
```

Review and edit the generated manifest before creating Anki notes.

## Public Safety Rules

- Do not commit copyrighted PDFs, rendered pages, crops, answer lists, or copied textbook passages.
- Do not commit absolute local paths, Anki profile paths, API tokens, or private deck exports.
- Treat solution manuals as references for checking answers and reasoning, then write explanations in fresh teaching prose.
