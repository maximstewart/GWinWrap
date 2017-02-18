#!/bin/bash


function main() {
    notify-send -u critical "You need to install ffmpegthumbnailer to have FXWinWrap work properly..."
    xterm -e sudo apt install ffmpegthumbnailer
}
main;
