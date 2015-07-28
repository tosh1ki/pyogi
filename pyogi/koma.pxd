from cpython cimport bool as bool_t

cdef class Koma:
    cdef:
        readonly str kanji, kanji_rear, csa, csa_rear
        readonly bool_t is_promoted
        readonly list act

    cdef void reverse(self)
    cdef void promote(self)
    cdef void depromote(self)
