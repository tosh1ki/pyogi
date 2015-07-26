from .koma cimport Koma

cdef class Grid:
    cdef:
        public str which_player
        public Koma koma

    cdef reset(self)
