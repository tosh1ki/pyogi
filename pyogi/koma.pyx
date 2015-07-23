#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .pieces_act import KOMA_INFOS

from cpython cimport bool as bool_t


cdef class Koma:

    '''Koma class

    Args
    -------------------
    piece_type : str
    '''

    cdef:
        str kanji, kanji_rear, csa, csa_rear
        bool_t is_promoted

    def __init__(self, piece_type):
        if piece_type not in list(KOMA_INFOS.csa):
            raise RuntimeError('Invalid piece_type:', piece_type)

        info = KOMA_INFOS.query('csa == @piece_type').iloc[0, :]
        self.csa = info.csa
        self.kanji = info.kanji
        self.kanji_rear = info.kanji_rear
        self.is_promoted = bool(info.promoted)
        self.act = info.act

        if self.is_promoted:
            self.csa_rear = info.beforepromote
        else:
            self.csa_rear = info.afterpromote

    def __str__(self):
        return self.csa

    cdef void reverse(self):
        self.csa, self.csa_rear = self.csa_rear, self.csa
        self.kanji, self.kanji_rear = self.kanji_rear, self.kanji

    cdef void promote(self):
        '''Promote this piece
        '''
        if not self.is_promoted:
            self.reverse()
            self.is_promoted = True
        else:
            raise RuntimeError('This piece is already promoted.')

    cdef void depromote(self):
        '''Return promoted piece
        '''
        if self.is_promoted:
            self.reverse()
            self.is_promoted = False
        else:
            raise RuntimeError('This piece is NOT promoted.')
