# This prompt was inspired by Phil!'s ZSH Prompt
# available at http://aperiodic.net/phil/prompt/

function precmd {
    local TERMWIDTH
    (( TERMWIDTH = ${COLUMNS} - 1 ))

    ###
    # Truncate the path if it's too long.

    PR_FILLBAR=""
    PR_PWDLEN=""

    local promptsize=${#${(%):---(%n@%m)---()--}}
    local pwdsize=${#${(%):-%~}}

    if [[ "$promptsize + $pwdsize" -gt $TERMWIDTH ]]; then
	((PR_PWDLEN=$TERMWIDTH - $promptsize))
    else
	PR_FILLBAR="\${(l.(($TERMWIDTH - ($promptsize + $pwdsize)))..${PR_HBAR}.)}"
    fi
}

setopt extended_glob
preexec () {
    if [[ "$TERM" == "screen" ]]; then
	local CMD=${1[(wr)^(*=*|sudo|-*)]}
	echo -n "\ek$CMD\e\\"
    fi
}


setprompt () {
    ###
    # Need this so the prompt will work.

    setopt prompt_subst

    ###
    # See if we can use extended characters to look nicer.

    typeset -A altchar
    set -A altchar ${(s..)terminfo[acsc]}
    PR_SET_CHARSET="%{$terminfo[enacs]%}"
    PR_SHIFT_IN="%{$terminfo[smacs]%}"
    PR_SHIFT_OUT="%{$terminfo[rmacs]%}"
    PR_HBAR=${altchar[q]:--}
    PR_ULCORNER=${altchar[l]:--}
    PR_LLCORNER=${altchar[m]:--}
    PR_LRCORNER=${altchar[j]:--}
    PR_URCORNER=${altchar[k]:--}

    ###
    # Decide if we need to set titlebar text.

    case $TERM in
	screen)
	    PR_TITLEBAR=$'%{\e_screen \005 | %(!.-=[ROOT]=- | .)%n@%m | %~ \e\\%}'
	    ;;
	*)
	    PR_TITLEBAR=$'%{\e]0;%(!.-=*[ROOT]*=- | .)%n@%m | %~\a%}'
	    ;;
    esac

    ###
    # Decide whether to set a screen title
    if [[ "$TERM" == "screen" ]]; then
	PR_STITLE=$'%{\ekzsh\e\\%}'
    else
	PR_STITLE=''
    fi

    ###
    # Finally, the prompt.

    PROMPT='$PR_SET_CHARSET$PR_STITLE${(e)PR_TITLEBAR}\
$CL_B$PR_SHIFT_IN$PR_ULCORNER$PR_HBAR$PR_SHIFT_OUT(\
$CL_Y%(!.%SROOT%s.%n)$CL_B@$CL_N$CL_LR%m$CL_N$CL_B\
)$PR_SHIFT_IN$PR_HBAR$PR_HBAR${(e)PR_FILLBAR}$PR_HBAR$PR_SHIFT_OUT(\
$CL_N$CL_LM%$PR_PWDLEN<...<%~%<<\
$CL_N$CL_B)$PR_SHIFT_IN$PR_HBAR$PR_URCORNER$PR_SHIFT_OUT\

$PR_SHIFT_IN$PR_LLCORNER$PR_HBAR$PR_SHIFT_OUT(\
$CL_N%(?.$CL_LG.$CL_LR)%?$CL_N$CL_B)\
$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT%(!.$CL_R.$CL_B)%#$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT$CL_N '

    RPROMPT=' $CL_B$PR_SHIFT_IN$PR_HBAR$PR_HBAR$PR_SHIFT_OUT($CL_Y%D{%a %d %b},\
 %*$CL_B)$PR_SHIFT_IN$PR_HBAR$PR_LRCORNER$PR_SHIFT_OUT$CL_N'

    PS2='$CL_B$PR_SHIFT_IN$PR_LLCORNER$PR_SHIFT_OUT(\
$CL_N$CL_LG%4>.>%_%>>$CL_N$CL_B)$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT$CL_N '
}

setprompt