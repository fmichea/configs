#!/usr/bin/env python3
"""Tracks when each repository was last checked with /repo-check.

`repo-check.py offer` is a SessionStart hook: inside a repository not checked
in the last MAX_AGE_DAYS, it shows the user a notice and gives Claude context
asking it to offer /repo-check.
`repo-check.py mark` records the repository of the current directory as
checked; the skill runs it after a check, and Claude after the user declines.

Each repository has an empty file in STATE_DIR, named after the path of its
main checkout so worktrees share it; the file's modification time is the date
of the last check.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

STATE_DIR = Path(os.environ.get("CLAUDE_REPO_CHECK_DIR", Path.home() / ".claude" / "repo-check"))
MAX_AGE_DAYS = 30
OFFER = (
    "This repository has not been checked with /repo-check in the last {days} days. "
    "Offer once, in one line, to run /repo-check, which audits it against the user's "
    "standards. If the user declines, run `~/.claude/hooks/repo-check.py mark` so the "
    "offer waits another {days} days."
)
# Shown to the user when the session opens, since Claude speaks only once prompted.
NOTICE = "Not checked with /repo-check in {days} days: run /repo-check, or tell Claude to skip it."


def main_checkout(cwd: str) -> Path | None:
    """The main checkout of the repository containing cwd, or None outside one."""
    result = subprocess.run(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).parent


def state_file(repo: Path) -> Path:
    return STATE_DIR / str(repo).replace("/", "-")


def checked_recently(repo: Path) -> bool:
    try:
        age = time.time() - state_file(repo).stat().st_mtime
    except FileNotFoundError:
        return False
    return age < MAX_AGE_DAYS * 24 * 3600


def offer() -> None:
    try:
        cwd = json.load(sys.stdin)["cwd"]
    except (ValueError, KeyError, TypeError):
        return
    repo = main_checkout(cwd)
    if repo is None or checked_recently(repo):
        return
    context = {
        "hookEventName": "SessionStart",
        "additionalContext": OFFER.format(days=MAX_AGE_DAYS),
    }
    output = {
        "systemMessage": NOTICE.format(days=MAX_AGE_DAYS),
        "hookSpecificOutput": context,
    }
    print(json.dumps(output))


def mark() -> None:
    repo = main_checkout(os.getcwd())
    if repo is None:
        sys.exit("repo-check: not inside a git repository")
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_file(repo).touch()
    print(f"repo-check: marked {repo} as checked")


def main() -> None:
    commands = {"offer": offer, "mark": mark}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        sys.exit("usage: repo-check.py offer|mark")
    commands[sys.argv[1]]()


if __name__ == "__main__":
    main()
