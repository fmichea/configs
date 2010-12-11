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
setopt hist_verify
setopt nobeep
setopt HIST_IGNORE_DUPS
setopt TRANSIENT_RPROMPT

#######################
# Prompt Configuration

CL_R="%{"$'\033[0;31m'"%}"	# RED
CL_B="%{"$'\033[1;34m'"%}"	# BLUE
CL_P="%{"$'\033[0;35m'"%}"	# PURPLE
CL_Y="%{"$'\033[1;33m'"%}"	# YELLOW
CL_N="%{"$'\033[0m'"%}"		# NORMAL

# [root@localhost pwd]# ... (hour)
# [username@localhost pwd]% ... (hour)
PS1="${CL_B}[${CL_Y}%n${CL_B}@${CL_R}%m ${CL_P}%~${CL_B}]%#${CL_N} "
RPS1="${CL_B}(%*)${CL_N}"

##########
# Aliases

alias reload='. ${HOME}/.zshrc'
alias rmold='rm -f **/*~ **/.*~'

###############
# My Functions

srm() # Safe RM
{
    mkdir -vp ~/.trash;
    for i in $*; do
	mv "$i" ~/.trash;
    done
}

ctrash()
{
    rm -rf ~/.trash
}

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
