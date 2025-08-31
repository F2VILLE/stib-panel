#!/bin/bash

if [ "$1" == "clean" ]; then
    rm -rf build dist *.spec
    exit 0
fi

pyinstaller --onefile main.py -n stib-panel && cp -r ./views ./dist