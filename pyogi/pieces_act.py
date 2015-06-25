#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd


ACT1 = [
    [[ 1,  0]],
    [[ 0,  1]],
    [[-1,  0]],
    [[ 0, -1]]
]
ACT2 = [
    [[ 1,  1]],
    [[-1,  1]],
    [[-1, -1]],
    [[ 1, -1]]
]

KA_ACT = [
    [[ 1,  1], [ 2,  2], [ 3,  3], [ 4,  4],
     [ 5,  5], [ 6,  6], [ 7,  7], [ 8,  8]],
    [[ 1, -1], [ 2, -2], [ 3, -3], [ 4, -4],
     [ 5, -5], [ 6, -6], [ 7, -7], [ 8, -8]],
    [[-1,  1], [-2,  2], [-3,  3], [-4,  4],
     [-5,  5], [-6,  6], [-7,  7], [-8,  8]],
    [[-1, -1], [-2, -2], [-3, -3], [-4, -4],
     [-5, -5], [-6, -6], [-7, -7], [-8, -8]]
]

HI_ACT = [
    [[ 1,  0], [ 2,  0], [ 3,  0], [ 4,  0],
     [ 5,  0], [ 6,  0], [ 7,  0], [ 8,  0]],
    [[-1,  0], [-2,  0], [-3,  0], [-4,  0],
     [-5,  0], [-6,  0], [-7,  0], [-8,  0]],
    [[ 0,  1], [ 0,  2], [ 0,  3], [ 0,  4],
     [ 0,  5], [ 0,  6], [ 0,  7], [ 0,  8]],
    [[ 0, -1], [ 0, -2], [ 0, -3], [ 0, -4],
     [ 0, -5], [ 0, -6], [ 0, -7], [ 0, -8]]
]

KY_ACT = [
    [[ 0, -1], [ 0, -2], [ 0, -3], [ 0, -4],
     [ 0, -5], [ 0, -6], [ 0, -7], [ 0, -8]]
]

KE_ACT = [
    [[ 1, -2]],
    [[-1, -2]]
]

KI_ACT = [
    [[ 1, -1]],
    [[-1, -1]]
]
KI_ACT.extend(ACT1)

TO_ACT = KI_ACT
NG_ACT = KI_ACT
NY_ACT = KI_ACT
NK_ACT = KI_ACT

GI_ACT = [
    [[ 0, -1]]
]
GI_ACT.extend(ACT2)

FU_ACT = [[[0, -1]]]

UM_ACT = []
UM_ACT.extend(KA_ACT)
UM_ACT.extend(ACT1)

RY_ACT = []
RY_ACT.extend(HI_ACT)
RY_ACT.extend(ACT2)

OU_ACT = []
OU_ACT.extend(ACT1)
OU_ACT.extend(ACT2)

ACTS = [
    OU_ACT, HI_ACT, KA_ACT, KI_ACT, GI_ACT,
    KE_ACT, KY_ACT, FU_ACT, RY_ACT, UM_ACT,
    NG_ACT, NK_ACT, NY_ACT, TO_ACT
]

ALL_KOMA = [
    'OU', 'HI', 'KA', 'KI', 'GI',
    'KE', 'KY', 'FU', 'RY', 'UM',
    'NG', 'NK', 'NY', 'TO'
]
TURN_PIECE = {
    'TO': 'FU', 'NY': 'KY', 'NK': 'KE',
    'NG': 'GI', 'UM': 'KA', 'RY': 'HI'
}

PIECE_TO_ACT = dict(zip(ALL_KOMA, ACTS))

KOMA_KANJI = ['歩', '香', '桂', '銀', '金', '角', '飛', '玉']
KOMA_CSA = ['FU', 'KY', 'KE', 'GI', 'KI', 'KA', 'HI', 'OU']
CSA_TO_KANJI = {
    'FU': '歩', 'KI': '金', 'GI': '銀', 'KE': '桂', 'KY': '香',
    'HI': '飛', 'KA': '角', 'OU': '玉', 'UM': '馬', 'RY': '竜',
    'NG': '全', 'NY': '杏', 'NK': '圭', 'TO': 'と'
}

columns = ['csa', 'kanji', 'promoted', 'act']
koma_infos_list = [
    ['FU', '歩', False, FU_ACT],
    ['KI', '金', False, KI_ACT],
    ['GI', '銀', False, GI_ACT],
    ['KE', '桂', False, KE_ACT],
    ['KY', '香', False, KY_ACT],
    ['HI', '飛', False, HI_ACT],
    ['KA', '角', False, KA_ACT],
    ['OU', '玉', False, OU_ACT],
    ['UM', '馬', True,  UM_ACT],
    ['RY', '竜', True,  RY_ACT],
    ['NG', '全', True,  NG_ACT],
    ['NY', '杏', True,  NY_ACT],
    ['NK', '圭', True,  NK_ACT],
    ['TO', 'と', True,  TO_ACT]
]

KOMA_INFOS = pd.DataFrame(koma_infos_list, columns=columns)
