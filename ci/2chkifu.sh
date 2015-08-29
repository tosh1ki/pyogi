#!/bin/bash

cd ./../data/

if [ ! -f 2chkifu.zip ]; then
    wget https://zipkifubrowser.googlecode.com/files/2chkifu.zip
fi

if [ ! -d 2chkifu/ ]; then
    unzip -q 2chkifu.zip
fi

cd -
