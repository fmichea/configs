#!/bin/sh
# Install the Python tools the configs use, on machines with uv: keygate for the
# git config, ruff for the Claude Code Python rules. chezmoi runs this again
# whenever its content changes: bump a version here to upgrade it.
set -eu

command -v uv >/dev/null 2>&1 || exit 0

uv tool install keygate==0.6.2
uv tool install ruff==0.17.4
