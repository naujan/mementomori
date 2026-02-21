#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "This file needs root privileges."
    echo "run: sudo ./install.sh"
    exit 1
fi

SCRIPT_NAME="mementomori"
SCRIPT_PATH="/usr/bin/$SCRIPT_NAME"
USER_HOME=$(eval echo ~${SUDO_USER})

echo "$USER_HOME"

echo "Copying script to $SCRIPT_PATH"
cp mementomori.py "$SCRIPT_PATH"
echo "Applying permissions"
chmod 755 "$SCRIPT_PATH"

echo "Installation complete."