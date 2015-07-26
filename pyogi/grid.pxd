from .koma cimport Koma

cdef class Grid:
    cdef:
        public str which_player
        public Koma koma

    cpdef is_empty(self)
    cpdef is_of_sente(self)
    cpdef reset(self)
