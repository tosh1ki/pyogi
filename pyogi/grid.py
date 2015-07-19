#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .koma import Koma
from .pieces_act import KOMA_INFOS

class Grid:

    def __init__(self, which_player=None, csa_piece=None):

        if which_player in [None, '+', '-']:
            self.which_player = which_player
        else:
            raise RuntimeError('Invalid which_player:', which_player)

        if csa_piece:
            self.piece = Koma(csa_piece)
        else:
            self.piece = None

    def __repr__(self):
        if self.which_player and self.piece:
            return self.which_player + self.piece.csa
        else:
            return '   '

    def is_empty(self):
        return self.which_player is None
           
    def is_of_sente(self):
        return self.which_player == '+'
