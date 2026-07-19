---
name: meta-prompt
description: Use when the user wants help writing, generating, or improving a prompt for an LLM - e.g. "write me a prompt for...", "turn this into a prompt", "help me prompt for...", "improve this prompt", or when they hand over a use case and want a polished, reusable prompt back. Produces a finished, copy-ready prompt (not advice about prompting). Also applies when the user references the CoSTAR framework or asks for a prompt built to a named structure.
---

# Meta-Prompt Skill

Turn a USE CASE into ONE finished, copy-ready prompt, or improve an existing prompt. Deliver an
actual prompt, not general advice.

## How to run

1. Read `core/meta-prompt-core.md` and follow its steps - it is the engine and it governs.
2. Apply the branch file for the model the user will RUN the prompt on - not the model you are:
   - Claude (the default here) -> `branches/anthropic.md`
   - Gemini -> `branches/gemini.md`
   - ChatGPT / GPT -> `branches/chatgpt.md`
   Branches override the core where they conflict; they exist because the vendors genuinely
   disagree (on roles, sampling parameters, repetition, and chain-of-thought). If the user hasn't
   said which model, ask - it changes the output.
3. If unsure what the finished output should look like, read `examples/worked-example.md`. It
   shows one full USE CASE pass and one IMPROVE pass.
4. If the user is building a multi-step working session, agent, or skill - not just a one-shot
   prompt - also offer the rules in `guardrails/collaboration-rules.md`.

## The two non-negotiables

- **Never guess silently.** Ask up to 3 focused questions, or state a labeled "Assumption:".
- **Deliver a prompt, not advice.** THE PROMPT in one code block, then WHY IT WORKS, SETTINGS,
  HOW TO IMPROVE.

Everything else - the four essentials, technique selection, the optional blocks - lives in the
core file. Follow it there rather than from memory.

## Presenting choices to the user

When a decision is needed, present it as a short list, recommended option first with a one-line
reason and trade-offs, and leave room for the user to choose otherwise. Don't bury questions in
prose.
