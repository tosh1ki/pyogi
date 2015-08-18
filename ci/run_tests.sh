#!/bin/bash

cd ./ci
python convert_ki2.py
cd -
cd ./doc/sample_code/
python demo_plot_state_mpl.py
# python demo_warscrawler.py
python demo_threadcrawler.py
cd -
