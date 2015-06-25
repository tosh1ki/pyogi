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

columns = ['csa', 'kanji', 'promoted', 'canpromote', 'beforepromote', 'act']
koma_infos_list = [
    ['FU', '歩', False, True,  None, FU_ACT],
    ['KI', '金', False, False, None, KI_ACT],
    ['GI', '銀', False, True,  None, GI_ACT],
    ['KE', '桂', False, True,  None, KE_ACT],
    ['KY', '香', False, True,  None, KY_ACT],
    ['HI', '飛', False, True,  None, HI_ACT],
    ['KA', '角', False, True,  None, KA_ACT],
    ['OU', '玉', False, False, None, OU_ACT],
    ['UM', '馬', True,  False, 'KA', UM_ACT],
    ['RY', '竜', True,  False, 'HI', RY_ACT],
    ['NG', '全', True,  False, 'GI', NG_ACT],
    ['NY', '杏', True,  False, 'KY', NY_ACT],
    ['NK', '圭', True,  False, 'KE', NK_ACT],
    ['TO', 'と', True,  False, 'FU', TO_ACT]
]

KOMA_INFOS = pd.DataFrame(koma_infos_list, columns=columns)

PIECE_TO_ACT = dict(zip(KOMA_INFOS.csa, KOMA_INFOS.act))
CSA_TO_KANJI = dict(zip(KOMA_INFOS.csa, KOMA_INFOS.kanji))

promoted = KOMA_INFOS[KOMA_INFOS.promoted]
TURN_PIECE = dict(zip(promoted.csa, promoted.beforepromote))
