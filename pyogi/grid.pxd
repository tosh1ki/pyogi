from .koma cimport Koma
from cpython cimport bool as bool_t


cdef class Grid:
    cdef:
        public str which_player
        public Koma koma

    cpdef bool_t is_empty(self)
    cpdef bool_t is_of_sente(self)
    cpdef int reset(self)
