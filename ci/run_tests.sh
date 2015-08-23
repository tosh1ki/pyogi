#!/bin/bash

cd ./ci
python convert_ki2.py
cd -
cd ./doc/sample_code/
python demo_plot_state_mpl.py
python search_forking_pro.py -p ./../../data/2chkifu/
python test_komaochi_convert.py -p ./../../data/2chkifu/
python demo_kifuconvert.py -p ./../../data/2chkifu/
cd -
