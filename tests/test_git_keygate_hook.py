import json
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

from conftest import FAKE_BIN, GIT_DIR, PYTHON_DIR

GITCONFIG = Path(__file__).resolve().parent.parent / "home" / "dot_gitconfig"

LOCAL_HOOK = """\
#!/bin/sh
echo ran >> "$LOCAL_HOOK_CALLS"
"""


class Repo:
    """A repository committed to with the real gitconfig, and a fake keygate."""

    def __init__(self, path: Path, state: Path):
        self.path = path
        self.state = state
        self.keygate_calls = state / "keygate-calls.jsonl"
        self.local_hook_calls = state / "local-hook-calls"
        self.keygate_calls.touch()
        self.local_hook_calls.touch()

    def env(self, keygate_exit: int | None) -> dict:
        """Environment with a fake keygate exiting with keygate_exit; None: no keygate."""
        path = f"{GIT_DIR}:/usr/bin:/bin"
        if keygate_exit is not None:
            path = f"{FAKE_BIN}:{PYTHON_DIR}:{path}"
        return {
            "HOME": str(self.state),
            "PATH": path,
            "GIT_CONFIG_GLOBAL": str(GITCONFIG),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_AUTHOR_NAME": "Test",
            "GIT_AUTHOR_EMAIL": "test@example.com",
            "GIT_COMMITTER_NAME": "Test",
            "GIT_COMMITTER_EMAIL": "test@example.com",
            "FAKE_KEYGATE_CALLS": str(self.keygate_calls),
            "FAKE_KEYGATE_EXIT": str(keygate_exit or 0),
            "LOCAL_HOOK_CALLS": str(self.local_hook_calls),
        }

    def git(self, *args: str, keygate_exit: int | None = 0) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args],
            cwd=self.path,
            env=self.env(keygate_exit),
            capture_output=True,
            text=True,
        )

    def add_local_hook(self) -> None:
        hook = self.path / ".git" / "hooks" / "pre-commit"
        hook.write_text(LOCAL_HOOK)
        hook.chmod(0o755)

    def commit_file(self, keygate_exit: int | None = 0) -> subprocess.CompletedProcess:
        (self.path / "file").write_text("content")
        self.git("add", "file")
        return self.git("commit", "--quiet", "--message", "file", keygate_exit=keygate_exit)

    def commits(self) -> int:
        result = self.git("rev-list", "--count", "--all")
        return int(result.stdout.strip() or 0)

    def keygate_runs(self) -> list[list[str]]:
        return [json.loads(line) for line in self.keygate_calls.read_text().splitlines()]

    def local_hook_runs(self) -> int:
        return len(self.local_hook_calls.read_text().splitlines())


@pytest.fixture
def repo(tmp_path) -> Repo:
    state = tmp_path / "state"
    state.mkdir()
    repo = Repo(tmp_path / "repo", state)
    repo.path.mkdir()
    repo.git("init", "--quiet")
    return repo


def test_passing_scan_commits(repo):
    result = repo.commit_file(keygate_exit=0)

    assert result.returncode == 0
    assert repo.keygate_runs() == [["scan"]]
    assert repo.commits() == 1


def test_failing_scan_blocks_commit(repo):
    result = repo.commit_file(keygate_exit=1)

    assert result.returncode != 0
    assert repo.commits() == 0


def test_missing_keygate_warns_and_commits(repo):
    result = repo.commit_file(keygate_exit=None)

    assert result.returncode == 0
    assert "keygate not installed" in result.stderr
    assert repo.commits() == 1


def test_repository_hook_still_runs(repo):
    repo.add_local_hook()

    repo.commit_file(keygate_exit=0)

    assert repo.keygate_runs() == [["scan"]]
    assert repo.local_hook_runs() == 1


def test_repository_can_opt_out(repo):
    repo.git("config", "set", "hook.keygate.enabled", "false")

    result = repo.commit_file(keygate_exit=1)

    assert result.returncode == 0
    assert repo.keygate_runs() == []
