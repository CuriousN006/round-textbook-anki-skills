# Card Patterns

Use these patterns as starting points. Adapt field names to the user's actual note type.

## Front Field

```html
[OCR] 03. <cleaned problem prompt><br><br>
<div><img src="source_round03_q03.png" width="640" height="360" style="max-width:100%; height:auto;"></div><br>
1. <choice or statement><br>
2. <choice or statement><br>
3. <choice or statement><br>
4. <choice or statement>
```

Guidelines:

- Mark OCR-derived text when it may still need human/source verification.
- Put required images before choices or response options.
- Keep images focused on the figure, table, formula box, or prompt area that is needed for review.

## Back Field

```html
Answer: 2<br><br>

Why:<br>
<fresh explanation in teaching prose><br><br>

Formula:<br>
\[
  <main equation>
\]<br>

Symbol meanings:<br>
- \(a\): ...<br>
- \(b\): ...<br><br>

Trap:<br>
<common confusion, unit issue, sign convention, or boundary condition>
```

Guidelines:

- Use the solution source to confirm the answer, then write the explanation freshly.
- For statement-evaluation prompts, explain each printed statement in order when the prompt asks for correct/incorrect statements.
- For calculation prompts, show direct substitution before any mnemonic or shortcut.
- Use MathJax commands such as `\lt`, `\gt`, `\le`, and `\ge` instead of raw comparison symbols that may be parsed as HTML.

## Source Traceability

When the note type has a source or extra field, store compact trace data:

```text
source=<source nickname>; scope=<round/test/chapter>; problem=03; page=<page id>; answer_checked=yes
```

Do not store private absolute paths in public-facing fields unless the user explicitly wants local-only notes.
