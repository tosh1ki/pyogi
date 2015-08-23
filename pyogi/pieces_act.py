#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
各駒の情報 (対応する漢字, 成に関する情報, 効き) を保持する．

# 効きに関して
例えば角の効きを保存している KA_ACT については，
* KA_ACT の4つの要素それぞれが，4方向ある角の効きのそれぞれを表す．
* それぞれの効きの方向を表すリスト (ex. KA_ACT[0]) の要素は，
  それぞれの効きの方向の効きのうち，自身がいるマスからの相対座標で
  表した座標が自身のいるマスから近いものから順に入っている．
'''

import pandas as pd

DIR = [
    [ 1,  0],
    [ 1,  1],
    [ 0,  1],
    [-1,  1],
    [-1,  0],
    [-1, -1],
    [ 0, -1],
    [ 1, -1]
]

ACT1 = [[DIR[i]] for i in range(8) if i%2 == 0]
ACT2 = [[DIR[i]] for i in range(8) if i%2 == 1]

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


columns = ['csa', 'kanji', 'kanji_rear', 'promoted', 'canpromote',
           'ogoma', 'beforepromote', 'afterpromote', 'act']
koma_infos_list = [
    ['FU', '歩', 'と', False, True,  False, None, 'TO', FU_ACT],
    ['KI', '金', None, False, False, False, None, None, KI_ACT],
    ['GI', '銀', '全', False, True,  False, None, 'NG', GI_ACT],
    ['KE', '桂', '圭', False, True,  False, None, 'NK', KE_ACT],
    ['KY', '香', '杏', False, True,  False, None, 'NY', KY_ACT],
    ['HI', '飛', '竜', False, True,  True,  None, 'RY', HI_ACT],
    ['KA', '角', '馬', False, True,  True,  None, 'UM', KA_ACT],
    ['OU', '玉', None, False, False, False, None, None, OU_ACT],
    ['UM', '馬', '角', True,  False, True,  'KA', None, UM_ACT],
    ['RY', '竜', '飛', True,  False, True,  'HI', None, RY_ACT],
    ['NG', '全', '銀', True,  False, False, 'GI', None, NG_ACT],
    ['NY', '杏', '香', True,  False, False, 'KY', None, NY_ACT],
    ['NK', '圭', '桂', True,  False, False, 'KE', None, NK_ACT],
    ['TO', 'と', '歩', True,  False, False, 'FU', None, TO_ACT]
]

KOMA_INFOS = pd.DataFrame(koma_infos_list, columns=columns)

PIECE_TO_ACT = dict(zip(KOMA_INFOS.csa, KOMA_INFOS.act))
KANJI_TO_PIECE = dict(zip(KOMA_INFOS.kanji, KOMA_INFOS.csa))
CSA_TO_KANJI = dict(zip(KOMA_INFOS.csa, KOMA_INFOS.kanji))

promoted = KOMA_INFOS[KOMA_INFOS.promoted]
TURN_PIECE = dict(zip(promoted.csa, promoted.beforepromote))
TURN_PIECE_REVERSED = dict(zip(promoted.beforepromote, promoted.csa))
