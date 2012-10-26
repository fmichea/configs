####################################################
# .zshrc: kushou's main configuration file for zsh #
####################################################

#####################
# Main Configuration

HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000

autoload -Uz compinit
compinit

setopt correct
#setopt hist_verify
setopt nobeep
setopt HIST_IGNORE_DUPS
setopt TRANSIENT_RPROMPT

#######################################################
# KeyBoard Bindings found in magicking's configuration

bindkey -e

bindkey "^[[1~" beginning-of-line
bindkey "^[OH"  beginning-of-line
bindkey "\e[1~" beginning-of-line
bindkey "\e[7~" beginning-of-line

bindkey "\e[4~" end-of-line
bindkey "\e[8~" end-of-line
bindkey "^[[4~" end-of-line
bindkey "^[OF"  end-of-line

bindkey "^[[3~" delete-char
bindkey "\e[3~" delete-char

bindkey "\e[2~" overwrite-mode

#######################
# Prompt Configuration

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
if ! [ $SSH_TTY ] && [ -f ${HOME}/.zsh/prompt.sh ]; then
    source ${HOME}/.zsh/prompt.sh
fi

##########
# Aliases

alias find='noglob find'
alias reload='. ${HOME}/.zshrc'

################################################################
# Including .commonshrc, common configuration for bash and zsh.
# Including .zsh_opt, location specific configuration.

if [ -f ${HOME}/.commonshrc ]; then
    source ${HOME}/.commonshrc
else
    echo "Common configuration file is not found !"
fi

if [ -f ${HOME}/.zshrc_opt ]; then
    source ${HOME}/.zshrc_opt
fi

# EOF
