import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def merged_worktree(run, commit, clone, gh, push_to_main) -> Path:
    """A worktree with one commit, its PR merged, and main moved ahead."""
    path = Path(run("git-wt-add", clone, "feat/topic").stdout.strip())
    gh.set_pr(commit(path, "change"), state="MERGED")
    push_to_main("squashed-change")
    return path


def test_wt_add_creates_worktree_from_fetched_default_branch(run, git, clone, push_to_main):
    latest = push_to_main("after-clone")

    result = run("git-wt-add", clone, "feat/topic")

    path = clone / ".claude" / "worktrees" / "topic"
    assert result.returncode == 0, result.stderr
    assert Path(result.stdout.strip()).resolve() == path
    assert git(path, "branch", "--show-current") == "feat/topic"
    assert git(path, "rev-parse", "HEAD") == latest


def test_wt_add_leaves_branch_without_upstream(run, git, clone):
    run("git-wt-add", clone, "feat/topic")

    with pytest.raises(subprocess.CalledProcessError):
        git(clone, "rev-parse", "--abbrev-ref", "feat/topic@{upstream}")


def test_wt_add_from_a_worktree_creates_it_in_the_main_checkout(run, clone):
    first = Path(run("git-wt-add", clone, "feat/one").stdout.strip())

    result = run("git-wt-add", first, "fix/two")

    assert Path(result.stdout.strip()).resolve() == clone / ".claude" / "worktrees" / "two"


def test_wt_add_starts_from_given_start_point(run, git, clone, push_to_main):
    first = git(clone, "rev-parse", "HEAD")
    push_to_main("second")

    result = run("git-wt-add", clone, "feat/topic", first)

    assert git(Path(result.stdout.strip()), "rev-parse", "HEAD") == first


def test_wt_add_fails_when_branch_exists(run, git, clone):
    git(clone, "branch", "feat/topic")

    result = run("git-wt-add", clone, "feat/topic")

    assert result.returncode != 0
    assert result.stderr.startswith("git wt-add:")


@pytest.fixture
def include_rules(git, pusher) -> None:
    """Push a .gitignore and a .worktreeinclude to origin's main."""
    (pusher / ".gitignore").write_text("models/\n.env\n")
    (pusher / ".worktreeinclude").write_text("models/\nnotes.txt\n")
    git(pusher, "add", ".gitignore", ".worktreeinclude")
    git(pusher, "commit", "--quiet", "--message", "include rules")
    git(pusher, "push", "--quiet", "origin", "main")


@pytest.mark.parametrize(
    "name, copied",
    [
        ("models/model.bin", True),
        ("models/nested/weights.bin", True),
        (".env", False),
        ("notes.txt", False),
        ("draft.txt", False),
    ],
)
def test_wt_add_copies_ignored_files_listed_in_worktreeinclude(
    run,
    clone,
    include_rules,
    name,
    copied,
):
    source = clone / name
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(f"content of {name}")

    result = run("git-wt-add", clone, "feat/topic")

    assert result.returncode == 0, result.stderr
    destination = Path(result.stdout.strip()) / name
    assert destination.exists() == copied
    if copied:
        assert destination.read_text() == f"content of {name}"


def test_wt_add_without_worktreeinclude_copies_nothing(run, clone):
    (clone / "model.bin").write_text("weights")

    result = run("git-wt-add", clone, "feat/topic")

    assert result.returncode == 0, result.stderr
    assert not (Path(result.stdout.strip()) / "model.bin").exists()


def test_wt_cleanup_removes_merged_worktree_and_updates_main(
    run,
    git,
    clone,
    pusher,
    merged_worktree,
):
    result = run("git-wt-cleanup", clone, "feat/topic")

    assert result.returncode == 0, result.stderr
    assert not merged_worktree.exists()
    assert not git(clone, "branch", "--list", "feat/topic")
    assert git(clone, "rev-parse", "main") == git(pusher, "rev-parse", "main")


def test_wt_cleanup_works_from_inside_the_worktree(run, merged_worktree):
    result = run("git-wt-cleanup", merged_worktree, "feat/topic")

    assert result.returncode == 0, result.stderr
    assert not merged_worktree.exists()


def test_wt_cleanup_leaves_main_checkout_on_another_branch(run, git, clone, merged_worktree):
    git(clone, "switch", "--quiet", "--create", "other")

    result = run("git-wt-cleanup", clone, "feat/topic")

    assert result.returncode == 0, result.stderr
    assert git(clone, "branch", "--show-current") == "other"


def open_pr(path: Path, gh, commit) -> None:
    gh.set_pr_state("OPEN")


def unpushed_commit(path: Path, gh, commit) -> None:
    commit(path, "after-merge")


def untracked_file(path: Path, gh, commit) -> None:
    (path / "notes.txt").write_text("draft")


def modified_file(path: Path, gh, commit) -> None:
    (path / "change").write_text("edited")


@pytest.mark.parametrize(
    "make_unsafe",
    [open_pr, unpushed_commit, untracked_file, modified_file],
)
def test_wt_cleanup_refuses_and_keeps_everything(
    run,
    git,
    commit,
    clone,
    gh,
    merged_worktree,
    make_unsafe,
):
    make_unsafe(merged_worktree, gh, commit)

    result = run("git-wt-cleanup", clone, "feat/topic")

    assert result.returncode != 0
    assert result.stderr.startswith("git wt-cleanup:")
    assert merged_worktree.exists()
    assert git(clone, "branch", "--list", "feat/topic")


def test_wt_cleanup_refuses_branch_without_worktree(run, git, clone):
    git(clone, "branch", "feat/topic")

    result = run("git-wt-cleanup", clone, "feat/topic")

    assert result.returncode != 0
    assert git(clone, "branch", "--list", "feat/topic")
