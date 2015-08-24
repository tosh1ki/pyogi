#!/bin/bash

cd ./ci
bash 2chkifu.sh
python convert_ki2.py
cd -
cd ./doc/sample_code/
python search_forking_pro.py -p ./../../data/2chkifu/
python test_komaochi_convert.py -p ./../../data/2chkifu/ > results_komaochi_convert.txt
python demo_kifuconvert.py -p ./../../data/2chkifu/ > results_kifu_convert.txt
tail results_komaochi_convert.txt
tail results_kifu_convert.txt
cd -
