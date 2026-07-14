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

## Bootstrap From a Repository Link

When the user gives only this repository URL or an unfamiliar environment:

1. Read the repository-root `START_HERE.md`, this `SKILL.md`, and `docs/anki-mcp-setup.md`.
2. Determine whether the current session can actually read files, run commands, and use local MCP tools. Do not claim local access from a chat-only environment.
3. If the current session is chat-only, explain the limitation and guide the user to a tool-capable agent using current official product documentation. Ask only for operating system and GUI/terminal preference.
4. If tool access exists, run `scripts/diagnose_environment.py` before proposing installations or configuration changes. This diagnosis is read-only.
5. Do not clone the repository merely to read documentation when remote access is enough. Use a local checkout only when local scripts, source files, or Git changes require it.

`agents/openai.yaml` is Codex/ChatGPT metadata. Other agents may ignore it. The portable core is `SKILL.md`, `references/`, and `scripts/`.

## Approval Boundary

Proceed without extra approval only for read-only inspection and actions already allowed inside the active workspace. Before installing programs or packages, downloading files, changing MCP or agent settings, writing outside the workspace, or creating/updating/deleting Anki notes, explain the exact action and request approval according to the host product's policy.

Prefer scoped automatic approval or automatic risk review over disabling sandbox and approval protections. Never ask the user to paste passwords, API keys, or access tokens into chat. Never expose local Anki write access to the public internet.

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

If local source settings are missing, ask only for the PDF folder, desired parent deck, and target scope. After approval, `scripts/configure_local_source.py` can create git-ignored `source-details.local.md` and `source-manifest.local.json` drafts. Ask for an Anki profile or media directory only when the selected workflow actually needs it.

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

1. Run the read-only environment diagnosis and choose exactly one Anki bridge path. If packages or settings are missing, request approval before changing them.
2. Inventory the source set. List candidate PDFs, page counts, and type hints without copying private paths into public files.
3. Pick the exact scope requested by the user: source, chapter/topic/round/year, problem range, and target deck.
4. Inspect the current Anki collection with a harmless read action. Check whether matching decks or notes already exist before adding or updating anything.
5. Verify the source pages. Confirm the header/banner, problem numbering, first/last problem in scope, and matching answer or explanation section.
6. Choose the card pattern. Use multiple-choice, calculation, concept, image-first, cloze-like, or interview Q&A structure according to the source, not according to a fixed textbook template.
7. Build 2-3 trial notes with stable source traceability. Preserve local numbering conventions such as `01`, `02`, or original exam numbers.
8. Use solution material only to confirm answers and reasoning. Write the back field in fresh teaching prose instead of copying long passages.
9. Re-read the trial notes from Anki and compare the actual stored Front, Back, deck, tags, image names, and answers against the intended batch. Continue to the full batch only when the trial passes.
10. Re-read every saved note in the completed batch and compare actual stored fields against the intended batch.
11. If a user points out a card-quality failure, fix that card and then audit all cards with the same pattern, not only the one example.
12. For correction passes, read the actual saved note text in Anki in order, in small batches, and judge the Front and Back semantically. Do not claim a quality pass from generated payloads, search results, or mechanical audits.

## Card Rules

