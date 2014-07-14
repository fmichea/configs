##########
# Aliases

alias c='clear'
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
alias mv='mv -v'
alias ne='emacs -nw'
alias objdump='objdump -M intel'
alias py2='python2'
alias py3='python3'
alias py='python'
alias rm='rm -v'
alias v='vim'
alias vo,='vim'

alias kls='ls'
alias ks='ls'
alias l='ls'
alias s='ls'
alias sl='ls'

alias sshtmp='ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
alias scptmp='scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'

export EDITOR="vim"

if [ "$HOST_OS" = "Linux" ]; then
    alias cdtemp='cd `mktemp -d`'
    alias ls='ls --color=auto'

    which most &> /dev/null && export PAGER="most"

    function nn { # No Network access to a command.
        cmd="$@"
        sg no-network $cmd
    }

    function clipcp {
        if [ $# -eq 3 ]; then
            CONTENT=`cat $1 | head -n $(( $2 + $3 )) | tail -n $(( $3 + 1))`
        else
            CONTENT=`cat -`
        fi
        echo "$CONTENT" | xclip
        xclip -o
    }
elif [ "$HOST_OS" = "Darwin" ]; then
    alias cdtemp='cd `mktemp -d /tmp/tmp.XXXXXXXX`'
    alias ls='ls -G'
fi

function mkcd {
    dir="$1"
    mkdir -p "$dir"
    cd "$dir"
}
