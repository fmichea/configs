#!/bin/sh

function usage {
    echo "usage: $0 [-p install_path] [-x xdg_path] install/uninstall"
    exit 1
}

[ $# -lt 1 ] && usage

FILES=".hgrc .Xdefaults .zsh .zshrc .gitignore .gitconfig .vim .vimrc"
FILES+=".tmux.conf .xinitrc .mutt .gvimrc"

FILES_XDG="i3 i3status"

INSTALL_PATH=${HOME}
XDG_PATH=${XDG_CONFIG_HOME:-"$HOME/.config"}

while getopts "p:x:" arg; do
    case $arg in
        p ) INSTALL_PATH=$OPTARG;;
        x ) XDG_PATH=$OPTARG;;
    esac
done
shift $(( $OPTIND - 1 ))

[ $# -ne 1 ] && usage

INSTALL_TYPE=$1
INSTALL_PATH_FILE=~/.config_installpath

function make_link {
    echo "=> Installing $2 in $1."
    ln -sf `pwd`/$2 $1/$2
}

function remove_link {
    echo "=> Removing link created at $1."
    rm -f $1
}

if [ $INSTALL_TYPE = "uninstall" ]; then
    if [ -e $INSTALL_PATH_FILE ]; then
        INSTALL_PATH=`head -n 1 $INSTALL_PATH_FILE`
        XDG_PATH=`tail -n 1 $INSTALL_PATH_FILE`
        rm $INSTALL_PATH_FILE
    else
        echo "$INSTALL_PATH_FILE not found. Nothing is installed."
        exit 2
    fi
elif [ $INSTALL_TYPE = "install" ]; then
    echo -ne "$INSTALL_PATH\n$XDG_PATH" > $INSTALL_PATH_FILE
else
    echo "I don't know action \"$INSTALL_TYPE\"."
    exit 3
fi

function install_files {
    for filename in $1; do
        case $INSTALL_TYPE in
            install ) [ -e "$2/$filename" ] || make_link $2 $filename;;
            uninstall ) [ -e "$2/$filename" ] && remove_link "$2/$filename";;
        esac
    done
}

install_files "$FILES" $INSTALL_PATH
install_files "$FILES_XDG" $XDG_PATH

exit 0

# EOF
