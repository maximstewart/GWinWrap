#!/bin/bash

function main() {
    for i in `ls`; do
        if [[ -d "${i}" ]]; then
            dpkg  --build "${i}"
        else
               echo "Not a dir."
        fi
    done
}
main;
