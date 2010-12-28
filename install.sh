#!/bin/bash

files=(.zshrc .emacs .emacs.d .Xdefaults .commonshrc)
pwd=`pwd`
INSTALL_PATH=${HOME}

# Installing standart files.
echo "Installing basic files in $INSTALL_PATH directory."
for index in "${files[@]}"
do
    echo "=> Installing $pwd/$index as a symlink."
    ln -sf $pwd/$index ${INSTALL_PATH}/$index
done

unset files
exit 0
