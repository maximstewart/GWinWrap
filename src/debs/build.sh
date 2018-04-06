#!/bin/bash

# Fixes ownershp
function main() {
    sudo find . -type f -exec chmod 644 {} +
    sudo find . -type d -exec chmod 755 {} +

    # Set postrm permissions
    for i in `find . -name postrm`; do
        sudo chmod 755 "${i}"
    done

    # Set fxwinwrap permissions
    for i in `find . -name fxwinwrap`; do
        sudo chmod 755 "${i}"
    done

    # Set xwinwrap permissions
    for i in `find . -name xwinwrap`; do
        sudo chmod 755 "${i}"
    done

    sudo chmod 755 fxwinwrap*/opt/FXWinWrap/resources/bin/*

    sudo chown -R root:root ./*/
builder;
}

#builds debs
function builder() {
    for i in `ls`; do
        if [[ -d "${i}" ]]; then
            dpkg  --build "${i}"
        else
               echo "Not a dir."
        fi
    done
}
main;
