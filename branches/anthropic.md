# Claude Branch (Opus 4.8 / Sonnet 5 tuning)

Layered ON TOP of `core/meta-prompt-core.md`. Use the core as the engine; apply these Claude-
specific adjustments when the target model is Claude. Verified against Anthropic's live prompting
docs (general best-practices + Opus 4.8 page) at build time.

This is the PRIMARY branch and the source of truth for the SKILL. The Gemini and ChatGPT
branches are thin fallback exports.

---

## What Claude does well out of the box (so you can prompt LIGHTER)

- Reasons well on its own. Prefer "reason through this carefully" over a hand-written step list.
  Claude's own reasoning frequently exceeds a prescribed recipe.
- Calibrates response length to task complexity; it is less verbose by default and may skip
  verbal summaries after tool calls.
- Parses XML tags very reliably - lean into them for structure (Claude benefits from this more
  than most models).
- Runs independent tool calls in parallel automatically.
- Is less prone to hallucination and grounds answers in opened files/sources.

Because of this, the core's "avoid over-scaffolding" note matters MORE on Claude. Drop quality
rubrics, forced step lists, and "CRITICAL/YOU MUST" language unless a plainer prompt fell short.

## Literal instruction following (important - promote to a top rule)

Opus 4.8 and Sonnet 5 interpret prompts literally and do NOT silently generalize one instruction
to other items, nor infer requests you didn't make. Precise, but you must be explicit:
- State scope: "Apply this to every section, not just the first."
- Say action vs advice outright: "Make the edits" (not "can you suggest changes?"), or the
  reverse if you only want recommendations.
- Give the full task and constraints up front in the first turn; Claude is autonomous and rewards
  well-specified initial prompts over drip-fed context.

## Over-eagerness / over-engineering (watch this, especially in Claude Code)

Claude can over-build: extra files, unnecessary abstractions, unrequested flexibility. When
generating prompts for coding/agent tasks, include scope-limiting language, e.g.:
"Only make changes directly requested or clearly necessary. Don't add features, refactors,
docstrings to untouched code, defensive handling for impossible cases, or abstractions for
one-time operations. The right amount of complexity is the minimum needed for the current task."

## Effort & thinking (the main API lever - replaces budget_tokens)

`budget_tokens` is deprecated (400 error on Opus 4.7+/Sonnet 5). Use the `effort` parameter:
- xhigh - best for coding and agentic use cases (Opus 4.8 default recommendation).
- high  - minimum for most intelligence-sensitive work; balances tokens vs intelligence.
- medium- cost-sensitive; some risk of under-thinking on complex tasks.
- low   - short, scoped, latency-sensitive tasks only.
- max   - intelligence-demanding tasks; can overthink; test before relying on it.
If reasoning looks shallow on a hard task, RAISE effort rather than prompting around it. Thinking
is off unless you set `thinking: {type: "adaptive"}`; adaptive thinking generally beats the old
manual extended thinking. At `max`/`xhigh`, set a large max output budget (start ~64k).

## Subagents (relevant to your agent/skill work)

Opus 4.8 spawns FEWER subagents by default; steerable. Give explicit guidance when you want them:
"Don't spawn a subagent for work you can do directly in one response. Spawn subagents when
fanning out across items or reading multiple files in parallel."

## Verbosity control

If output is too long/short, prompt directly and prefer POSITIVE concision examples over "don't"
instructions, e.g.: "Provide concise, focused responses. Skip non-essential context, keep
examples minimal." If you want visible progress summaries in agent runs, ask for them explicitly
(Claude may skip them by default).

## Tool triggering & anti-overtriggering

Opus 4.8 favors reasoning over tool calls (usually good). To get MORE tool use, raise effort to
high/xhigh, or describe when/why to use the tool. Do NOT use "CRITICAL: you MUST use this tool" -
on these models that causes OVER-triggering; plain "Use this tool when..." is correct.

## Design / frontend defaults (relevant to Claude Design work)

Opus 4.8 has a persistent house style (warm cream #F4F1EA, serif display, terracotta accent) that
suits editorial/hospitality but not dashboards/dev-tools/fintech/healthcare. Generic negatives
("don't use cream", "make it clean") just shift it to another fixed palette. Two reliable fixes:
1. Specify a concrete alternative (exact palette hexes, typeface, radii, spacing).
2. Ask it to propose 3-4 distinct visual directions first, then build the chosen one.

## Settings quick-reference (Claude)

| Setting | When | Value |
|---|---|---|
| effort | coding / agentic | xhigh |
| effort | intelligence-sensitive | high (minimum) |
| effort | cost-sensitive | medium |
| effort | short/latency-sensitive | low |
| thinking | multi-step reasoning / agent loops | {type: "adaptive"} |
| max output tokens | at xhigh/max | start ~64k |
| temperature | factual/extraction/math | ~0 |
| temperature | creative | 0.7-0.9 |
