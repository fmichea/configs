#####################################################################
# NVM configuration: the default node version's bin directory goes on PATH at
# startup, so node also works in child processes, and nvm itself loads on its
# first call. A default alias other than `node` or a version (e.g. `lts/*`)
# loads nvm at startup instead.

export NVM_DIR="$HOME/.nvm"

nvm_scripts=(
    "$NVM_DIR/nvm.sh"
    /opt/homebrew/opt/nvm/nvm.sh
    /usr/local/opt/nvm/nvm.sh
)
nvm_completions=(
    "$NVM_DIR/bash_completion"
    /opt/homebrew/opt/nvm/etc/bash_completion.d/nvm
    /usr/local/opt/nvm/etc/bash_completion.d/nvm
)

# Source nvm.sh with args (e.g. --no-use), then its completion.
nvm_load() {
    local -a scripts=(${^nvm_scripts}(N))
    local -a completions=(${^nvm_completions}(N))
    (( ${#scripts} )) || return 1
    source "${scripts[1]}" "$@"
    (( ${#completions} )) && source "${completions[1]}"
    return 0
}

# Print the newest installed version matching the default alias, which is
# `node` (any version), a version prefix (`22`, `v22.1`) or an exact version.
nvm_default_version_dir() {
    local alias_file="$NVM_DIR/alias/default"
    local versions="$NVM_DIR/versions/node"
    [ -f "$alias_file" ] || return 1
    local default=$(<"$alias_file")
    local -a candidates
    case "$default" in
        node)
            candidates=("$versions"/v*(N/n))
            ;;
        v[0-9]*|[0-9]*)
            local version="v${default#v}"
            candidates=("$versions/$version"(N/) "$versions/$version".*(N/n))
            ;;
    esac
    (( ${#candidates} )) || return 1
    print -r -- "${candidates[-1]}"
}

# Stands in for nvm until its first call; sourcing nvm.sh replaces it.
nvm() {
    nvm_load --no-use || { print -u2 "nvm: nvm.sh not found"; return 1 }
    nvm "$@"
}

if nvm_default_dir=$(nvm_default_version_dir); then
    export PATH="$nvm_default_dir/bin:$PATH"
else
    nvm_load
fi
unset nvm_default_dir
