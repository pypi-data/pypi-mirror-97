# -*- coding: utf-8 -*-
# !python
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True
# -*- coding: utf-8 -*-
"""This module defines the Cython declarations related to module |anntools|."""

from cpython cimport PyObject

cimport numpy

cdef class ANN(object):

    cdef public numpy.int32_t nmb_inputs
    cdef public numpy.int32_t nmb_outputs
    cdef public numpy.int32_t nmb_layers
    cdef public numpy.int32_t[:] nmb_neurons
    cdef public double[:, :] weights_input
    cdef public double[:, :] weights_output
    cdef public double[:, :, :] weights_hidden
    cdef public double[:, :] intercepts_hidden
    cdef public double[:] intercepts_output
    cdef public numpy.int32_t[:, :] activation
    cdef public double[:] inputs
    cdef public double[:] outputs
    cdef public double[:, :] neurons
    cdef public double[:] output_derivatives
    cdef public double[:, :] neuron_derivatives

    cdef inline void apply_activationfunction(self, numpy.int32_t idx_layer, numpy.int32_t idx_neuron, double input_) nogil
    cdef inline double apply_derivativefunction(self, numpy.int32_t idx_layer, numpy.int32_t idx_neuron, double inner) nogil
    cpdef inline void calculate_values(self) nogil
    cpdef inline void calculate_derivatives(self, numpy.int32_t idx_input) nogil


cdef class SeasonalANN(object):

    cdef public numpy.int32_t nmb_anns
    cdef public numpy.int32_t nmb_inputs
    cdef public numpy.int32_t nmb_outputs
    cdef PyObject **canns
    cdef public double[:, :] ratios
    cdef public double[:] inputs
    cdef public double[:] outputs

    cpdef inline void calculate_values(self, numpy.int32_t idx_season) nogil
