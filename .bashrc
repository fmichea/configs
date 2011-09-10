######################################################
# .bashrc: kushou's main configuration file for bash #
######################################################

#####################
# Main Configuration

shopt -s cdspell
shopt -s dotglob

#######################
# Prompt Configuration

CL_B="\[\e[01;34m\]"
CL_G="\[\e[01;32m\]"
CL_LR="\[\e[02;31m\]"
CL_LM="\[\e[02;35m\]"
CL_N="\e[0m"
CL_R="\[\e[01;31m\]"
CL_Y="\[\e[01;33m\]"

# Default Prompt
#
# --[root@localhost]--[pwd]--
# --[return_status]--#--
#
# --[username@localhost]--[pwd]--
# --[return_status]--$--

PS1="${CL_B}--[${CL_Y}\u${CL_B}@${CL_N}${CL_LR}\h\
${CL_N}${CL_B}]--[${CL_N}${CL_LM}\w${CL_N}${CL_B}]--\

--[\
\`foo=\$?; if [[ \$foo -eq 0 ]]; then echo -n \"${CL_G}\"; else echo -n \"${CL_R}\";\
 fi; echo -n \$foo;\`${CL_B}]--\$ ${CL_N}"

################################################################
# Including .commonshrc, common configuration for bash and zsh.

if [ -f $HOME/.commonshrc ]; then
    source $HOME/.commonshrc
else
    echo "Common configration file is not found !"
fi