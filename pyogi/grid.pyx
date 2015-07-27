
cdef:
    str EMPTY_PLAYER = ' '
    EMPTY_CSA = <Koma>None
    str SENTE_STR = '+'
    list PLAYER_LIST = [EMPTY_PLAYER, '+', '-']


cdef class Grid:

    '''Grid class

    Args
    -------------------
    which_player : optional (default = None)
    csa_piece : optional (default = None)
    '''
    def __init__(self, str which_player=EMPTY_PLAYER, str csa_piece=''):
        if which_player in PLAYER_LIST:
            self.which_player = which_player
        else:
            raise RuntimeError('Invalid which_player:', which_player)

        if csa_piece != '':
            self.koma = Koma(csa_piece)
        else:
            self.koma = EMPTY_CSA

    def __str__(self):
        if self.which_player != EMPTY_PLAYER and self.koma != EMPTY_CSA:
            return self.which_player + self.koma.csa
        else:
            return '   '

    cpdef bool_t is_empty(self):
        return self.which_player == EMPTY_PLAYER

    cpdef bool_t is_of_sente(self):
        return self.which_player == SENTE_STR

    cpdef int reset(self):
        self.which_player = EMPTY_PLAYER
        self.koma = EMPTY_CSA
