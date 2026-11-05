import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = (
    Path(__file__).resolve().parent.parent
    / "home"
    / "dot_claude"
    / "hooks"
    / "executable_git-c-allow.py"
)


@pytest.fixture
def home(tmp_path):
    home = tmp_path / "home"
    (home / ".claude").mkdir(parents=True)
    (home / "extra" / "repo").mkdir(parents=True)
    (home / "cwd" / "repo").mkdir(parents=True)
    (home / "outside").mkdir()
    settings = {"permissions": {"additionalDirectories": ["~/extra"]}}
    (home / ".claude" / "settings.json").write_text(json.dumps(settings))
    return home


def run_hook(home: Path, command: str) -> str:
    request = {
        "cwd": str(home / "cwd"),
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
    }
    result = subprocess.run(
        [sys.executable, HOOK],
        input=json.dumps(request),
        capture_output=True,
        text=True,
        env={"HOME": str(home)},
        check=True,
    )
    return result.stdout


def decision(home: Path, command: str) -> str | None:
    output = run_hook(home, command.replace("HOME", str(home)))
    if not output:
        return None
    return json.loads(output)["hookSpecificOutput"]["permissionDecision"]


@pytest.mark.parametrize(
    "command",
    [
        "git -C HOME/cwd/repo status --short --branch",
        "git -C HOME/extra/repo log --oneline -1",
        "git -C ~/extra/repo fetch --quiet origin",
        "git -C HOME/cwd/repo diff main",
        "git -C HOME/cwd/repo show HEAD",
        "git -C HOME/cwd/repo add docs/a.md docs/b.md",
        "git -C HOME/cwd/repo commit --message 'feat(x): add y'",
        "git -C HOME/cwd/repo commit --message 'fix: close #12'",
        "git -C HOME/cwd/repo worktree list",
        "git -C HOME/cwd/repo worktree add -b topic .claude/worktrees/topic origin/main",
        "git -C HOME/cwd/repo worktree remove .claude/worktrees/topic",
        "git -C HOME/cwd/repo pull --ff-only --quiet",
        "git -C HOME/cwd/repo branch --show-current",
        "git status",
        "git worktree add .claude/worktrees/topic -b topic main",
        "git worktree remove .claude/worktrees/topic",
        "git wt-add feat/topic",
        "git -C HOME/cwd/repo wt-add feat/topic origin/main",
        "git -C HOME/cwd/repo wt-cleanup feat/topic",
        "git pr-open --title 'feat: x' --body-file body.md",
    ],
)
def test_allows_safe_subcommand_inside_working_directory(home, command):
    assert decision(home, command) == "allow"


@pytest.mark.parametrize(
    "command",
    [
        "git -C HOME/outside status",
        "git -C HOME/outside wt-cleanup feat/topic",
        "git pr-open --title x --body-file body.md --allow-public",
        "git -C HOME/cwd/repo pr-open --allow-public --title x --body-file b.md",
        "git pr-merge feat/topic",
        "git -C HOME/cwd/../outside status",
        "git -C HOME/cwd/repo push",
        "git -C HOME/cwd/repo worktree remove --force x",
        "git -C HOME/cwd/repo worktree remove -f x",
        "git -C HOME/cwd/repo worktree remove x -ff",
        "git worktree remove --force x",
        "git worktree prune",
        "git push",
        "git -c core.pager=x log",
        "git -C HOME/cwd/repo pull",
        "git -C HOME/cwd/repo pull --rebase",
        "git -C HOME/cwd/repo branch --delete x",
        "git -C HOME/cwd/repo diff --output=/tmp/x",
        "git -C HOME/cwd/repo diff --no-index /dev/null HOME/outside/key",
        "git diff --no-index /dev/null HOME/outside/key",
        "git -C HOME/cwd/repo fetch --upload-pack=evil origin",
        "git -C HOME/cwd/repo status && rm -rf x",
        "git -C HOME/cwd/repo status; rm -rf x",
        "git -C HOME/cwd/repo log | sh",
        "git -C HOME/cwd/repo status foo#; rm -rf x",
        "git status foo#&& rm -rf x",
        "git status # ; rm -rf x",
        "git -C HOME/cwd/repo log > out.txt",
        "git -C HOME/cwd/repo commit --message \"$(rm -rf x)\"",
        "git -C HOME/cwd/repo commit --file - <<'EOF'\nmsg\nEOF",
        "git -C HOME/cwd/repo commit --message 'unterminated",
        "git",
        "git -C HOME/cwd/repo",
    ],
)
def test_defers_everything_else(home, command):
    assert decision(home, command) is None


def test_defers_on_invalid_input(home):
    result = subprocess.run(
        [sys.executable, HOOK],
        input="not json",
        capture_output=True,
        text=True,
        env={"HOME": str(home)},
    )

    assert result.returncode == 0
    assert result.stdout == ""
