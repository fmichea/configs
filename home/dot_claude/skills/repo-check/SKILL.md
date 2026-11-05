---
name: repo-check
description: Audit the current repository against the user's standards (CLAUDE.md, project map, default branch, tests, secrets, README) and propose fixes. Use when the user runs /repo-check or accepts the offer to run it.
---

# Repository check

Audit the repository of the current directory against the user's standards. Change nothing during the audit.

## Checks

Run each check, read-only. Look at files and run the commands the repository documents; do not guess.

1. **CLAUDE.md:** the repository has one, and it gives the commands to build and test. In a repository marked "Worktree: yes" in the project map, it also records the worktree setup steps: dependency installs and `.worktreeinclude` entries.
2. **Project map:** `~/.claude/projects.md` lists the repository, and its row matches what the repository contains.
3. **Default branch:** the default branch is `main` (`git symbolic-ref refs/remotes/origin/HEAD`, or `gh repo view --json defaultBranchRef`).
4. **Tests:** the repository has tests, the documented command runs them, and they pass.
5. **Secrets:** `.gitignore` covers `.env`-style files and other local secrets the project uses, and `git config get hook.keygate.enabled` is not `false`.
6. **README:** it exists and says what the repository is and how to run it.

## Report

List each check with its result: pass, gap, or not applicable, and one line of evidence. For each gap, propose a fix in plain words, with a recommendation when there are options.

Wait for the user to choose which fixes to make. Make the chosen fixes on a branch, following the git and worktree rules of the global CLAUDE.md.

## Record the check

Once the report is given, run `~/.claude/hooks/repo-check.py mark`, so the offer to run this check waits another 30 days.
