#!/usr/bin/env python3
"""Install the Meta-Prompt Toolkit as a Claude Code skill.

Copies this folder into your Claude skills directory so Claude picks it up
automatically. Works on Windows, macOS, and Linux.

Usage:
    python install.py              install (or update an existing install)
    python install.py --uninstall  remove it again
    python install.py --where      just show where things would go

Nothing outside your Claude skills folder is touched.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Final

SKILL_NAME: Final[str] = "meta-prompt"

# Copied into the installed skill. Everything else here (git internals, this
# installer, editor leftovers) stays behind.
PAYLOAD: Final[tuple[str, ...]] = (
    "SKILL.md",
    "README.md",
    "core",
    "branches",
    "guardrails",
    "examples",
)

# A real install must contain these, or the skill silently does nothing.
REQUIRED: Final[tuple[str, ...]] = ("SKILL.md", "core")


def skills_dir() -> Path:
    """The Claude skills folder for the current user, on any OS."""
    return Path.home() / ".claude" / "skills"


def say(message: str = "") -> None:
    print(message)


def fail(message: str, hint: str = "") -> None:
    say()
    say(f"  PROBLEM: {message}")
    if hint:
        say(f"  TRY THIS: {hint}")
    say()
    sys.exit(1)


def check_source(source: Path) -> None:
    missing = [name for name in REQUIRED if not (source / name).exists()]
    if missing:
        fail(
            f"this doesn't look like the toolkit folder - missing {', '.join(missing)}",
            "Run this script from inside the meta-prompt-toolkit folder, e.g. "
            "'cd meta-prompt-toolkit' first.",
        )


def install(source: Path, target: Path) -> None:
    check_source(source)
    replacing = target.exists()

    if replacing:
        say(f"  Found an existing install at: {target}")
        say("  Replacing it with this version.")
        shutil.rmtree(target)

    target.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    for name in PAYLOAD:
        item = source / name
        if not item.exists():
            continue  # optional pieces may legitimately be absent
        if item.is_dir():
            shutil.copytree(item, target / name)
        else:
            shutil.copy2(item, target / name)
        copied.append(name)

    say()
    say("  DONE. Installed:")
    for name in copied:
        say(f"    - {name}")
    say()
    say(f"  Location: {target}")
    say()
    say("  WHAT TO DO NEXT")
    say("    1. Open Claude Code. (If it's already open, that's fine - no restart needed.)")
    say("    2. Type  /skills  and press Enter. You should see 'meta-prompt' listed.")
    say("    3. Try it. Ask Claude, in plain English:")
    say('         "Write me a prompt for summarizing customer feedback into themes."')
    say()
    say("  Claude will use the skill on its own. You never have to name it.")
    say()


def uninstall(target: Path) -> None:
    if not target.exists():
        say()
        say(f"  Nothing to remove - no install found at: {target}")
        say()
        return
    shutil.rmtree(target)
    say()
    say(f"  Removed: {target}")
    say("  Claude will stop offering the skill straight away.")
    say()


def main() -> None:
    parser = argparse.ArgumentParser(add_help=True, description=__doc__)
    parser.add_argument("--uninstall", action="store_true", help="remove the installed skill")
    parser.add_argument("--where", action="store_true", help="show paths and exit, change nothing")
    args = parser.parse_args()

    source = Path(__file__).resolve().parent
    target = skills_dir() / SKILL_NAME

    say()
    say("  Meta-Prompt Toolkit installer")
    say("  " + "-" * 30)

    if args.where:
        say(f"  Toolkit folder:  {source}")
        say(f"  Would install to: {target}")
        say(f"  Currently installed: {'yes' if target.exists() else 'no'}")
        say()
        return

    if args.uninstall:
        uninstall(target)
        return

    try:
        install(source, target)
    except PermissionError:
        fail(
            "no permission to write to your Claude skills folder",
            "Close Claude Code and run this again. On Windows, avoid running it "
            "from inside a folder like Program Files.",
        )
    except OSError as exc:
        fail(f"could not copy the files ({exc})", "Check you have free disk space, then retry.")


if __name__ == "__main__":
    main()
