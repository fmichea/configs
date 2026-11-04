import json
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent / "home" / "dot_zsh" / "bin"
FAKE_BIN = TESTS / "bin"
PYTHON_DIR = Path(sys.executable).parent
GIT_DIR = Path(shutil.which("git")).parent


class FakeGh:
    """Sets up and inspects the state of the fake gh in tests/bin/gh."""

    pr_url = "https://github.com/fmichea/repo-1/pull/7"

    def __init__(self, state: Path):
        self.state = state
        (state / "calls.jsonl").touch()
        (state / "checks-exit").write_text("0")
        self.set_repo()

    def set_repo(self, private: bool = True, owner: str = "fmichea") -> None:
        repo = {"isPrivate": private, "owner": {"login": owner}}
        (self.state / "repo.json").write_text(json.dumps(repo))

    def set_pr(self, head: str, state: str = "OPEN", checks: bool = True) -> None:
        rollup = [{"context": "ci/jenkins/tests", "state": "PENDING"}] if checks else []
        pr = {
            "number": 7,
            "state": state,
            "headRefOid": head,
            "statusCheckRollup": rollup,
        }
        (self.state / "pr.json").write_text(json.dumps(pr))

    def set_pr_state(self, state: str) -> None:
        pr = json.loads((self.state / "pr.json").read_text())
        (self.state / "pr.json").write_text(json.dumps({**pr, "state": state}))

    def fail_checks(self) -> None:
        (self.state / "checks-exit").write_text("1")

    def calls(self, *subcommand: str) -> list[dict]:
        """Calls whose arguments start with subcommand, with their directory."""
        lines = (self.state / "calls.jsonl").read_text().splitlines()
        calls = [json.loads(line) for line in lines]
        return [call for call in calls if call["args"][: len(subcommand)] == list(subcommand)]


@pytest.fixture
def gh(tmp_path) -> FakeGh:
    state = tmp_path / "gh-state"
    state.mkdir()
    return FakeGh(state)


@pytest.fixture
def env(tmp_path, gh) -> dict:
    # Scripts run `git wt-cleanup`, which git finds as git-wt-cleanup on PATH.
    git_commands = tmp_path / "git-commands"
    git_commands.mkdir()
    (git_commands / "git-wt-cleanup").symlink_to(SCRIPTS / "executable_git-wt-cleanup")
    home = tmp_path / "home"
    home.mkdir()
    return {
        "HOME": str(home),
        "PATH": f"{FAKE_BIN}:{git_commands}:{PYTHON_DIR}:{GIT_DIR}:/usr/bin:/bin",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
        "FAKE_GH_STATE": str(gh.state),
        "FAKE_GH_PR_URL": gh.pr_url,
    }


@pytest.fixture
def git(env) -> Callable[..., str]:
    """git(cwd, *args) runs git and returns its stripped stdout."""

    def git(cwd: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    return git


@pytest.fixture
def commit(git) -> Callable[[Path, str], str]:
    """commit(repo, name) commits a new file and returns the commit id."""

    def commit(repo: Path, name: str) -> str:
        (repo / name).write_text(name)
        git(repo, "add", name)
        git(repo, "commit", "--quiet", "--message", name)
        return git(repo, "rev-parse", "HEAD")

    return commit


@pytest.fixture
def run(env) -> Callable[..., subprocess.CompletedProcess]:
    """run(script, cwd, *args) runs a script of home/dot_zsh/bin, e.g. git-wt-add."""

    def run(script: str, cwd: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [SCRIPTS / f"executable_{script}", *args],
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
        )

    return run


@pytest.fixture
def origin(tmp_path, git) -> Path:
    """An empty bare remote."""
    origin = tmp_path / "origin.git"
    git(tmp_path, "init", "--quiet", "--bare", "--initial-branch=main", str(origin))
    return origin


@pytest.fixture
def pusher(tmp_path, git, commit, origin) -> Path:
    """A clone that pushed the first commit of main to origin."""
    pusher = tmp_path / "pusher"
    git(tmp_path, "clone", "--quiet", str(origin), str(pusher))
    git(pusher, "switch", "--quiet", "--create", "main")
    commit(pusher, "initial")
    git(pusher, "push", "--quiet", "origin", "main")
    return pusher


@pytest.fixture
def clone(tmp_path, git, origin, pusher) -> Path:
    """The clone the scripts under test run in."""
    clone = tmp_path / "clone"
    git(tmp_path, "clone", "--quiet", str(origin), str(clone))
    return clone.resolve()


@pytest.fixture
def push_to_main(git, commit, pusher) -> Callable[[str], str]:
    """push_to_main(name) pushes a new commit to origin's main and returns its id."""

    def push_to_main(name: str) -> str:
        head = commit(pusher, name)
        git(pusher, "push", "--quiet", "origin", "main")
        return head

    return push_to_main
