#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

sys.path.append('./../../')
from pyogi.board import initial_state_csa


if __name__ == '__main__':

    path_materials = './../../pyogi/materials/'

    path_jpg = os.path.join(path_materials, 'japanese-chess-b02.jpg')
    img = mpimg.imread(path_jpg)
    plt.figure(figsize=(8, 8))
    plt.tick_params(labelleft='off', labelbottom='off')
    plt.imshow(img, extent=[0, 10, 0, 10])

    csa_to_code = {
        'OU': 1, 'HI': 2, 'KA': 3, 'KI': 4, 'GI': 5,
        'KE': 6, 'KY': 7, 'FU': 8, 'RY': 22, 'UM': 23,
        'NG': 24, 'NK': 26, 'NY': 27, 'TO': 28
    }

    for csa in initial_state_csa.split():
        is_gote = csa[0] == '-'
        i = int(csa[3])
        j = int(csa[4])

        koma_code = is_gote*30 + csa_to_code[csa[5:]]

        fname = 'sgl{0:02}.png'.format(koma_code)
        path_koma = os.path.join('./../../pyogi/materials/', fname)
        img_koma = mpimg.imread(path_koma)
        plt.autoscale(False)
        x, y = 0.5 + (9 - i), 0.5 + (9 - j)
        plt.imshow(img_koma, extent=[x, x+1, y, y+1])
