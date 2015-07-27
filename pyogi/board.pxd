
from .grid cimport Grid
from .koma cimport Koma

from cpython cimport bool as bool_t


cdef class Board:
    cdef:
        readonly list board
        readonly list mochigoma
        readonly int tesu
        readonly str last_move_txt, teai
        public list players
        readonly list last_move_xy

    cpdef get_mochigoma_str(self, teban, kanji=*)
    cpdef set_initial_state(self, teai=*)
    cpdef move(self, move)
