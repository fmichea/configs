# configs

Configuration files of [Franck Michea](mailto:franck@michea.dev), managed with [chezmoi](https://www.chezmoi.io/).
They were written reading files from a lot of people, the list would now be too long and incomplete, thanks to all of them.

## Install

```sh
chezmoi init --source ~/configs --apply https://github.com/fmichea/configs.git
```

chezmoi clones the repository into `~/configs` and installs it. On a machine with GitHub SSH access, use `--ssh fmichea/configs` as the last argument instead, so the clone can push.

chezmoi asks whether the machine is a development machine; answer yes to also install [configs-private](#what-goes-where). Unattended installs add `--promptDefaults`, which answers no.

## Dependencies

The configuration uses these tools.

- [chezmoi](https://www.chezmoi.io/)
- [zsh](https://www.zsh.org/)
- [git](https://git-scm.com/) and [Git LFS](https://git-lfs.com/)
- [delta](https://github.com/dandavison/delta)
- [vim](https://www.vim.org/)
- [tmux](https://github.com/tmux/tmux)
- [fzf](https://github.com/junegunn/fzf)
- [fd](https://github.com/sharkdp/fd)
- [ripgrep](https://github.com/BurntSushi/ripgrep)
- [direnv](https://direnv.net/)
- [nvm](https://github.com/nvm-sh/nvm)
- [chruby](https://github.com/postmodern/chruby)
- [Go](https://go.dev/): `chezmoi apply` installs [gopls](https://github.com/golang/tools/tree/master/gopls) with it, for vim-go.
- Linux: [i3](https://i3wm.org/) and [i3status](https://i3wm.org/i3status/)
- macOS: [Karabiner-Elements](https://karabiner-elements.pqrs.org/)

## Layout

- `home/` is the chezmoi source state (see `.chezmoiroot`): `dot_zshrc` installs as `~/.zshrc`, `dot_config/i3` as `~/.config/i3`, and so on.
- `home/.chezmoiexternal.toml` lists the vim and zsh plugins, pinned to a commit.
- `home/.chezmoiignore` skips Linux-only and macOS-only files on the other platform.
- `karabiner/` is linked as a whole directory to `~/.config/karabiner`, because Karabiner-Elements stops detecting changes when only `karabiner.json` is a symlink.

## Editing

chezmoi runs in symlink mode: most files in `~` are symlinks into `home/`, so editing `~/.gitconfig` edits the tracked file. Commit the change from `~/configs`.

Executable files (`~/.zsh/bin/*`, `~/.claude/hooks/*`, `~/.claude/bin/*`, i3 startup script) are copies instead. Edit them in `home/` and run `chezmoi apply`.

## Git worktrees

`git wt-add <branch>` creates a worktree in `.claude/worktrees/` of the main checkout, on a new branch from the remote's default branch. `git wt-cleanup <branch>` removes the worktree and the branch once its pull request is merged, and refuses otherwise. Both are scripts in `~/.zsh/bin`, and `~/.claude/hooks/git-c-allow.py` lets Claude Code run them without a prompt.

## Pull requests

`git pr-open --title <title> --body-file <file>` pushes the current branch and opens a pull request against the default branch. Claude Code runs it without a prompt on private repositories owned by `OWNER` (set at the top of the script); anywhere else it refuses unless given `--allow-public`, which always prompts.

`git pr-merge [<branch>]` waits for the pull request's checks, refuses if one fails, then squash-merges (`--merge` for a merge commit), deletes the branch and removes its worktree with `git wt-cleanup`. A pull request with no checks reported merges right away. It always prompts.

## Claude Code permissions

`~/.claude/hooks/permission-log.sh` logs every permission prompt to `~/.claude/permission-log.jsonl`. `~/.claude/bin/permission-report.py --since-days N` groups them by suggested rule, to find candidates for `permissions.allow` in `home/dot_claude/settings.json`.

Claude Code checks each part of a pipeline against the rules on its own, so a rule such as `Bash(curl * | sh)` never matches. The deny rules on bare `sh`, `bash` and `zsh` and their `-` and `-s` forms block piping anything into a shell; `curl` and `wget` always ask.

Open decision: how to allow WebFetch of documentation. Wildcards such as `docs.*.*` or `*.github.io` match domains anyone can register or publish on, so a prompt injection could exfiltrate data through the URL path without a prompt; filtering on URL shape (no query string) does not prevent that. The alternative is allowing exact domains as they come up in the report. Until decided, only `cloudnative-pg.io` is allowed.

## What goes where

- **configs (this repository, public):** anything a fresh server or a stranger could use: shell, editor, git and terminal config, Claude Code preferences, installer logic.
- **configs-private:** anything describing my own setup that only development machines need: the project map, SSH hosts, private repository names.
- **Neither:** secrets (keys, tokens). Those live in Vault or the macOS Keychain.