- Keep front fields reviewable: source marker, problem statement or question, needed image, then choices or response format.
- Keep front fields searchable: OCR or transcribe problem statements and choices into text. Do not embed the whole problem or page image as the review surface.
- Keep back fields useful: answer, direct reasoning, formula or definition, symbol meanings, common trap, and a human-readable source line when available.
- Strip visible source/debug artifacts such as `source_id=...`, `type=...`, `scope=...`, `problem=...`, `page=...`, and `answer_checked=...` from the card fields.
- Put formulas, substitutions, and necessary definitions in the main `풀이`. The `참고` section is only for supplementary traps, comparisons, unit checks, and memory aids.
- Do not leave renderer placeholders such as `Mathjax`/`MathJax` or broken escape/control characters in saved cards.
- For statement-evaluation and "correct/incorrect choice" questions, explain choices in printed order with a clear true/false or correct/incorrect judgment and the reason for each choice.
- Choice explanations must not parrot the printed choice. Explain the principle, formula, unit conversion, classification boundary, or counterexample that makes the choice right or wrong.
- For calculation questions, keep the main derivation in direct substitution form and split dense formulas into readable steps. Put mnemonics or alternate memory forms in a separate reference section.
- Do not use generic filler such as "this choice fits the category" when the learner needs a reason. State the classification boundary, process mechanism, formula, exception, or counterexample.
- If source wording or answer keys are questionable, mark the source-standard answer clearly and add a compact caveat instead of silently inventing a cleaner rule.
- For interview or concept PDFs, convert into prompt-answer cards, comparison cards, or scenario follow-up cards instead of forcing multiple-choice structure.
- In Anki HTML, avoid raw `<` and `>` in text or math. Use MathJax commands such as `\lt`, `\gt`, `\le`, and `\ge`.
- For image HTML, prefer actual dimensions with `max-width:100%; height:auto;`. Avoid fixed CSS that can squash figures.
- If the user later asks what a symbol, term, unit, process, or formula origin means, update the relevant card so the clarification survives future review.

## Image and OCR Rules

- Read the problem from page images first when the PDF layout contains figures, tables, columns, answer choices, or page banners.
- Mark OCR-derived fronts with `[OCR]` when the text may need later cleanup.
- Crop only the figure, formula box, table, graph, or prompt area needed for review. Do not crop the entire problem/page just to avoid OCR.
- When converting an image-only card to OCR text, remove old whole-problem image references and keep only focused visual crops that the learner actually needs.
- For figure-dependent questions, do not replace the source figure with a text summary when the geometry, graph, table layout, or symbol placement affects the answer. Crop the focused figure and keep OCR text searchable around it.
- Re-render at higher DPI before cropping if the crop is too small, blurry, or cut off.
- Do not generate or redraw technical diagrams from memory when the source figure is accuracy-sensitive. Use the source image or ask the user for the figure.

## Verification

Treat any answer mismatch, wrong deck, duplicate note, missing note, wrong source scope, broken image reference, visible source/debug artifact, malformed MathJax, formula missing from `풀이`, or thin choice explanation as a blocker.

- Re-read saved notes through Anki MCP or AnkiConnect after creating the first few notes of a new source or scope.
- Treat the first 2-3 notes as a trial batch. Do not continue to the full write until their stored fields, deck, tags, images, and answers pass readback.
- For a complete batch, compare every saved answer against the matching answer key or solution section before reporting completion.
- For a complete batch, audit every saved note for searchable text fronts, missing/duplicate numbering, stale whole-page image references, source/debug artifacts, broken MathJax, answer lines that begin with bare MathJax, required formulas in `풀이`, and choice explanations that are too thin or merely repeat the choice.
- For correction work, use Anki readback as the authority. The pass is not complete until the stored Front and Back fields have been read and judged semantically.
- For image cards, confirm the saved field references the actual media filename and preserves aspect ratio.
- For mixed source roots, report which source IDs were touched and which were only inspected.
- Report the checked deck name, problem count, changed note IDs when available, and any corrected problem numbers.
- If real Anki or source PDFs were unavailable, report only the static or mocked checks that actually ran and list the remaining integration steps. Never imply cross-product or live-Anki compatibility from static tests.

## References

- Read `references/source-taxonomy.md` when classifying a source set or deciding deck structure.
- Read `references/source-details-template.md` when local source paths, manifests, deck conventions, or answer-key mapping are missing.
- Read `references/card-patterns.md` when choosing front/back structure or MathJax/HTML patterns.
- Read `references/crop-workflow.md` when using `scripts/crop_problem_images.py` for figure crops or media insertion.
- Read `references/quality-audit.md` before large correction passes or after a user reports poor explanations, broken OCR order, missing figures, or visible artifacts.

## Public Safety

- Never commit PDFs, rendered pages, cropped textbook images, Anki exports, local profile paths, answer-key dumps, or private deck data.
- Keep source-specific setup in `source-details.local.md`, a local manifest, or environment variables.
- Do not publish copied problem or solution text unless the user provides proof that redistribution is allowed.
