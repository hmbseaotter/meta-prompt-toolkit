# Worked Example

One end-to-end pass through the engine, showing the expected output shape. Read this if you are
unsure what "finished, copy-ready prompt" means in practice.

---

## Example 1 — USE CASE mode (the default)

**User asks:**

> Write me a prompt for summarizing customer feedback into themes.

**Resolving ambiguity.** Two things are genuinely unclear: how many themes, and whether the reader
wants evidence or just labels. Neither is worth a blocking question, so state assumptions instead
of asking:

> Assumption: the audience is a product team that needs to act on this, so each theme carries
> supporting quotes and a rough frequency.
> Assumption: input is a batch of free-text responses, not a live feed.

**Task classification:** classification/extraction + light analysis. Not high-stakes, not agentic,
not long-document. So: no anti-hallucination block, no research block, no chaining. Output must
match a repeatable shape, so a schema is worth specifying. Volume of feedback is unbounded, so a
count clamp matters.

### 1) THE PROMPT

```
<task>
Group the customer feedback below into recurring themes, so a product team can decide what to
fix first.
</task>

<feedback>
{{paste feedback here — one response per line}}
</feedback>

<instructions>
Identify 3-7 themes. A theme is a recurring underlying issue or desire, not a restatement of one
comment — merge near-duplicates rather than listing them separately.

For each theme give:
- A short label (under 8 words)
- How many responses it covers, and roughly what share of the total
- One or two verbatim quotes that best represent it
- Whether it reads as a bug, a missing feature, or a usability friction

Order themes by how many responses they cover, most first.

Use only what appears in the feedback. If something is mentioned once and fits nothing else, put
it under a final "Isolated mentions" list rather than inflating it into a theme.
</instructions>

<output_spec>
A markdown table with columns: Theme | Count | Share | Type | Representative quotes.
Then, below the table, one short paragraph (3-5 sentences) naming what you would fix first and
why.
</output_spec>
```

### 2) WHY IT WORKS

- Classification task, so the theme *definition* is stated explicitly — without it, models return
  one theme per comment.
- The 3-7 clamp and the "Isolated mentions" escape hatch together prevent both over-splitting and
  the opposite failure, forcing a stray comment into a theme it doesn't belong to.
- Verbatim quotes anchor each theme to real evidence, which makes the output auditable.
- The closing paragraph converts a description into a decision, which is what the audience
  actually needs.

### 3) SETTINGS

For chat use, nothing. For API use, see the branch file for your model — this task is
light-to-moderate reasoning, so mid-tier effort is enough. Do not set a temperature unless your
model's branch file says it applies.

### 4) HOW TO IMPROVE

- If themes come back too broad, lower the range to 3-5 and add "prefer specific over general."
- If you have a fixed taxonomy already, replace the open-ended grouping with your category list
  and switch this to a straight classification prompt with examples.
- For very large batches, split into a CHAINING pipeline: theme-extract per batch, then a merge
  pass that reconciles the batch-level themes.

---

## Example 2 — IMPROVE mode

**User provides:**

> EXISTING PROMPT: "Summarize this article."
> WHAT IT SHOULD DO: give me something I can paste into a weekly digest
> WHAT IT DOES INSTEAD: gives a long generic summary, different length every time

**The diagnosis, and the discipline.** Three of the four essentials are missing: no audience, no
format, no length clamp. Improve mode means the smallest change that fixes the named problem —
not a rewrite. So keep "summarize this article" and add only what is missing:

```
Summarize this article for a weekly email digest read by busy non-specialists.

Write 2-3 sentences: what the article claims, and why it matters to someone in {{field}}.
Lead with the claim, not with "This article discusses...".

<article>
{{paste article}}
</article>
```

**What changed and why:** the audience fixes the register, the sentence count fixes the variable
length, and the "lead with the claim" line kills the throat-clearing opener that makes digest
entries unreadable. The original instruction survives intact.

Note what was NOT added: no role, no "you are an expert editor," no quality rubric, no
step-by-step breakdown. The prompt failed for want of specification, not for want of scaffolding
— adding scaffolding would have been the wrong fix.
