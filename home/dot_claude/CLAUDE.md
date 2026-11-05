# Personal preferences

## Writing

Applies to everything written for humans: replies, code comments, docs, commit messages, PR descriptions.

- Describe current behavior only. Do not narrate history ("previously", "now", "changed from", "moved here from X", "added for X"). Change history belongs in git.
- When touching code that has comments like that, rewrite them to describe current behavior.
- Commit messages and PR descriptions describe the change itself, not the debugging journey that led to it.
- Be concise. Lead with the answer and skip detail that does not change what the reader does next.

## Code

- Keep files small, keep functions small, create sub functions with explicit names.
- When arguments don't fit on one line, put each on its own line, with a trailing comma after the last (Black style).
- Never hand-edit generated files (e.g. `BUILD.bazel` from Gazelle, Job DSL `*.groovy`); change the source and rerun the generator.
- Keep vendored upstream files (CRDs, chart output) byte-identical. Remove content only if upstream offers a variant without it; carry necessary local changes as patches.

## Verification

- Do not guess about things that change often: package versions, config schemas, API and CLI flags. Check them against the source of truth (registry, official docs, `--help`, the installed tool).
- If something could not be verified, say what was assumed and ask me to confirm.

## Tests

- Write tests for new code.
- Test behavior: given this input, we get this output or effect. A test must not depend on how the code is written.
- Do not assert on internals, call order, private helpers, or mocks of code we own. A refactor that keeps behavior must not break tests.
- In Python, use `pytest.mark.parametrize` instead of loops over cases, so each case reports on its own.
- Run the relevant tests before reporting a task done. Report failures with their output.

## Security

- Never print secret values (passwords, keys, tokens) in command output, commit messages, PR or issue text. Check that a secret exists or list its keys; when a value is needed, decode it inside the command that consumes it.
- Don't quote credential-shaped strings even when they are public; describe them instead.
- If a secret leaks into any output (command output, this conversation, a file, a commit, PR or issue text), stop all other work. Tell me which secret leaked and where, and ask to rotate it. Rotating it is the top priority: resume other work only once it is rotated, or once I explicitly decide not to rotate it.

## Process

- When I have not specified exactly what a change entails, agree on the solution with me before implementing it. Describe the approach in plain words in chat, present options with a recommendation, and wait for my approval.

## Git

- Commit messages start with a conventional commit type: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`.
- New repositories use `main` as their initial branch.
- Stage explicit paths (`git add <paths>`); never `git add -A`, `git add .` or `git commit --all`. Check `git status` for unexpected files before committing.
- Commit and push only on a branch, never directly to the default branch.
- Before creating a PR or pushing new commits to one, stop so I can skim the changes locally. Push only once I say so. List each change to review as Markdown, not a code block: one field per line, ending each line but the last of a group with `\`, bold labels, the change description in italics, branch, worktree path and commit id in inline code. Separate changes with a `---` line between blank lines:

  ```markdown
  **Project:** repo-1\
  **Branch:** `feat/change-1`\
  **Worktree:** `.claude/worktrees/change-1`\
  **Commit:** `4c77f67`

  **Change:**\
  *Add the database catalog*

  ---

  **Project:** repo-2
  ...
  ```
- Open a PR with `git pr-open --title <title> --body-file <file>`, which pushes the current branch and opens the PR against the default branch. It runs without a prompt, so run it only after my go-ahead. It refuses on a public repository or one I don't own; rerun it with `--allow-public`, which asks for my approval.
- Base every PR on the default branch, never on another PR's branch. When order matters, write "merge after #N" in the description.
- Split PRs so each is useful if merged alone; put bulk data that needs review in its own PRs, separate from code.
- After opening a PR, wait for my review. Merge only when I say so, even if the merge method is already decided.
- Merge PRs with `git pr-merge <branch>`. It waits for the checks and refuses if one fails, squash-merges, deletes the branch and runs `git wt-cleanup` on its worktree. Pass `--merge` only when I ask to keep the commits. Report a refusal instead of working around it.

## Worktrees

- In repositories marked "Worktree: yes" in the project map, do every unit of work that modifies the repository in a git worktree on its own branch. Elsewhere, work on a branch in the main checkout, and move the work to a worktree when a second unit of work starts in the same repository.
- Create a worktree with `git wt-add <branch> [<start-point>]`. It fetches, branches from the remote's default branch unless given a start point, and creates `.claude/worktrees/<name>/` in the main checkout, where `<name>` is the last part of the branch name.
- When a unit of work spans several worktree repositories, create a worktree in each, with the same branch name.
- The first time a repository gets a worktree, record its setup steps (dependency installs, `.worktreeinclude` entries) in that repository's CLAUDE.md.
- Once the unit of work is merged, remove each worktree and its branch with `git wt-cleanup <branch>`, unless `git pr-merge` already did. It refuses unless the pull request is merged, the branch has no commits outside it and the worktree has nothing uncommitted; report a refusal instead of working around it. For a branch in the main checkout, switch back to the default branch and delete the branch.

## Projects

@~/.claude/projects.md

## Tooling

- Write shell commands for a human to review before approving: one purpose per command, long flags over short ones where they exist, no dense pipelines or loops packing several steps together. Split complex work into separate commands or a short script.
- When I am typing on a physical console without copy-paste, keep commands short and split into small steps.
- Batch queries to external APIs into one request rather than per-item loops, which hit rate limits.
- Use jq for JSON parsing.
- Use `rg` to search file contents and `fd` to find files, instead of `grep -r`, `ag` and `find`.
- Use the Edit tool rather than scripts to edit files, unless the file is large and a script avoids loading too much into context.
- Put the subcommand before any flags, e.g. `kubectl get pods --namespace monitoring`, not `kubectl --namespace monitoring get pods`. Permission rules match from the start of the command.
- Write temporary files to the scratchpad directory, not the system temp directory.
- Run independent steps as separate Bash calls instead of chaining them with `&&` or `;`. Each call is then checked against the permission rules on its own.
- Write commit messages with one `--message` per paragraph, the attribution trailer last, instead of a heredoc.

## Monitoring

- Query Prometheus with `gcx metrics query '<promql>'` and Loki with `gcx logs query '<logql>'`. Don't use `kubectl exec … promtool` or the API server proxy.
- To show a trend, run the range query with `--output graph --share-link`. Paste the chart into the reply in a code block with the key numbers written out, and link the Grafana Explore URL.
- Keep the pasted chart to three series or fewer, or aggregate, because colours are lost. With more series, give only the Grafana link.
