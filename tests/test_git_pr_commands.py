import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest


@pytest.fixture
def body(tmp_path) -> Path:
    body = tmp_path / "body.md"
    body.write_text("Adds a topic.")
    return body


@pytest.fixture
def topic_branch(git, commit, clone) -> str:
    """Commit id of feat/topic, checked out in the main checkout."""
    git(clone, "switch", "--quiet", "--create", "feat/topic")
    return commit(clone, "topic")


@pytest.fixture
def topic_worktree(run, commit, clone, gh) -> Path:
    """A worktree on feat/topic with one commit and an open PR with checks."""
    path = Path(run("git-wt-add", clone, "feat/topic").stdout.strip())
    gh.set_pr(commit(path, "topic"))
    return path


@pytest.fixture
def pr_open(run, clone, body) -> Callable[..., subprocess.CompletedProcess]:
    """pr_open(*extra, body_file=body) runs git pr-open in the main checkout."""

    def pr_open(*extra: str, body_file: Path = body) -> subprocess.CompletedProcess:
        return run(
            "git-pr-open",
            clone,
            "--title",
            "feat: add topic",
            "--body-file",
            str(body_file),
            *extra,
        )

    return pr_open


@pytest.fixture
def pr_merge(run, clone) -> Callable[..., subprocess.CompletedProcess]:
    """pr_merge(*args, cwd=clone) runs git pr-merge."""

    def pr_merge(*args: str, cwd: Path = clone) -> subprocess.CompletedProcess:
        return run("git-pr-merge", cwd, *args)

    return pr_merge


def test_pr_open_pushes_branch_and_opens_pr(pr_open, git, clone, origin, gh, body, topic_branch):
    result = pr_open()

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == gh.pr_url
    assert git(origin, "rev-parse", "feat/topic") == topic_branch
    assert git(clone, "rev-parse", "--abbrev-ref", "feat/topic@{upstream}") == "origin/feat/topic"
    [create] = gh.calls("pr", "create")
    assert create["args"] == [
        "pr",
        "create",
        "--base",
        "main",
        "--head",
        "feat/topic",
        "--title",
        "feat: add topic",
        "--body-file",
        str(body),
    ]


def public_repo(clone: Path, gh, git) -> None:
    gh.set_repo(private=False)


def repo_of_another_owner(clone: Path, gh, git) -> None:
    gh.set_repo(owner="someone-else")


def on_default_branch(clone: Path, gh, git) -> None:
    git(clone, "switch", "--quiet", "main")


def untracked_file(clone: Path, gh, git) -> None:
    (clone / "notes.txt").write_text("draft")


def modified_file(clone: Path, gh, git) -> None:
    (clone / "topic").write_text("edited")


@pytest.mark.parametrize(
    "make_unsafe",
    [public_repo, repo_of_another_owner, on_default_branch, untracked_file, modified_file],
)
def test_pr_open_refuses_without_pushing(
    pr_open,
    git,
    clone,
    origin,
    gh,
    topic_branch,
    make_unsafe,
):
    make_unsafe(clone, gh, git)

    result = pr_open()

    assert result.returncode != 0
    assert result.stderr.startswith("git pr-open:")
    assert not git(origin, "branch", "--list", "feat/topic")
    assert not gh.calls("pr", "create")


def test_pr_open_refusal_on_public_repo_names_the_flag(pr_open, gh, topic_branch):
    gh.set_repo(private=False)

    result = pr_open()

    assert "--allow-public" in result.stderr


@pytest.mark.parametrize("make_public", [public_repo, repo_of_another_owner])
def test_pr_open_allow_public_opens_pr(pr_open, git, clone, gh, topic_branch, make_public):
    make_public(clone, gh, git)

    result = pr_open("--allow-public")

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == gh.pr_url


def test_pr_open_refuses_missing_body_file(pr_open, git, origin, tmp_path, topic_branch):
    result = pr_open(body_file=tmp_path / "missing.md")

    assert result.returncode != 0
    assert not git(origin, "branch", "--list", "feat/topic")


def test_pr_merge_squashes_at_checked_head_and_removes_worktree(
    pr_merge,
    git,
    clone,
    gh,
    topic_worktree,
):
    head = git(topic_worktree, "rev-parse", "HEAD")

    result = pr_merge("feat/topic")

    assert result.returncode == 0, result.stderr
    [merge] = gh.calls("pr", "merge")
    assert merge["args"] == [
        "pr",
        "merge",
        "7",
        "--squash",
        "--delete-branch",
        "--match-head-commit",
        head,
    ]
    assert Path(merge["cwd"]).resolve() == topic_worktree.resolve()
    assert not topic_worktree.exists()
    assert not git(clone, "branch", "--list", "feat/topic")


def test_pr_merge_defaults_to_current_branch(pr_merge, gh, topic_worktree):
    result = pr_merge(cwd=topic_worktree)

    assert result.returncode == 0, result.stderr
    assert gh.calls("pr", "view", "feat/topic")
    assert not topic_worktree.exists()


def test_pr_merge_with_merge_flag_creates_merge_commit(pr_merge, gh, topic_worktree):
    pr_merge("feat/topic", "--merge")

    [merge] = gh.calls("pr", "merge")
    assert "--merge" in merge["args"]
    assert "--squash" not in merge["args"]


def test_pr_merge_without_checks_merges_with_note(pr_merge, git, gh, topic_worktree):
    gh.set_pr(git(topic_worktree, "rev-parse", "HEAD"), checks=False)

    result = pr_merge("feat/topic")

    assert result.returncode == 0, result.stderr
    assert "no checks reported" in result.stdout
    assert gh.calls("pr", "merge")


def test_pr_merge_refuses_when_checks_fail(pr_merge, gh, topic_worktree):
    gh.fail_checks()

    result = pr_merge("feat/topic")

    assert result.returncode != 0
    assert "ci/jenkins/tests" in result.stderr
    assert not gh.calls("pr", "merge")
    assert topic_worktree.exists()


def test_pr_merge_refuses_pr_that_is_not_open(pr_merge, gh, topic_worktree):
    gh.set_pr_state("CLOSED")

    result = pr_merge("feat/topic")

    assert result.returncode != 0
    assert not gh.calls("pr", "merge")


def test_pr_merge_reports_kept_worktree_after_merge(pr_merge, topic_worktree):
    (topic_worktree / "notes.txt").write_text("draft")

    result = pr_merge("feat/topic")

    assert result.returncode != 0
    assert "merged, but the worktree was kept" in result.stderr
    assert topic_worktree.exists()


def test_pr_merge_of_main_checkout_branch_runs_gh_there(pr_merge, clone, gh, topic_branch):
    gh.set_pr(topic_branch)

    result = pr_merge()

    assert result.returncode == 0, result.stderr
    [merge] = gh.calls("pr", "merge")
    assert Path(merge["cwd"]).resolve() == clone
