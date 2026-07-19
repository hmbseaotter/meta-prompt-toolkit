# Gemini Branch (Gemini 3.x fallback)

Layered ON TOP of `core/meta-prompt-core.md`. Apply these when the target model is Gemini.
Verified against Google's live docs (Gemini 3 developer guide, updated 2026-07-07; Gemini 3.5
Flash what's-new, 2026-07-06; prompt design strategies, 2026-06-10) at build time.

This is a SECONDARY fallback branch. The Claude branch is the primary.

---

## The headline delta: prompt SHORTER than the core suggests

Gemini 3 "responds best to direct, clear instructions" and "may over-analyze verbose or overly
complex prompt engineering." Techniques designed for older models actively hurt here. When
generating a prompt for Gemini, strip the core's optional blocks harder than you would for Claude
- keep the four essentials and little else unless the task genuinely needs more.

## Override the core: DO NOT hand-write chain-of-thought

The core prefers "reason through this carefully" over step lists. On Gemini 3.x, drop even that -
explicit CoT scaffolding is no longer necessary and adds over-analysis risk. Control reasoning
with the `thinking_level` parameter instead of with prompt text.

## Override the core: DO NOT set sampling parameters

`temperature`, `top_p`, and `top_k` are NO LONGER RECOMMENDED on Gemini 3.x; migration guidance
says remove them entirely. Default temperature is 1.0, and Google warns that lowering it "can
cause unexpected behavior, such as looping or degraded performance."

This directly contradicts the usual "temperature ~0 for factual/extraction" advice. Do not carry
that advice into a Gemini prompt. `candidate_count` is also unsupported on 3.x.

## Context placement (stronger than the core's long-document rule)

The core applies "long material at top, question at bottom" only to long documents. On Gemini,
apply it generally: supply all the context first, and place the specific instruction or question
at the very end. Anchor the question explicitly - open it with "Based on the preceding
information...".

## Structure

XML-style tags and Markdown headings are equally effective - neither is privileged. What matters
is picking one and using it consistently throughout the prompt.

## Verbosity

Gemini 3 is less verbose by default and prefers direct, efficient answers. If you want a
conversational or expansive tone, ask for it explicitly; it will not happen by default.

## Role / persona

Google still endorses roles - define them in `<role>` tags or a markdown header, placed in system
instructions or at the very start of the prompt ("You are a senior solution architect."). This is
a genuine vendor split: keep roles for Gemini even where you would drop them for GPT.

## Few-shot examples - a live tension in Google's own docs

The prompt-strategies page says to "always include few-shot examples." The newer Gemini 3 guide
pushes minimalism and lists too many examples as an overfitting anti-pattern. Weight the newer,
model-specific guidance: include examples when output must match a pattern (as the core says), but
keep the count low and do not add them reflexively.

## Other documented anti-patterns

Stop sequences that could appear in natural output; overly persuasive or emphatic language;
modifying sampling parameters (see above).

## Multi-turn: thought signatures

Gemini returns encrypted `thought` blocks that maintain reasoning continuity across turns. With
`store: true` the server handles them. In stateless mode you MUST resend all `thought` blocks
exactly as received, or reasoning continuity breaks.

## Settings quick-reference (Gemini)

`thinking_level` is the primary lever - but VALID VALUES AND DEFAULTS DIFFER PER MODEL. Do not
assume a uniform four-level scale.

| Model | Default | Supported values |
|---|---|---|
| gemini-3.1-pro-preview | high | low, medium, high |
| gemini-3-pro-preview | high | low, high (NO medium) |
| gemini-3-flash-preview | high | minimal, low, medium, high |
| gemini-3.5-flash | medium | minimal, low, medium, high |
| gemini-2.5-flash-lite | off | low, medium, high |

- `thinking_budget` - legacy, superseded by `thinking_level`. Cannot be combined with it.
- `temperature` / `top_p` / `top_k` / `candidate_count` - omit entirely on 3.x.
- `media_resolution_high` - for dense document parsing.
- `thinking_summaries` - "auto" or "none".

Model knowledge cutoff is January 2025; use Search Grounding for anything more recent.

## Not verified at build time

Vertex AI's separate prompt-design documentation was not checked. If the user is on Vertex rather
than the Gemini API, treat these settings as needing confirmation.
