# configs

Configuration files of [Franck Michea](mailto:franck.michea@gmail.com), managed with [chezmoi](https://www.chezmoi.io/).
They were written reading files from a lot of people, the list would now be too long and incomplete, thanks to all of them.

## Install

```sh
git clone https://github.com/fmichea/configs.git ~/configs
chezmoi init --source ~/configs --apply
```

chezmoi asks whether the machine is a development machine; answer yes to also install [configs-private](#what-goes-where). Unattended installs (fppm) add `--promptDefaults`, which answers no.

## Layout

- `home/` is the chezmoi source state (see `.chezmoiroot`): `dot_zshrc` installs as `~/.zshrc`, `dot_config/i3` as `~/.config/i3`, and so on.
- `home/.chezmoiexternal.toml` lists the vim and zsh plugins, pinned to a commit.
- `home/.chezmoiignore` skips Linux-only and macOS-only files on the other platform.
- `karabiner/` is linked as a whole directory to `~/.config/karabiner`, because Karabiner-Elements stops detecting changes when only `karabiner.json` is a symlink.

## Editing

chezmoi runs in symlink mode: most files in `~` are symlinks into `home/`, so editing `~/.gitconfig` edits the tracked file. Commit the change from `~/configs`.

Executable files (`~/.zsh/bin/*`, `~/.claude/hooks/*`, virtualenvwrapper hooks, i3 startup script) are copies instead. Edit them in `home/` and run `chezmoi apply`.

## What goes where

- **configs (this repository, public):** anything a fresh server or a stranger could use: shell, editor, git and terminal config, Claude Code preferences, installer logic.
- **configs-private:** anything describing my own setup that only development machines need: the project map, SSH hosts, private repository names.
- **Neither:** secrets (keys, tokens). Those live in Vault or the macOS Keychain.
