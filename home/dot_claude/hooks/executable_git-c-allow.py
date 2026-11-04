#!/usr/bin/env python3
"""PreToolUse hook for Bash: approves `git [-C <path>] <subcommand> ...`.

Permission rules match from the start of the command, so a rule such as
`Bash(git status)` never matches `git -C <path> status`, and a rule cannot
exclude a flag such as `--force` that may appear anywhere. This hook approves
git calls when the repository path (or the cwd, without `-C`) is inside a
working directory, the subcommand is on SAFE_SUBCOMMANDS and no unsafe option
is present. Anything else prints nothing and goes through the normal
permission flow. Deny and ask rules still apply to approved calls.
"""

import json
import os
import shlex
import sys
from pathlib import Path

SAFE_SUBCOMMANDS = {
    ("status",),
    ("diff",),
    ("log",),
    ("show",),
    ("fetch",),
    ("pull", "--ff-only"),
    ("add",),
    ("commit",),
    ("worktree", "add"),
    ("worktree", "list"),
    ("worktree", "remove"),
    ("branch", "--list"),
    ("branch", "--show-current"),
    # ~/.zsh/bin/git-wt-*: refuse to remove anything unmerged or uncommitted.
    ("wt-add",),
    ("wt-cleanup",),
}
# Options that write files, read files outside the repository (`diff
# --no-index` compares any two paths), run programs named on the command line,
# or skip git's safety checks (`worktree remove --force` discards uncommitted
# changes).
UNSAFE_OPTION_PREFIXES = ("--output", "--no-index", "--upload-pack", "--force")
UNSAFE_OPTIONS = {"-f", "-ff"}
SHELL_OPERATOR_CHARS = set("();<>|&")
EXPANSION_CHARS = set("$`\n")


def tokenize(command: str) -> list[str] | None:
    """Split a simple command into words; None if it uses any shell syntax."""
    if EXPANSION_CHARS & set(command):
        return None
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    # shlex starts a comment at any `#`, the shell only at the start of a word.
    lexer.commenters = ""
    try:
        tokens = list(lexer)
    except ValueError:
        return None
    if any(set(token) <= SHELL_OPERATOR_CHARS for token in tokens):
        return None
    return tokens


def working_directories(cwd: str) -> list[Path]:
    settings = Path.home() / ".claude" / "settings.json"
    try:
        extra = json.loads(settings.read_text())["permissions"]["additionalDirectories"]
    except (OSError, ValueError, KeyError, TypeError):
        extra = []
    return [Path(os.path.realpath(os.path.expanduser(d))) for d in [cwd, *extra]]


def is_inside(path: str, roots: list[Path]) -> bool:
    resolved = Path(os.path.realpath(os.path.expanduser(path)))
    return any(resolved == root or root in resolved.parents for root in roots)


def is_unsafe_option(arg: str) -> bool:
    return arg in UNSAFE_OPTIONS or arg.startswith(UNSAFE_OPTION_PREFIXES)


def is_safe_subcommand(args: list[str]) -> bool:
    if any(is_unsafe_option(arg) for arg in args):
        return False
    return any(tuple(args[: len(sub)]) == sub for sub in SAFE_SUBCOMMANDS)


def split_git_command(tokens: list[str], cwd: str) -> tuple[str, list[str]] | None:
    """Return (repository path, subcommand args), or None if not a plain git call."""
    if len(tokens) >= 4 and tokens[:2] == ["git", "-C"]:
        return tokens[2], tokens[3:]
    if len(tokens) >= 2 and tokens[0] == "git" and not tokens[1].startswith("-"):
        return cwd, tokens[1:]
    return None


def should_allow(command: str, cwd: str) -> bool:
    tokens = tokenize(command)
    split = split_git_command(tokens or [], cwd)
    if split is None:
        return False
    repo, args = split
    return is_inside(repo, working_directories(cwd)) and is_safe_subcommand(args)


def main() -> None:
    try:
        request = json.load(sys.stdin)
        command = request["tool_input"]["command"]
        cwd = request.get("cwd") or os.getcwd()
    except (ValueError, KeyError, TypeError):
        return
    if should_allow(command, cwd):
        decision = {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "safe git subcommand inside a working directory",
        }
        print(json.dumps({"hookSpecificOutput": decision}))


if __name__ == "__main__":
    main()
