---
name: round-textbook-anki
description: Create, verify, and maintain Anki cards from mixed textbook, workbook, exam, problem-bank, interview, and mock-test PDF source sets. Use when converting any numbered, chapter-based, round-based, past-exam, split problem/solution, or concept/interview study material into Anki notes with source classification, OCR cleanup, answer checks, MathJax, image crops, and Anki MCP readback without source-specific assumptions.
---

# Round Textbook Anki

## Scope

Use this skill for source-neutral Anki work across a folder or collection of study PDFs, not only one textbook.

Common source shapes include:

- subject-specific problem banks with continuous numbering
- chapter or topic problem banks
- mock rounds or practice tests where numbering restarts
- agency or company past-exam packets
- split problem/solution PDF pairs
- interview, concept, formula, or oral-exam preparation PDFs
- mixed source roots containing several of the above

Do not infer the source type, problem count, answer location, or deck structure from a previous project. Inspect the requested source set first.

## Source Configuration

This public skill is path-neutral. Prefer local settings in `references/source-details.local.md` or a local JSON manifest when present. These files must stay git-ignored.

Common environment variables:

- `TEXTBOOK_ANKI_SOURCE_ROOT`
- `TEXTBOOK_ANKI_SOURCE_MANIFEST`
- `TEXTBOOK_ANKI_PARENT_DECK`
- `TEXTBOOK_ANKI_MEDIA_DIR`
- `ROUND_TEXTBOOK_PROBLEM_PDF` for backward compatibility
- `ROUND_TEXTBOOK_SOLUTION_PDF` for backward compatibility
- `ROUND_TEXTBOOK_RENDERED_IMAGE_DIR` for backward compatibility

When a source root contains multiple PDFs, create or read a source manifest before building cards. Use `scripts/inventory_pdf_sources.py` for a first pass when page counts and filename-level classification are enough.

## Source Triage

Before writing cards, classify the source using `references/source-taxonomy.md`.

For each selected source, identify:

- source ID and title
- source type: `problem_bank`, `chapter_bank`, `mock_rounds`, `past_exam`, `split_problem_solution`, `interview_or_concept`, or `mixed`
- organization: continuous numbers, chapters, topics, rounds, years/agencies, or Q&A sections
- problem range and numbering convention
- answer source: same PDF, separate solution PDF, answer key pages, explanation pages, or user-provided answer
- deck path, tags, and source trace field convention

If the source type is unclear, inspect page images directly. Do not rely only on extracted PDF text when layout matters.

## Workflow

1. Inventory the source set. List candidate PDFs, page counts, and type hints without copying private paths into public files.
2. Pick the exact scope requested by the user: source, chapter/topic/round/year, problem range, and target deck.
3. Inspect the current Anki collection. Check whether matching decks or notes already exist before adding or updating anything.
4. Verify the source pages. Confirm the header/banner, problem numbering, first/last problem in scope, and matching answer or explanation section.
5. Choose the card pattern. Use multiple-choice, calculation, concept, image-first, cloze-like, or interview Q&A structure according to the source, not according to a fixed textbook template.
6. Build notes with stable source traceability. Preserve local numbering conventions such as `01`, `02`, or original exam numbers.
7. Use solution material only to confirm answers and reasoning. Write the back field in fresh teaching prose instead of copying long passages.
8. Re-read saved notes from Anki and compare actual stored fields against the intended batch.

## Card Rules

- Keep front fields reviewable: source marker, problem statement or question, needed image, then choices or response format.
- Keep back fields useful: answer, direct reasoning, formula or definition, symbol meanings, common trap, and source trace when available.
- For statement-evaluation questions, explain choices in printed order with a clear true/false or correct/incorrect judgment when that adds study value.
- For calculation questions, keep the main derivation in direct substitution form. Put mnemonics or alternate memory forms in a separate reference section.
- For interview or concept PDFs, convert into prompt-answer cards, comparison cards, or scenario follow-up cards instead of forcing multiple-choice structure.
- In Anki HTML, avoid raw `<` and `>` in text or math. Use MathJax commands such as `\lt`, `\gt`, `\le`, and `\ge`.
- For image HTML, prefer actual dimensions with `max-width:100%; height:auto;`. Avoid fixed CSS that can squash figures.
- If the user later asks what a symbol, term, unit, process, or formula origin means, update the relevant card so the clarification survives future review.

## Image and OCR Rules

- Read the problem from page images first when the PDF layout contains figures, tables, columns, answer choices, or page banners.
- Mark OCR-derived fronts with `[OCR]` when the text may need later cleanup.
- Crop only the figure, formula box, table, graph, or prompt area needed for review.
- Re-render at higher DPI before cropping if the crop is too small, blurry, or cut off.
- Do not generate or redraw technical diagrams from memory when the source figure is accuracy-sensitive. Use the source image or ask the user for the figure.

## Verification

Treat any answer mismatch, wrong deck, duplicate note, missing note, wrong source scope, broken image reference, or malformed MathJax as a blocker.

- Re-read saved notes through Anki MCP or AnkiConnect after creating the first few notes of a new source or scope.
- For a complete batch, compare every saved answer against the matching answer key or solution section before reporting completion.
- For image cards, confirm the saved field references the actual media filename and preserves aspect ratio.
- For mixed source roots, report which source IDs were touched and which were only inspected.
- Report the checked deck name, problem count, changed note IDs when available, and any corrected problem numbers.

## References

- Read `references/source-taxonomy.md` when classifying a source set or deciding deck structure.
- Read `references/source-details-template.md` when local source paths, manifests, deck conventions, or answer-key mapping are missing.
- Read `references/card-patterns.md` when choosing front/back structure or MathJax/HTML patterns.
- Read `references/crop-workflow.md` when using `scripts/crop_problem_images.py` for figure crops or media insertion.

## Public Safety

- Never commit PDFs, rendered pages, cropped textbook images, Anki exports, local profile paths, answer-key dumps, or private deck data.
- Keep source-specific setup in `source-details.local.md`, a local manifest, or environment variables.
- Do not publish copied problem or solution text unless the user provides proof that redistribution is allowed.
