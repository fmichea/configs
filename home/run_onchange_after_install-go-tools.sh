#!/bin/sh
# Install the Go tools the vim config uses, on machines with Go. chezmoi runs
# this again whenever its content changes: bump a version here to upgrade it.
set -eu

command -v go >/dev/null 2>&1 || exit 0

go install golang.org/x/tools/gopls@v0.24.0
