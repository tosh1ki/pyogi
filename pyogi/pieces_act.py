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


columns = ['csa', 'kanji', 'promoted', 'canpromote', 'ogoma',
           'beforepromote', 'afterpromote', 'act']
koma_infos_list = [
    ['FU', '歩', False, True,  False, None, 'TO', FU_ACT],
    ['KI', '金', False, False, False, None, None, KI_ACT],
    ['GI', '銀', False, True,  False, None, 'NG', GI_ACT],
    ['KE', '桂', False, True,  False, None, 'NK', KE_ACT],
    ['KY', '香', False, True,  False, None, 'NY', KY_ACT],
    ['HI', '飛', False, True,  True,  None, 'RY', HI_ACT],
    ['KA', '角', False, True,  True,  None, 'UM', KA_ACT],
    ['OU', '玉', False, False, False, None, None, OU_ACT],
    ['UM', '馬', True,  False, True,  'KA', None, UM_ACT],
    ['RY', '竜', True,  False, True,  'HI', None, RY_ACT],
    ['NG', '全', True,  False, False, 'GI', None, NG_ACT],
    ['NY', '杏', True,  False, False, 'KY', None, NY_ACT],
    ['NK', '圭', True,  False, False, 'KE', None, NK_ACT],
    ['TO', 'と', True,  False, False, 'FU', None, TO_ACT]
]

KOMA_INFOS = pd.DataFrame(koma_infos_list, columns=columns)

PIECE_TO_ACT = dict(zip(KOMA_INFOS.csa, KOMA_INFOS.act))
KANJI_TO_PIECE = dict(zip(KOMA_INFOS.kanji, KOMA_INFOS.csa))
CSA_TO_KANJI = dict(zip(KOMA_INFOS.csa, KOMA_INFOS.kanji))

promoted = KOMA_INFOS[KOMA_INFOS.promoted]
TURN_PIECE = dict(zip(promoted.csa, promoted.beforepromote))
TURN_PIECE_REVERSED = dict(zip(promoted.beforepromote, promoted.csa))


_teai_options = [
    ['手合割：平手', 'hirate', []],
    ['手合割：角落ち', 'kakuoti', ['22KA']],
    ['手合割：飛車落ち', 'hisyaoti', ['82HI']],
    ['手合割：香落ち', 'kyouoti', ['11KY']],
    ['手合割：右香落ち', 'migikyouoti', ['91KY']],
    ['手合割：飛香落ち', 'hikyouoti', ['82HI', '11KY']],
    ['手合割：二枚落ち', 'nimaioti', ['82HI', '22KA']],
    ['手合割：三枚落ち', 'sanmaioti', ['82HI', '22KA', '11KY']],
    ['手合割：四枚落ち', 'yonmaioti', ['91KY', '82HI', '22KA', '11KY']],
    ['手合割：六枚落ち', 'rokumaioti',
     ['91KY', '81KE', '82HI', '22KA', '21KE', '11KY']],
    ['手合割：その他',   'sonota', None]
]
TEAI_OPTIONS = pd.DataFrame(_teai_options,
                            columns = ['japanese', 'code', 'pieces'])

KOMAOCHI_OPTIONS = dict(zip(TEAI_OPTIONS.code, TEAI_OPTIONS.pieces))
TEAITXT_TO_TEAI = dict(zip(TEAI_OPTIONS.japanese, TEAI_OPTIONS.code))
komaochi_csa = list(map(lambda x: 'PI'+''.join(x), TEAI_OPTIONS.pieces[1:10]))

KOMAOCHI_CSA_TO_CODE = dict(zip(komaochi_csa, TEAI_OPTIONS.code[1:10]))
KOMAOCHI_CODE_TO_CSA = dict(zip(TEAI_OPTIONS.code[1:10], komaochi_csa))















