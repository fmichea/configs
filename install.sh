#!/bin/bash

FILES=(
    .commonshrc .emacs .emacs.d .hg .hgrc .Xdefaults
    .zsh .zshrc
)
FILES_XDG=(awesome)
PWD=`pwd`
INSTALL_PATH=${HOME}

# Installing standart files.
echo "Installing basic files in $INSTALL_PATH directory."
for index in "${FILES[@]}"
do
    echo "=> Installing $pwd/$index as a symlink."
    ln -sf $PWD/$index $INSTALL_PATH/$index
done

# Installing files in $XDG_CONFIG_HOME.
echo "Installing awesome in $XDG_CONFIG_HOME directory."
for index in "${FILES_XDG[@]}"
do
    echo "=> Installing $pwd/$index as a symlink."
    ln -sf $XDG_CONFIG_HOME/$index $INSTALL_PATH/$index
done

# Getting Vicious.
git clone http://git.sysphere.org/vicious
mv vicious $XDG_CONFIG_HOME/awesome/vicious

unset files
unset files_xdg
exit 0
