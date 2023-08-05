# -*- coding: utf-8 -*-
# !python
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True
# -*- coding: utf-8 -*-
"""This module defines the Cython declarations related to module
|configutils|.
"""

cdef class Config(object):

    cdef public double _abs_error_max
    cdef public double _rel_dt_min
