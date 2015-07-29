#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd


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
