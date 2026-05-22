---
name: round-textbook-anki
description: Create, verify, and maintain Anki cards from round-based textbook, exam, workbook, or mock-test PDF sources where each round, test, chapter, or section has independent numbering. Use when converting a numbered problem batch into Anki notes with OCR cleanup, answer-key checks, MathJax, image crops, source-page verification, and Anki MCP readback without source-specific assumptions.
---

# Round Textbook Anki

## Scope

Use this skill for source-neutral Anki work where a textbook, workbook, PDF, exam set, mock test, or chapter has repeated numbered problem blocks.

- Do not infer the requested round from prior deck counts, previous work, or a neighboring round.
- Verify the target round, test, chapter, or problem range from the source page banner or surrounding page context before writing Anki notes.
- Treat each round/test/chapter as an independent scope unless the user or source proves otherwise.
- If a separate general Anki card-authoring skill is installed, use it for generic note mechanics; this skill owns round selection, source verification, and batch QA.

## Source Configuration

This public skill is path-neutral. Prefer local settings in `references/source-details.local.md` when present. That file must stay git-ignored.

If no local settings file exists, read `references/source-details-template.md` and ask only for the missing source details that cannot be discovered locally.

Common environment variables:

- `ROUND_TEXTBOOK_PROBLEM_PDF`
- `ROUND_TEXTBOOK_SOLUTION_PDF`
- `ROUND_TEXTBOOK_RENDERED_IMAGE_DIR`
- `ROUND_TEXTBOOK_PARENT_DECK`
- `ROUND_TEXTBOOK_ROUND_LABEL`
- `ROUND_TEXTBOOK_PROBLEM_COUNT`
- `ROUND_TEXTBOOK_MEDIA_DIR`

## Workflow

1. Identify the exact requested scope: source title, round/test/chapter label, problem range, parent deck, and note type.
2. Inspect the current Anki collection first. Check whether the target deck and notes already exist before adding or updating anything.
3. Verify the source pages. Confirm the banner/header, first and last problem numbers, and matching solution or answer-key section.
4. Build notes with stable numbering. Zero-pad one-digit problem numbers when the local deck convention uses `01`, `02`, etc.
5. For image-dependent problems, inspect the original page image before cropping. A good crop contains the needed figure, table, formula, or prompt box without neighboring problem text or answer choices.
6. Use the solution source only to confirm answers and reasoning. Write the back field in fresh teaching prose instead of copying long passages.
7. After creating or updating notes, re-read the saved notes from Anki and compare actual stored fields against the intended batch.

## Card Rules

- Keep front fields reviewable: problem statement, needed image, then choices or requested response format.
- Keep back fields useful: answer, direct reasoning, formula or definition, symbol meanings, and the common trap when it helps future review.
- For statement-evaluation questions, explain choices in printed order with a clear true/false or correct/incorrect judgment when that adds study value.
- For calculation questions, keep the main derivation in direct substitution form. Put mnemonics or alternate memory forms in a separate note/reference section.
- In Anki HTML, avoid raw `<` and `>` in text or math. Use MathJax commands such as `\lt`, `\gt`, `\le`, and `\ge`.
- For image HTML, prefer actual dimensions with `max-width:100%; height:auto;`. Avoid fixed CSS that can squash figures.
- If the user later asks what a symbol, term, unit, process, or formula origin means, update the relevant card so the clarification survives future review.

## Verification

Treat any answer mismatch, wrong deck, duplicate note, missing note, wrong round, broken image reference, or malformed MathJax as a blocker.

- Re-read saved notes through Anki MCP or AnkiConnect after creating the first few notes of a batch.
- For a full round or test, compare every saved answer against the matching answer key or solution section before reporting completion.
- For image cards, confirm the saved field references the actual media filename and preserves aspect ratio.
- Report the checked deck name, problem count, changed note IDs when available, and any corrected problem numbers.

## References

- Read `references/source-details-template.md` when local source paths, deck conventions, or answer-key mapping are missing.
- Read `references/card-patterns.md` when choosing front/back structure or MathJax/HTML patterns.
- Read `references/crop-workflow.md` when using `scripts/crop_problem_images.py` for figure crops or media insertion.

## Public Safety

- Never commit PDFs, rendered pages, cropped textbook images, Anki exports, local profile paths, answer-key dumps, or private deck data.
- Keep source-specific setup in `source-details.local.md` or environment variables.
- Do not publish copied problem or solution text unless the user provides proof that redistribution is allowed.
