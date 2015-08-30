#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


csapath = os.path.join(os.path.dirname(__file__), 'initial_state_hirate.csa')

with open(csapath, 'r') as f:
    initial_state_csa = '\n'.join(f.readlines())

