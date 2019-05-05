#!/bin/bash

function main() {
    jar cvfm FXWinWrap.jar manifest.txt com/itdominator/fxwinwrap/*.class \
                                        com/itdominator/fxwinwrap/resources
    chmod +x FXWinWrap.jar
    mv FXWinWrap.jar ../
}
main;
