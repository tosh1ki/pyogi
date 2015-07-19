#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .pieces_act import KOMA_INFOS

class Koma:
    '''Koma class
    '''
    def __init__(self, piece_type):
        if not piece_type in list(KOMA_INFOS.csa):
            raise RuntimeError('Invalid piece_type:', piece_type)

        info = KOMA_INFOS.query('csa == @piece_type').iloc[0, :]
        self.csa = info.csa
        self.kanji = info.kanji
        self.is_promoted = bool(info.promoted)
        self.act = info.act

        if self.is_promoted:
            self.csa_rear = info.beforepromote
        else:
            self.csa_rear = info.afterpromote

    def __str__(self):
        return self.csa

    def promote(self):
        if not self.is_promoted:
            self.csa, self.csa_rear = self.csa_rear, self.csa 
            self.is_promoted = True
        else:
            raise RuntimeError('This piece is already promoted.')

    def depromote(self):
        if self.is_promoted:
            self.csa, self.csa_rear = self.csa_rear, self.csa
            self.is_promoted = False
        else:
            raise RuntimeError('This piece is NOT promoted.')
