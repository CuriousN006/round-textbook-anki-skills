# Source Taxonomy

Classify the source before deciding deck shape or card pattern.

## Types

| Type | Signals | Anki strategy |
| --- | --- | --- |
| `problem_bank` | One PDF, many numbered problems, answers may appear later in the same file | Deck per source; optional subdecks by topic or page range |
| `chapter_bank` | Chapter/topic headers, section-based numbering or topic clusters | Deck per source, subdeck/tag per chapter or topic |
| `mock_rounds` | Repeated tests, rounds, or sets where numbering restarts | Subdeck/tag per round; verify banner before each batch |
| `past_exam` | Year, agency/company, exam session, fixed problem count | Deck or tag by agency/year/session; preserve original numbering |
| `split_problem_solution` | Separate problem PDF and solution/explanation PDF | Pair files in the manifest; verify problem scope and matching solution section |
| `interview_or_concept` | Interview, oral exam, formula, definition, explanation, or summary material | Convert to Q&A, comparison, scenario, or concept cards; do not force MCQ |
| `mixed` | Folder contains several independent PDFs or source types | Build a source manifest first; work one source or scope at a time |

## Organization Hints

- `continuous`: problem numbers run from start to end without restarting.
- `chapter`: headers or contents divide the source into subject sections.
- `topic`: each subsection is a concept cluster rather than a formal chapter.
- `round`: each test or mock round restarts numbering.
- `exam_session`: source is anchored by year, agency, or session name.
- `qa_sections`: interview or concept material is organized as questions, answers, or headings.

## Decision Rules

- If there is a separate solution file, classify as `split_problem_solution` even when the problem file itself is round-based or chapter-based.
- If numbers restart, the scope label is part of the identity. `Round 2 / Problem 01` is not the same as `Round 1 / Problem 01`.
- If the source is a real past exam, preserve the year/agency/session in tags or source trace even when the target deck is topic-based.
- If a source mixes concept summaries and problems, split the Anki task by card type rather than forcing one template.
- If the source folder has many unrelated PDFs, create a manifest and touch only the requested source IDs.
