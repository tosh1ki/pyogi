from .pieces_act import KOMA_INFOS


cdef dict CSA_TO_INFO = KOMA_INFOS.set_index('csa').T.to_dict()
cdef list KOMA_CSA_ALL = list(KOMA_INFOS.csa)


cdef class Koma:

    '''Koma class

    Args
    -------------------
    piece_type : str
    '''
    def __cinit__(self, piece_type):
        if piece_type not in KOMA_CSA_ALL:
            raise RuntimeError('Invalid piece_type:', piece_type)

        info = CSA_TO_INFO[piece_type]
        self.csa = piece_type
        self.kanji = info['kanji']
        self.kanji_rear = info['kanji_rear']
        self.is_promoted = info['promoted']
        self.act = info['act']

        if self.is_promoted:
            self.csa_rear = info['beforepromote']
        else:
            self.csa_rear = info['afterpromote']

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
