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

**First, decide which of these you are.** It changes what you should do, and picking wrong is
mildly annoying to undo later.

**(a) You just want to USE the toolkit as-is.** Most people. Download it and you're done:

Click the green **Code** button at the top of the GitHub page, choose **Download ZIP**, and unzip
it. You'll get a folder called `meta-prompt-toolkit`. That's everything. Skip to step 2.

(If you have `git` and prefer the terminal, `git clone https://github.com/hmbseaotter/meta-prompt-toolkit.git`
does the same thing.)

**(b) You want to CHANGE it and keep your changes.** Edit the prompts, add your own branch file,
tune it to how you work. Then **fork it first** — a fork is your own copy of the repo, under your
own GitHub account, that you can freely save changes to.

To fork: on the GitHub page, click **Fork** (top right) → **Create fork**. GitHub makes a copy at
`github.com/YOUR-USERNAME/meta-prompt-toolkit`. Then download or clone **your fork**, not this one:

```
git clone https://github.com/YOUR-USERNAME/meta-prompt-toolkit.git
```

Replace `YOUR-USERNAME` with your actual GitHub username.

> **Why fork instead of just cloning?** If you clone this repo directly and later try to `git push`
> your changes, it will fail with a permission error — you don't have write access to someone
> else's repository, and GitHub won't let you write to mine. Nothing breaks and nothing of mine is
> touched, but your work has nowhere to go. Forking first gives your changes a home from the start.
>
> Already cloned directly and made changes? Nothing is lost. Fork the repo on GitHub, then point
> your copy at the fork:
> `git remote set-url origin https://github.com/YOUR-USERNAME/meta-prompt-toolkit.git`

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

### How current is this?

**Everything here was checked against the vendors' own live documentation in July 2026.**

That date matters, because AI guidance changes fast — parts of this were *already* out of date
within months of the underlying models shipping. Some concrete examples of what changed: Anthropic
replaced the `budget_tokens` setting with `effort`; Google stopped recommending the `temperature`
setting on Gemini 3 entirely; OpenAI reversed its own advice on how much detail to put in a prompt.

**To see how stale this might be:** each branch file (`branches/anthropic.md`, `branches/gemini.md`,
`branches/chatgpt.md`) states, at the top, which vendor pages it was built from and when — plus
anything the author couldn't verify. Start there.

**To see when this repo was last touched at all:** on the GitHub page, the file list shows the date
of the most recent change to each file, and clicking **Commits** (or the clock icon) shows the full
history with dates. If that was a long time ago, treat the vendor-specific settings tables with
suspicion and check the vendor's own docs.

Sources: Anthropic's official Claude prompting documentation for the core and the Claude branch;
Google's Gemini 3 developer guidance for the Gemini branch; OpenAI's current model and prompting
guides for the ChatGPT branch.

One warning worth repeating: the vendors have recently moved in *different* directions on sampling
parameters, personas, and chain-of-thought. Advice that is correct for one model can actively hurt
another. Don't assume it transfers — that's exactly why this toolkit keeps them in separate branch
files.
