# Card Patterns

Use these patterns as starting points. Adapt field names to the user's actual note type and source type.

## Multiple Choice Front

```html
[OCR] <source> / <scope> / 03<br><br>
<cleaned problem prompt><br><br>
<div><img src="source_scope_q03.png" width="640" height="360" style="max-width:100%; height:auto;"></div><br>
1. <choice or statement><br>
2. <choice or statement><br>
3. <choice or statement><br>
4. <choice or statement>
```

## Calculation or Short Answer Front

```html
[OCR] <source> / <scope> / 03<br><br>
<problem prompt with required data and units><br><br>
Find: <requested quantity>
```

## Interview or Concept Front

```html
<source> / <topic><br><br>
<question, prompt, or scenario>
```

## Back Field

```html
Answer: <final answer><br><br>

Why:<br>
<fresh explanation in teaching prose><br><br>

Formula or principle:<br>
\[
  <main equation or definition>
\]<br>

Symbol meanings:<br>
- \(a\): ...<br>
- \(b\): ...<br><br>

Trap or contrast:<br>
<common confusion, unit issue, sign convention, boundary condition, or adjacent concept>
```

Guidelines:

- Use solution material to confirm the answer, then write the explanation freshly.
- For statement-evaluation prompts, explain each printed statement in order when the prompt asks for correct/incorrect statements.
- For calculation prompts, show direct substitution before any mnemonic or shortcut.
- For interview/concept cards, include a model answer plus follow-up angle when it improves review value.
- Use MathJax commands such as `\lt`, `\gt`, `\le`, and `\ge` instead of raw comparison symbols that may be parsed as HTML.

## Source Traceability

When the note type has a source or extra field, store compact trace data:

```text
source_id=<id>; type=<source_type>; scope=<chapter/round/year/topic>; problem=03; page=<page id>; answer_checked=yes
```

Do not store private absolute paths in public-facing fields unless the user explicitly wants local-only notes.
