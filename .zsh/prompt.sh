# Prompt configuration. Largely inspired by zsh-git wunjo theme and Ph1l!'s
# prompt.

autoload -Uz zgitinit; zgitinit

function revstring {
    git describe --tags --always "$1" 2>/dev/null ||
    git rev-parse --short "$1" 2>/dev/null
}

coloratom() {
    local off=$1 atom=$2
    if [[ $atom[1] == [[:upper:]] ]]; then
        off=$(( $off + 60 ))
    fi
    echo $(( $off + $colorcode[${(L)atom}] ))
}

function colorword {
    local fg=$1 bg=$2 att=$3
    local -a s

    if [ -n "$fg" ]; then
        s+=$(coloratom 30 $fg)
    fi
    if [ -n "$bg" ]; then
        s+=$(coloratom 40 $bg)
    fi
    if [ -n "$att" ]; then
        s+=$attcode[$att]
    fi

    echo "%{"$'\e['${(j:;:)s}m"%}"
}

_prompt_precmd() {
    local ex=$?
    psvar=()

    if [[ $ex -ge 128 ]]; then
        sig=$signals[$ex-127]
        psvar[1]="${sig}"
    else
        psvar[1]="$ex"
    fi
    echo -ne "\a"
}

function _prompt_setup() {
    typeset -A pr
    typeset -A altchar
    set -A altchar ${(s..)terminfo[acsc]}
    pr[in]="%{$terminfo[smacs]%}"
    pr[out]="%{$terminfo[rmacs]%}"
    pr[h]=${altchar[q]:--}
    pr[ul]=${altchar[l]:--}
    pr[ll]=${altchar[m]:--}
    pr[lr]=${altchar[j]:--}
    pr[ur]=${altchar[k]:--}
    pr[t]=${altchar[t]:--}

    typeset -A colorcode
    colorcode[black]=0
    colorcode[red]=1
    colorcode[green]=2
    colorcode[yellow]=3
    colorcode[blue]=4
    colorcode[magenta]=5
    colorcode[cyan]=6
    colorcode[white]=7
    colorcode[default]=9
    colorcode[k]=$colorcode[black]
    colorcode[r]=$colorcode[red]
    colorcode[g]=$colorcode[green]
    colorcode[y]=$colorcode[yellow]
    colorcode[b]=$colorcode[blue]
    colorcode[m]=$colorcode[magenta]
    colorcode[c]=$colorcode[cyan]
    colorcode[w]=$colorcode[white]
    colorcode[.]=$colorcode[default]

    typeset -A attcode
    attcode[none]=00
    attcode[bold]=01
    attcode[faint]=02
    attcode[standout]=03
    attcode[underline]=04
    attcode[blink]=05
    attcode[reverse]=07
    attcode[conceal]=08
    attcode[normal]=22
    attcode[no-standout]=23
    attcode[no-underline]=24
    attcode[no-blink]=25
    attcode[no-reverse]=27
    attcode[no-conceal]=28

    local -A pc
    pc[default]='default'
    pc[date]='Yellow'
    pc[time]='Yellow'
    pc[host]='red'
    pc[user]='Yellow "" bold'
    pc[punc]='blue'
    pc[path]='magenta'
    pc[ok]='green'
    pc[ko]='red'
    pc[scm_branch]='Cyan'
    pc[scm_commitid]='Yellow'
    pc[scm_status_dirty]='Red'
    pc[scm_status_staged]='Green'
    pc[#]='blue "" bold'
    for cn in ${(k)pc}; do
        pc[${cn}]=$(eval colorword $pc[$cn])
    done
    pc[reset]=$(colorword . . 00)

    typeset -Ag prompt_colors
    prompt_colors=(${(kv)pc})
    typeset -Ag prompt_modifiers
    prompt_modifiers=(${(kv)pr})

#    local p_date p_line p_rc
#
    p_date=
#
#    p_line="$pc[line]%y$pc[reset]"

    PROMPT=
    PROMPT+="$pc[#]$pr[in]$pr[ul]$pr[h]$pr[out]($pc[reset]"
    PROMPT+="$pc[user]%(!.%SROOT%s.%n)$pc[reset]$pc[#]@$pc[reset]$pc[host]%m$pc[reset]$pc[reset]"
    PROMPT+="$pc[#])$pr[in]$pr[h]$pr[out]($pc[reset]"
    PROMPT+="$pc[path]%$pr[pwdlen]<...<%~%<<$pc[reset]"
    PROMPT+="$pc[#])$pr[in]$pr[h]$pr[out]$pc[reset]"
    PROMPT+="\$(_scm_status)\$(_scm_branch)"

    PROMPT+=$'\n'

    PROMPT+="$pc[#]$pr[in]$pr[ll]$pr[h]$pr[out]($pc[reset]"
    PROMPT+="%(?.$pc[ok].$pc[ko])%1v$pc[reset]"
    PROMPT+="$pc[#])$pr[in]$pr[h]$pr[out]$pc[reset]"
    PROMPT+="%(!.$pc[ko].$pc[#])%#$pc[reset]"
    PROMPT+="$pc[#]$pr[in]$pr[h]$pr[out]$pc[reset] "

    RPROMPT="$pc[#]$pr[in]$pr[h]$pr[out]($pr[reset]"
    RPROMPT+="$pc[time]%D{%T}$pc[reset]"
    RPROMPT+="$pc[#])$pr[in]$pr[h]$pr[out]$pc[reset]"

    export PROMPT RPROMPT
    add-zsh-hook precmd _prompt_precmd
}

function _scm_status {
    zgit_isgit || return

    local -A pc
    pc=(${(kv)prompt_colors})

    local -A pr
    pr=(${(kv)prompt_modifiers})

    head=$(zgit_head)
    gitcommit=$(revstring $head)

    local -a commits

    if zgit_rebaseinfo; then
        orig_commit=$(revstring $zgit_info[rb_head])
        orig_name=$(git name-rev --name-only $zgit_info[rb_head])
        orig="$pc[scm_branch]$orig_name$pc[punc]($pc[scm_commitid]$orig_commit$pc[punc])"
        onto_commit=$(revstring $zgit_info[rb_onto])
        onto_name=$(git name-rev --name-only $zgit_info[rb_onto])
        onto="$pc[scm_branch]$onto_name$pc[punc]($pc[scm_commitid]$onto_commit$pc[punc])"

        if [ -n "$zgit_info[rb_upstream]" ] && [ $zgit_info[rb_upstream] != $zgit_info[rb_onto] ]; then
            upstream_commit=$(revstring $zgit_info[rb_upstream])
            upstream_name=$(git name-rev --name-only $zgit_info[rb_upstream])
            upstream="$pc[scm_branch]$upstream_name$pc[punc]($pc[scm_commitid]$upstream_commit$pc[punc])"
            commits+="rebasing $upstream$pc[reset]..$orig$pc[reset] onto $onto$pc[reset]"
        else
            commits+="rebasing $onto$pc[reset]..$orig$pc[reset]"
        fi

        local -a revs
        revs=($(git rev-list $zgit_info[rb_onto]..HEAD))
        if [ $#revs -gt 0 ]; then
            commits+="\n$#revs commits in"
        fi

        if [ -f $zgit_info[dotest]/message ]; then
            mess=$(head -n1 $zgit_info[dotest]/message)
            commits+="on $mess"
        fi
    elif [ -n "$gitcommit" ]; then
        commits+="$pc[scm_branch]$head$pc[punc]($pc[scm_commitid]$gitcommit$pc[punc])$pc[reset]"
        local track_merge=$(zgit_tracking_merge)
        if [ -n "$track_merge" ]; then
            if git rev-parse --verify -q $track_merge >/dev/null; then
                local track_remote=$(zgit_tracking_remote)
                local tracked=$(revstring $track_merge 2>/dev/null)

                local -a revs_ahead
                local -a revs_behind
                revs_ahead=($(git rev-list --reverse $track_merge..HEAD))
                revs_behind=($(git rev-list --reverse HEAD..$track_merge))
                if [ $#revs_ahead -gt 0 ] || [ $#revs_behind -gt 0 ]; then
                    local base=""
                    local base_name=$(git name-rev --name-only $base)
                    local base_short=$(revstring $base)

                    if [ $#revs_behind -gt 0 ]; then
                        base=$(revstring $revs_behind[1]~1)
                        commits+="$pc[ko]-$pc[reset]$#revs_behind"
                    else
                        base=$(revstring $revs_ahead[1]~1)
                        commits+="$pc[ok]+$pc[reset]$#revs_ahead"
                    fi
                fi

                if [ -n "$tracked" ]; then
                    local track_name=$track_merge
                    if [[ $track_remote == "." ]]; then
                        track_name=${track_name##*/}
                    fi
                    tracked=$(revstring $tracked)
                    commits+="$pc[scm_branch]$track_name$pc[punc]"

                    if [[ "$tracked" != "$gitcommit" ]]; then
                        commits[$#commits]+="($pc[scm_commitid]$tracked$pc[punc])"
                    fi
                    commits[$#commits]+="$pc[reset]"
                fi
            fi
        fi
    fi

    if [ $#commits -gt 0 ]; then
        echo -n "$pc[#]($pc[reset]"
        local sep="$pc[#])$pr[in]$pr[h]$pr[out]($pc[reset]"
        for idx in `seq $#commits`; do
            if [ $idx -ne 1 ]; then
                echo -ne "$sep"
            fi
            echo -n "${commits[idx]}"
        done
        echo -n "$pc[#])$pr[in]$pr[h]$pr[out]"
    fi
}

_scm_branch() {
    zgit_isgit || return
    local -A pc
    pc=(${(kv)prompt_colors})

    local -A pr
    pr=(${(kv)prompt_modifiers})

    if zgit_inworktree; then
        local staged=""
        if ! zgit_isindexclean; then
             staged="$pc[scm_status_staged]+$pc[reset]"
        fi

        local -a dirty
        if ! zgit_isworktreeclean; then
            dirty+='!'
        fi

        if zgit_hasunmerged; then
            dirty+='*'
        fi

        if zgit_hasuntracked; then
            dirty+='?'
        fi

        if [ $#dirty -gt 0 ] || [ -n "$staged" ]; then
            echo -n "$pc[#]($pc[reset]$staged"
            echo -n "$pc[scm_status_dirty]${(j::)dirty}"
            echo -n "$pc[#])$pr[in]$pr[h]$pr[out]"
        fi
    fi

    echo $pc[reset]
}

_prompt_setup "$@"
