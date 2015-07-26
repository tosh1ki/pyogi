
EMPTY_PLAYER = ' '
EMPTY_CSA = <Koma>None

cdef class Grid:

    '''Grid class

    Args
    -------------------
    which_player : optional (default = None)
    csa_piece : optional (default = None)
    '''
    def __init__(self, which_player=EMPTY_PLAYER, csa_piece=EMPTY_CSA):
        if which_player in [EMPTY_PLAYER, '+', '-']:
            self.which_player = which_player
        else:
            raise RuntimeError('Invalid which_player:', which_player)

        if csa_piece != EMPTY_CSA:
            self.koma = Koma(csa_piece)
        else:
            self.koma = EMPTY_CSA

    def __str__(self):
        if self.which_player != EMPTY_PLAYER and self.koma != EMPTY_CSA:
            return self.which_player + self.koma.csa
        else:
            return EMPTY_PLAYER + EMPTY_CSA

    def is_empty(self):
        return self.which_player == EMPTY_PLAYER

    def is_of_sente(self):
        return self.which_player == '+'

    cdef reset(self):
        self.which_player = EMPTY_PLAYER
        self.koma = EMPTY_CSA
