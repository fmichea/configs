##########
# Aliases

alias c='clear'
alias grep='grep --color=auto'

alias df='df -h'
alias du='du -h'

alias cp='cp -v'
alias mv='mv -v'
alias rm='rm -v'

alias dc='cd'

alias v='vim'
alias vo,='vim'

alias kls='ls'
alias ks='ls'
alias l='ls'
alias s='ls'
alias sl='ls'

alias cdtemp='cd $(tempdir)'

export EDITOR="vim"

if [ "$HOST_OS" = "Linux" ]; then
    alias ls='ls --color=auto'
    alias objdump='objdump -M intel'

    which most &> /dev/null && export PAGER="most"
elif [ "$HOST_OS" = "Darwin" ]; then
    alias ls='ls -G'
fi
