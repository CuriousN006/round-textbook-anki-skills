# Quality Audit

Use this before large correction passes and whenever a user reports poor cards. The goal is semantic card quality, not just clean HTML.

## Direct Review Rule

- Read saved notes through Anki in small batches. Judge the actual `Front` and `Back` fields, not a generated payload, search result, or mechanical audit.
- Do not use automated checks as a discovery method for bad explanations. They cannot tell whether reasoning is shallow, copied, misleading, or missing the point.
- A correction pass is not complete until the suspicious pattern has been checked across the whole affected deck or source.

## Front Field Checklist

- Problem text and choices are searchable OCR or transcription.
- Reading order matches the source: prompt, `<보기>` or table if present, then answer choices.
- Whole-page or whole-problem images are removed unless the user explicitly asked for image-first review.
- Figure-dependent prompts include a focused crop of the original figure, graph, table, or symbol legend.
- Image HTML preserves aspect ratio and references a real media filename.

## Back Field Checklist

- The first line gives the final answer.
- The main explanation contains the necessary formula, substitution, definition, classification rule, or mechanism.
- Formula-heavy answers are split into readable steps.
- Every symbol used in a formula is defined near the formula.
- A reference or note section only adds traps, comparisons, unit checks, or memory aids; it must not hide the core solution.
- No literal placeholders remain, including `Mathjax`, `MathJax`, `source_id=`, `answer_checked=`, `problem=`, `page=`, or similar debug metadata.

## Choice And Statement Questions

- If the prompt asks for correct/incorrect choices, counts, or "not true" items, explain every printed statement or choice in order.
- Each item needs a reason: boundary, exception, formula, process mechanism, material classification, unit conversion, or counterexample.
- Do not write generic filler such as "this is included in the category" without naming the category rule.
- If the source answer is questionable, state the source-standard answer and add a concise caveat.

## Common Failure Patterns

- OCR put the numeric answer choices before the `<보기>` block.
- A diagram was replaced by a text summary even though the graph, geometry, or symbol placement matters.
- The card copied a textbook table as broken line fragments instead of rewriting the useful content.
- The explanation merely repeats the printed choice.
- The core formula appears only in a reference/note section.
- Dense derivations are crammed into one line or one paragraph.
- Generated cards still contain internal trace strings or renderer placeholders.
