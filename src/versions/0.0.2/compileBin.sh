#!/bin/bash

function main() {
    gcc -no-pie -s gwinwrap_exec_bin.cpp -o gwinwrap
}
main;
