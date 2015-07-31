
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

    cpdef str get_mochigoma_str(self, int teban, bool_t kanji=*)
    cpdef int set_initial_state(self, str teai=*)
    cpdef list move(self, str move)
    cpdef list is_forking_query(self, str query_piece, list targets, bool_t display=*)
