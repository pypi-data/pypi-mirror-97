# -*- coding: utf-8 -*-
# !python
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True
# -*- coding: utf-8 -*-
"""This Cython module implements the performance-critical features of the
Python module |roottools|."""

cimport numpy

cdef class PegasusBase:

    cdef double apply_method0(self, double x) nogil

    cdef double find_x(
        self,
        double x0,
        double x1,
        double xmin,
        double xmax,
        double xtol,
        double ytol,
        numpy.int32_t itermax,
    ) nogil
