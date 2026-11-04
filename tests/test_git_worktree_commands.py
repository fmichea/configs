import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "home" / "dot_zsh" / "bin"
WT_ADD = BIN / "executable_git-wt-add"
WT_CLEANUP = BIN / "executable_git-wt-cleanup"
GIT_DIR = Path(shutil.which("git")).parent


@pytest.fixture
def env(tmp_path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    gh = fake_bin / "gh"
    gh.write_text('#!/bin/sh\ncat "$FAKE_GH_PR_VIEW"\n')
    gh.chmod(0o755)
    home = tmp_path / "home"
    home.mkdir()
    return {
        "HOME": str(home),
        "PATH": f"{fake_bin}:{GIT_DIR}:/usr/bin:/bin",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
        "FAKE_GH_PR_VIEW": str(tmp_path / "pr.json"),
    }


def git(env: dict, cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def commit(env: dict, repo: Path, name: str) -> str:
    (repo / name).write_text(name)
    git(env, repo, "add", name)
    git(env, repo, "commit", "--quiet", "--message", name)
    return git(env, repo, "rev-parse", "HEAD")


def run_script(env: dict, cwd: Path, script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, script, *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )


def branch_exists(env: dict, repo: Path, branch: str) -> bool:
    return bool(git(env, repo, "branch", "--list", branch))


@pytest.fixture
def upstream(env, tmp_path):
    """A remote with one commit on main, and a second clone to push to it."""
    origin = tmp_path / "origin.git"
    git(env, tmp_path, "init", "--quiet", "--bare", "--initial-branch=main", str(origin))
    pusher = tmp_path / "pusher"
    git(env, tmp_path, "clone", "--quiet", str(origin), str(pusher))
    git(env, pusher, "switch", "--quiet", "--create", "main")
    commit(env, pusher, "initial")
    git(env, pusher, "push", "--quiet", "origin", "main")
    return origin, pusher


@pytest.fixture
def clone(env, tmp_path, upstream):
    origin, _ = upstream
    clone = tmp_path / "clone"
    git(env, tmp_path, "clone", "--quiet", str(origin), str(clone))
    return clone.resolve()


def push_to_main(env: dict, upstream, name: str) -> str:
    _, pusher = upstream
    head = commit(env, pusher, name)
    git(env, pusher, "push", "--quiet", "origin", "main")
    return head


def test_wt_add_creates_worktree_from_fetched_default_branch(env, clone, upstream):
    latest = push_to_main(env, upstream, "after-clone")

    result = run_script(env, clone, WT_ADD, "feat/topic")

    path = clone / ".claude" / "worktrees" / "topic"
    assert result.returncode == 0, result.stderr
    assert Path(result.stdout.strip()).resolve() == path
    assert git(env, path, "branch", "--show-current") == "feat/topic"
    assert git(env, path, "rev-parse", "HEAD") == latest


def test_wt_add_leaves_branch_without_upstream(env, clone):
    run_script(env, clone, WT_ADD, "feat/topic")

    upstream = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "feat/topic@{upstream}"],
        cwd=clone,
        env=env,
        capture_output=True,
    )
    assert upstream.returncode != 0


def test_wt_add_from_a_worktree_creates_it_in_the_main_checkout(env, clone):
    first = Path(run_script(env, clone, WT_ADD, "feat/one").stdout.strip())

    result = run_script(env, first, WT_ADD, "fix/two")

    assert Path(result.stdout.strip()).resolve() == clone / ".claude" / "worktrees" / "two"


def test_wt_add_starts_from_given_start_point(env, clone, upstream):
    first = git(env, clone, "rev-parse", "HEAD")
    push_to_main(env, upstream, "second")

    result = run_script(env, clone, WT_ADD, "feat/topic", first)

    assert git(env, Path(result.stdout.strip()), "rev-parse", "HEAD") == first


def test_wt_add_fails_when_branch_exists(env, clone):
    git(env, clone, "branch", "feat/topic")

    result = run_script(env, clone, WT_ADD, "feat/topic")

    assert result.returncode != 0
    assert result.stderr.startswith("git wt-add:")


def merged_worktree(env: dict, clone: Path, upstream, pr_state: str = "MERGED") -> Path:
    """A worktree with one commit, its PR in pr_state, and main moved ahead."""
    path = Path(run_script(env, clone, WT_ADD, "feat/topic").stdout.strip())
    head = commit(env, path, "change")
    Path(env["FAKE_GH_PR_VIEW"]).write_text(json.dumps({"state": pr_state, "headRefOid": head}))
    push_to_main(env, upstream, "squashed-change")
    return path


def test_wt_cleanup_removes_merged_worktree_and_updates_main(env, clone, upstream):
    path = merged_worktree(env, clone, upstream)

    result = run_script(env, clone, WT_CLEANUP, "feat/topic")

    assert result.returncode == 0, result.stderr
    assert not path.exists()
    assert not branch_exists(env, clone, "feat/topic")
    assert git(env, clone, "rev-parse", "main") == git(env, upstream[1], "rev-parse", "main")


def test_wt_cleanup_works_from_inside_the_worktree(env, clone, upstream):
    path = merged_worktree(env, clone, upstream)

    result = run_script(env, path, WT_CLEANUP, "feat/topic")

    assert result.returncode == 0, result.stderr
    assert not path.exists()


def test_wt_cleanup_leaves_main_checkout_on_another_branch(env, clone, upstream):
    merged_worktree(env, clone, upstream)
    git(env, clone, "switch", "--quiet", "--create", "other")

    result = run_script(env, clone, WT_CLEANUP, "feat/topic")

    assert result.returncode == 0, result.stderr
    assert git(env, clone, "branch", "--show-current") == "other"


def open_pr(env: dict, path: Path) -> None:
    pr = json.loads(Path(env["FAKE_GH_PR_VIEW"]).read_text())
    Path(env["FAKE_GH_PR_VIEW"]).write_text(json.dumps({**pr, "state": "OPEN"}))


def unpushed_commit(env: dict, path: Path) -> None:
    commit(env, path, "after-merge")


def untracked_file(env: dict, path: Path) -> None:
    (path / "notes.txt").write_text("draft")


def modified_file(env: dict, path: Path) -> None:
    (path / "change").write_text("edited")


@pytest.mark.parametrize(
    "make_unsafe",
    [open_pr, unpushed_commit, untracked_file, modified_file],
)
def test_wt_cleanup_refuses_and_keeps_everything(env, clone, upstream, make_unsafe):
    path = merged_worktree(env, clone, upstream)
    make_unsafe(env, path)

    result = run_script(env, clone, WT_CLEANUP, "feat/topic")

    assert result.returncode != 0
    assert result.stderr.startswith("git wt-cleanup:")
    assert path.exists()
    assert branch_exists(env, clone, "feat/topic")


def test_wt_cleanup_refuses_branch_without_worktree(env, clone):
    git(env, clone, "branch", "feat/topic")

    result = run_script(env, clone, WT_CLEANUP, "feat/topic")

    assert result.returncode != 0
    assert branch_exists(env, clone, "feat/topic")
