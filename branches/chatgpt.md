# ChatGPT / GPT Branch (GPT-5.6 fallback)

Layered ON TOP of `core/meta-prompt-core.md`. Apply these when the target model is a current GPT
model. Verified against OpenAI's live docs (prompt-guidance, latest-model, and reasoning guides at
developers.openai.com) at build time.

This is a SECONDARY fallback branch. The Claude branch is the primary.

DOC LOCATION NOTE: `platform.openai.com/docs/*` now redirects to `developers.openai.com/api/docs/*`,
and `cookbook.openai.com` redirects to `developers.openai.com/cookbook/*`. Any older bookmark is
stale.

---

## The headline delta: leaner prompts measurably win

OpenAI reports that simplified prompts improved evaluation scores by roughly 10-15% while cutting
tokens by 41-66%. This is a deliberate reversal of the GPT-5-era playbook. When generating a
prompt for GPT, cut: repeated instructions and examples, generic tool descriptions, redundant
guidance ("ask first", "be concise"), and reassurance or sign-off filler.

## Override the core: state each instruction EXACTLY ONCE

The core (and common practice) tolerates restating key rules for emphasis. On GPT this actively
degrades behavior, and long sessions amplify the damage. Keep each policy in exactly one location.
This is the single biggest trap when porting a Claude-tuned prompt to GPT.

## Outcome-first, not process-first

State the goal, relevant context, constraints, required evidence, success criteria, and output
format. Do not prescribe how the model should think. Explicit "think step by step" instructions
are called out as unnecessary for reasoning models - internal deliberation is already built in.
Use `reasoning.effort` instead of prompt text.

## Verbosity does NOT self-calibrate from vague instructions

Unlike Claude, GPT handles "be concise" poorly - it can go too brief. Specify what a shorter
answer must PRESERVE, not just that it should be short. Example of the right shape:

"Lead with the conclusion. Include the evidence needed to support it, any material caveat, and the
next action."

Concrete defaults worth stating: 3-6 sentences or up to 5 bullets for a typical answer; at most
2 sentences for a simple yes/no.

## Role / persona - de-emphasized (opposite of Gemini)

Define tone through specific behavioral choices, not persona labels. Avoid vague descriptors like
"friendly." Prefer: "State the answer directly. If the user reports a problem, acknowledge the
specific issue before giving the next step." OpenAI's older reasoning guidance goes further and
lists persona prompts that might contradict the model's reasoning process as an anti-pattern.

This is a genuine vendor split - Gemini still endorses `<role>` tags. Keep role handling in the
branch files, not the core.

## Structure

XML tags are preferred over pure markdown for complex or bounded constraint blocks - e.g.
`<tool_orchestration>`, `<output_verbosity_spec>`, `<tool_usage_rules>`.

## Agentic / tool use

- Autonomy boundary, stated once: "For requests to answer, explain, review, diagnose, or plan,
  report the result. Do not implement changes unless the request also asks for them."
- Require confirmation ONLY for external writes, destructive actions, or scope expansion. Repeated
  approval requests for safe, expected actions are a documented anti-pattern.
- Stop conditions: "Stop when [condition] is met. Retry transient failures at most [R] times. Do
  not repeat completed calls."
- Parallelism: run independent reads concurrently when safe; use sequential direct calls when each
  result may change the next decision.
- Tool preambles - a reversal from GPT-5 era. Do not narrate routine operations ("reading
  file...", "running tests..."). Give a brief 1-2 sentence update only when starting a major new
  phase or discovering something that changes the plan, and make each update carry a concrete
  outcome ("Found X", "Confirmed Y").
- Tool descriptions: 1-2 sentences on what the tool does and when to use it. No more.

## Documented anti-patterns

Telling the model to "use pro mode" or "think harder"; generic efficiency instructions without
task-specific routing; broad brevity instructions that yield too-brief answers; relying on tool
availability alone to route work.

## Settings quick-reference (GPT-5.6)

Models: `gpt-5.6-sol` (flagship), `gpt-5.6-terra` (strong, cheaper), `gpt-5.6-luna` (efficient,
high-volume). `gpt-5.6` is an alias routing to `sol`.

| Setting | Values | Notes |
|---|---|---|
| reasoning.effort | none, low, medium, high, xhigh, max | `minimal` valid on some other models |
| reasoning.mode | standard (default), pro | pro adds work/latency, bills at standard rates |
| text.verbosity | low, medium, high | |
| summary | "auto" | org verification may be required |

- Treat `reasoning.effort` as a tuning knob, not the primary way to recover quality. Start from
  your prior baseline and TEST ONE LEVEL LOWER - 5.6 often holds quality with fewer tokens.
  Reserve `max` for the hardest quality-first workloads.
- Migration mapping: GPT-4o / 4.1 behavior maps to `none`; GPT-5's `minimal` maps to `none`.
- `temperature` / `top_p` are not listed as supported parameters for GPT-5.6. Do not carry
  "temperature ~0 for factual tasks" advice into a GPT-5.6 prompt.
- DEPRECATED: reusable prompt objects (`v1/prompts`) shut down 2026-11-30. Do not build on prompt
  IDs.
- With `store: false` or ZDR, reasoning items carry `encrypted_content` for stateless continuity.

## Not verified at build time

A GPT-5.6-specific cookbook prompting guide could not be located (the expected path 404s).
Content above comes from the official prompt-guidance and latest-model docs. The
reasoning-best-practices page still references o1/o3-era models and is likely stale; items sourced
only from it are flagged inline above.
