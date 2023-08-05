# -*- coding: utf-8 -*-
# !python
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True
# -*- coding: utf-8 -*-

cimport numpy

cdef class DoubleBase:
    pass


cdef class Double(DoubleBase):

    cdef double value


cdef class PDouble(DoubleBase):

    cdef double *p_value


cdef class PPDouble:

    cdef object ready
    cdef numpy.int32_t length
    cdef double **pp_value
    cdef bint _allocated