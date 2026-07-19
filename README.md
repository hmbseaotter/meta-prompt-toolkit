# Meta-Prompt Toolkit

A small toolkit that helps you write **great prompts** for AI models — and improve prompts you
already have. You describe what you want; it hands you a finished, copy-ready prompt.

It works best with Claude (where it can run as an automatic "skill"), and includes fallback
versions for Gemini and ChatGPT for when Claude isn't available.

---

## What this is (plain English)

Good AI results depend heavily on how you ask. This toolkit is a reusable "prompt for writing
prompts." You give it a use case — say, *"a prompt that reviews a contract and lists the key
terms"* — and it produces a well-structured prompt you can paste into an AI, plus a short note on
why it's built that way and how to tweak it.

## Why it exists

Writing a strong prompt every time is repetitive and easy to get wrong. This bottles up current
best practices (from Anthropic's official guidance) so you get consistent, high-quality prompts
without re-learning the rules each time. It also has an **improve mode**: paste a prompt that
isn't working, say what's wrong, and it suggests the smallest fix.

## What's in here

- `SKILL.md` — lets Claude use this automatically as a "skill" (see deploy steps below).
- `core/meta-prompt-core.md` — the engine. The reusable prompt itself. Works on any AI.
- `branches/anthropic.md` — extra tuning for Claude (Opus 4.8 / Sonnet 5). The main branch.
- `branches/gemini.md`, `branches/chatgpt.md` — fallback tuning for those models.
- `examples/worked-example.md` — one full worked pass, so you can see the expected output shape.
- `guardrails/collaboration-rules.md` — optional rules that make an AI a safer, more honest
  collaborator on bigger, multi-step work.

---

## How to use it — the quick way (any AI, no setup)

1. Open `core/meta-prompt-core.md`.
2. Copy the big block between the ``` marks (that's the engine).
3. Paste it into Claude, ChatGPT, or Gemini.
4. At the bottom, replace the `USE CASE` line with what you want, and send.
5. You'll get back a finished prompt to copy and use.

That's it. Everything below is for people who want Claude to use this **automatically**.

---

## How to deploy as a Claude skill (step by step, for beginners)

A "skill" means Claude picks this up on its own whenever you ask for prompt help — no copy-paste.
This requires **Claude Code** (Anthropic's command-line/desktop tool).

### 1. Get the toolkit onto your computer

If you have `git` installed, open a terminal and run (replace the URL with your repo's URL):

```
git clone https://github.com/YOUR-USERNAME/meta-prompt-toolkit.git
```

You should see a new folder called `meta-prompt-toolkit`. If you don't have `git`, you can instead
click the green **Code** button on the GitHub page, choose **Download ZIP**, and unzip it.

### 2. Put it where Claude Code looks for skills

Skills live in a `skills` folder. Copy the toolkit into your Claude skills directory.

**macOS / Linux:**

```
mkdir -p ~/.claude/skills
cp -r meta-prompt-toolkit ~/.claude/skills/meta-prompt
```

**Windows (PowerShell):**

```
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
Copy-Item -Recurse meta-prompt-toolkit "$env:USERPROFILE\.claude\skills\meta-prompt"
```

The **folder name is what matters** — the skill is named after the directory (`meta-prompt`), not
after anything inside the files. Make sure it ends up at
`.claude/skills/meta-prompt/SKILL.md`.

### 3. Check it's recognized

Skills load automatically — no restart needed, even if Claude Code is already open. To confirm,
open Claude Code and run:

```
/skills
```

You should see **meta-prompt** in the list. If you do, it worked.

### 4. Use it

Just ask naturally, for example:

> Write me a prompt for summarizing customer feedback into themes.

Claude will recognize this as a prompt-writing request and use the skill automatically. You don't
need to mention the skill by name.

---

## Updating the toolkit later

If you improve the toolkit, pull the latest version and re-copy it:

```
cd meta-prompt-toolkit
git pull
rm -rf ~/.claude/skills/meta-prompt
cp -r . ~/.claude/skills/meta-prompt
rm -rf ~/.claude/skills/meta-prompt/.git
```

(The `rm -rf` of the old copy prevents stale files lingering after a rename; removing `.git`
afterwards keeps repository internals out of your skills folder.)

---

## A note on privacy

Nothing in this repository contains personal or private information — it's all prompt text and
documentation. You can read every file before you run anything.

---

## Credits & basis

Built on current published prompt-engineering guidance: Anthropic's official Claude prompting
documentation for the core and main branch, Google's Gemini 3 developer guidance for the Gemini
branch, and OpenAI's current model and prompting guides for the ChatGPT branch. Every branch was
verified against live vendor sources at build time (July 2026), and each branch file names the
pages it was built from plus anything left unverified.

AI guidance evolves fast — and the vendors have recently moved in *different* directions on
sampling parameters, personas, and chain-of-thought. Re-check the branch files periodically
rather than assuming advice from one vendor transfers to another.
