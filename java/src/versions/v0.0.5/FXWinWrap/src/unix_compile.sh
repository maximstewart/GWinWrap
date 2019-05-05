#!/bin/bash
# -Xlint:unchecked
function main() {
    javac *.java
    rm ../com/itdominator/fxwinwrap/*.class
    mv *.class ../com/itdominator/fxwinwrap/
}
main;
