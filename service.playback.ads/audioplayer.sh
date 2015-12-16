#!/bin/bash

PLAYER_CMD="$1"
cd "$2"

# Play the directory structure
while true
do
    for file in *.mp3
    do
        echo $PLAYER_CMD "$2/$file"
        $PLAYER_CMD "$2/$file"
    done
done