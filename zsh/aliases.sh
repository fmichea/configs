##########
# Aliases

alias c='clear'
alias cdtemp='cd `mktemp -d`'
alias clfiles='find . \( -name "*~" -o -name "*.pyc" -o -name "*.o" \) -delete'
alias cp='cp -v'
alias dc='cd'
alias df='df -h'
alias du='du -h'
alias grep='grep --color=auto'
alias ipy2='ipython2'
alias ipy='ipython'
alias j='jobs'
alias la='ls -la'
alias ll='ls -l'
alias ls='ls --color=auto'
alias mv='mv -v'
alias ne='emacs -nw'
alias py2='python2'
alias py='python'
alias rm='rm -v'

alias kls='ls'
alias ks='ls'
alias l='ls'
alias s='ls'
alias sl='ls'

export EDITOR="vim"
export PAGER="most"

function mkcd {
    dir="$1"
    mkdir -p "$dir"
    cd "$dir"
}
