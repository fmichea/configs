#! /bin/sh

################################################################################
# startup.sh: Launched by i3 when it starts.                                   #
################################################################################

# Disable audible bell.
xset b off

# Screen layout.
if [ -f ~/scripts/misc/screen_switch.py ]; then
    python ~/scripts/misc/screen_switch.py
fi

# Keymap.
if [ -f ~/scripts/misc/keymap_switch.py ]; then
    python ~/scripts/misc/keymap_switch.py
fi
setxkbmap -option caps:none

# Background picutre.
feh --bg-scale ~/.config/i3/wallpaper.jpg

# Default programs.
pulseaudio --start
keepassx &
