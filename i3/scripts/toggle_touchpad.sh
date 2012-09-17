#! /bin/sh

FILE="/tmp/touchpad.disabled"

if [ -f "$FILE" ]; then
    rm -f "$FILE"
    synclient TouchpadOff=0
else
    touch "$FILE"
    synclient TouchpadOff=1
fi
