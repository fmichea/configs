#####################
# KeyBoard Bindings

bindkey -e

typeset -A key

key[Home]="${terminfo[khome]}"
key[End]="${terminfo[kend]}"
key[Insert]="${terminfo[kich1]}"
key[Delete]="${terminfo[kdch1]}"
key[Up]="${terminfo[kcuu1]}"
key[Down]="${terminfo[kcud1]}"
key[Left]="${terminfo[kcub1]}"
key[Right]="${terminfo[kcuf1]}"
key[PageUp]="${terminfo[kpp]}"
key[PageDown]="${terminfo[knp]}"

# Normal behavior for home and end.
[[ -n "${key[Home]}" ]] && bindkey "${key[Home]}" beginning-of-line
[[ -n "${key[End]}" ]] && bindkey "${key[End]}" end-of-line

# Normal behavior of delete and insert.
[[ -n "${key[Insert]}" ]] && bindkey "${key[Insert]}" overwrite-mode
[[ -n "${key[Delete]}" ]] && bindkey "${key[Delete]}" delete-char

# Normal behavior of Left and Right
[[ -n "${key[Left]}" ]] && bindkey "${key[Left]}" backward-char
[[ -n "${key[Right]}" ]] && bindkey "${key[Right]}" forward-char

[[ -n "${key[Up]}" ]] && bindkey "${key[Up]}" up-line-or-history
[[ -n "${key[Down]}" ]] && bindkey "${key[Down]}" down-line-or-history

# Xterm compatibility layer AFAIK.
if [ -n "$DISPLAY" ]; then
    function zle-line-init () {
        echoti smkx
    }
    function zle-line-finish () {
        echoti rmkx
    }
    zle -N zle-line-init
    zle -N zle-line-finish
fi

# Up and Down begin a search in history, from the beginning of the line. It
# searches for all of commands that start like the left of your cursor in
# history. If cursor is at the beginning of the line it will just behave like
# normal Up/Down behavior.
#
# Note: if you want to append content to the current line, just hit End or
# Ctrl-E.
#
# FIXME: Find a way to use terminfos.
if [ "$HOST_OS" = "Linux" ]; then
    bindkey "^[Oa" history-beginning-search-backward
    bindkey '^[Ob' history-beginning-search-forward
    bindkey '^[Od' emacs-backward-word
    bindkey '^[Oc' emacs-forward-word
elif [ "$HOST_OS" = "Darwin" ]; then
    bindkey ";5A" history-beginning-search-backward
    bindkey ';5B' history-beginning-search-forward
    bindkey ';5D' emacs-backward-word
    bindkey ';5C' emacs-forward-word
fi

# Stop on slash in paths when using ^W.
tcsh-backward-kill-word () {
    local WORDCHARS="${WORDCHARS//[\/._:-]/}"
    zle backward-delete-word
}
zle -N backward-kill-word tcsh-backward-kill-word

# Opens man of the command.
autoload run-help
bindkey "^xh" run-help

# Edit command in vim.
autoload edit-command-line && zle -N edit-command-line
bindkey "^xe" edit-command-line
