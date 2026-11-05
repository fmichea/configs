#!/bin/sh
# Install the Python tools the git config uses, on machines with uv. chezmoi runs
# this again whenever its content changes: bump a version here to upgrade it.
set -eu

command -v uv >/dev/null 2>&1 || exit 0

uv tool install keygate==0.6.2
