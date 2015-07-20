#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .koma import Koma
from .pieces_act import KOMA_INFOS


class Grid:
    '''Grid class

    Args
    -------------------
    which_player : optional (default = None)
    csa_piece : optional (default = None)
    '''
    def __init__(self, which_player=None, csa_piece=None):

        if which_player in [None, '+', '-']:
            self.which_player = which_player
        else:
            raise RuntimeError('Invalid which_player:', which_player)

        if csa_piece:
            self.koma = Koma(csa_piece)
        else:
            self.koma = None

    def __str__(self):
        if self.which_player and self.koma:
            return self.which_player + self.koma.csa
        else:
            return '   '
                
    def is_empty(self):
        return self.which_player is None
           
    def is_of_sente(self):
        return self.which_player == '+'

    def reset(self):
        self.which_player = None
        self.koma = None
