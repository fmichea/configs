import json
import os
import subprocess
import time
from collections.abc import Callable
from pathlib import Path

import pytest

from conftest import GIT_DIR, PYTHON_DIR

HOOK = Path(__file__).resolve().parent.parent / "home" / "dot_claude" / "hooks" / "executable_repo-check.py"
DAY = 24 * 3600


@pytest.fixture
def state_dir(tmp_path) -> Path:
    return tmp_path / "repo-check"


@pytest.fixture
def hook_env(tmp_path, state_dir) -> dict:
    return {
        "HOME": str(tmp_path),
        "PATH": f"{PYTHON_DIR}:{GIT_DIR}:/usr/bin:/bin",
        "GIT_CONFIG_NOSYSTEM": "1",
        "CLAUDE_REPO_CHECK_DIR": str(state_dir),
    }


@pytest.fixture
def offer(hook_env) -> Callable[[Path], dict | None]:
    """offer(cwd) runs the SessionStart hook and returns its output, or None."""

    def offer(cwd: Path) -> dict | None:
        request = {"hook_event_name": "SessionStart", "source": "startup", "cwd": str(cwd)}
        result = subprocess.run(
            [HOOK, "offer"],
            input=json.dumps(request),
            capture_output=True,
            text=True,
            env=hook_env,
            check=True,
        )
        if not result.stdout:
            return None
        return json.loads(result.stdout)

    return offer


@pytest.fixture
def mark(hook_env) -> Callable[[Path], subprocess.CompletedProcess]:
    """mark(cwd) records the repository of cwd as checked."""

    def mark(cwd: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [HOOK, "mark"],
            cwd=cwd,
            capture_output=True,
            text=True,
            env=hook_env,
        )

    return mark


@pytest.fixture
def repo(tmp_path, hook_env) -> Path:
    repo = tmp_path / "repo"
    subprocess.run(
        ["git", "init", "--quiet", str(repo)],
        env=hook_env,
        check=True,
    )
    return repo.resolve()


@pytest.fixture
def worktree(tmp_path, repo, hook_env) -> Path:
    """A worktree of repo, on a new branch."""
    worktree = tmp_path / "worktree"
    subprocess.run(
        ["git", "commit", "--quiet", "--allow-empty", "--message", "initial"],
        cwd=repo,
        env={
            **hook_env,
            "GIT_AUTHOR_NAME": "Test",
            "GIT_AUTHOR_EMAIL": "test@example.com",
            "GIT_COMMITTER_NAME": "Test",
            "GIT_COMMITTER_EMAIL": "test@example.com",
        },
        check=True,
    )
    subprocess.run(
        ["git", "worktree", "add", "--quiet", "-b", "feature", str(worktree)],
        cwd=repo,
        env=hook_env,
        check=True,
    )
    return worktree


def age_marks(state_dir: Path, days: int) -> None:
    """Make every recorded check days old."""
    then = time.time() - days * DAY
    for state in state_dir.iterdir():
        os.utime(state, (then, then))


def test_offers_check_in_unchecked_repository(offer, repo):
    output = offer(repo)

    assert "/repo-check" in output["systemMessage"]
    assert "/repo-check" in output["hookSpecificOutput"]["additionalContext"]


def test_offers_nothing_outside_repository(offer, tmp_path):
    assert offer(tmp_path) is None


def test_offers_nothing_after_mark(offer, mark, repo):
    mark(repo)

    assert offer(repo) is None


def test_mark_from_subdirectory_covers_repository(offer, mark, repo):
    subdirectory = repo / "src"
    subdirectory.mkdir()

    mark(subdirectory)

    assert offer(repo) is None


def test_mark_from_worktree_covers_main_checkout(offer, mark, repo, worktree):
    mark(worktree)

    assert offer(repo) is None
    assert offer(worktree) is None


@pytest.mark.parametrize(
    ("days", "offered"),
    [
        (29, False),
        (31, True),
    ],
)
def test_offers_again_after_a_month(offer, mark, repo, state_dir, days, offered):
    mark(repo)
    age_marks(state_dir, days)

    assert (offer(repo) is not None) == offered


def test_mark_outside_repository_fails(mark, tmp_path):
    result = mark(tmp_path)

    assert result.returncode != 0
    assert "not inside a git repository" in result.stderr


def test_offer_ignores_invalid_input(hook_env):
    result = subprocess.run(
        [HOOK, "offer"],
        input="not json",
        capture_output=True,
        text=True,
        env=hook_env,
    )

    assert result.returncode == 0
    assert result.stdout == ""
