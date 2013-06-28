####################################################
# .zshrc: kushou's main configuration file for zsh #
####################################################

################
# Login in a TTY

[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && exec startx &> /dev/null

#####################
# Main Configuration

HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000

autoload -Uz compinit
compinit

setopt correct
setopt hist_ignore_dups # Don't put duplicates in history.
setopt no_bang_hist # Don't redefine ! (useful for commit messages etc...).
setopt nobeep
setopt transient_rprompt # Don't keep RPROMPT when command is entered.
setopt prompt_subst

#########
# Aliases

if [ -f "${HOME}/.zsh/aliases.sh" ]; then
    source "${HOME}/.zsh/aliases.sh"
fi

########################
# Keyboard configuration

if [ -f "${HOME}/.zsh/keyboard.sh" ]; then
    source "${HOME}/.zsh/keyboard.sh"
fi

#######################
# Prompt Configuration

fpath=($fpath "$HOME/.zsh/functions")
typeset -U fpath
autoload -Uz add-zsh-hook

autoload colors zsh/terminfo
if [[ "$terminfo[colors]" -ge 8 ]]; then
    colors
fi
for color in RED GREEN YELLOW BLUE MAGENTA CYAN WHITE; do
    eval CL_${${color}[1]}='%{$terminfo[bold]$fg[${(L)color}]%}'
    eval CL_L${${color}[1]}='%{$fg[${(L)color}]%}'
done
CL_N="%{$terminfo[sgr0]%}"

# Default prompt if not defined in another file loaded after.
#
# [root@localhost pwd]# ... (hour)
# [username@localhost pwd]% ... (hour)

PROMPT="${CL_B}[${CL_Y}%n${CL_B}@${CL_N}${CL_LR}%m ${CL_LM}%~${CL_N}${CL_B}]%#${CL_N} "
RPROMPT="${CL_B}(%*)${CL_N}"

# This file should overwrite PROMPT and RPROMPT.
if ! [ $SSH_TTY ] && [ -f "${HOME}/.zsh/prompt.sh" ] && [ -n "$DISPLAY" ]; then
    source "${HOME}/.zsh/prompt.sh"
fi

##########
# Aliases

alias find='noglob find'
alias reload='. ${HOME}/.zshrc'

######################################################
# Including .zsh_opt, location specific configuration.

if [ -f "${HOME}/.zshrc_opt" ]; then
    source "${HOME}/.zshrc_opt"
fi

# EOF