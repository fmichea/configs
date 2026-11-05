# Make completion case insensitive (found in oh-my-zsh).
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=*' 'l:|=* r:|=*'

# Group completions under their description, which fzf-tab shows as headers
# (F1/F2 switch groups).
zstyle ':completion:*:descriptions' format '[%d]'
# Leave the menu to fzf-tab, so it completes the common prefix first.
zstyle ':completion:*' menu no
# Tab in the fzf-tab list picks the selected entry, like Enter.
zstyle ':fzf-tab:*' fzf-flags --bind=tab:accept
