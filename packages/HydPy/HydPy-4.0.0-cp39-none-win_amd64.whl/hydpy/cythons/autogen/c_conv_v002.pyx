#!python
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: cdivision=True
import numpy
cimport numpy
from libc.math cimport exp, fabs, log, sin, cos, tan, asin, acos, atan, isnan, isinf
from libc.math cimport NAN as nan
from libc.math cimport INFINITY as inf
from libc.stdio cimport *
from libc.stdlib cimport *
import cython
from cpython.mem cimport PyMem_Malloc
from cpython.mem cimport PyMem_Realloc
from cpython.mem cimport PyMem_Free
from hydpy.cythons.autogen cimport annutils
from hydpy.cythons.autogen cimport configutils
from hydpy.cythons.autogen import pointerutils
from hydpy.cythons.autogen cimport pointerutils
from hydpy.cythons.autogen cimport quadutils
from hydpy.cythons.autogen cimport rootutils
from hydpy.cythons.autogen cimport smoothutils

@cython.final
cdef class Parameters:
    cdef public ControlParameters control
    cdef public DerivedParameters derived
@cython.final
cdef class ControlParameters:
    cdef public double[:,:] inputcoordinates
    cdef public double[:,:] outputcoordinates
    cdef public numpy.int32_t maxnmbinputs
    cdef public double power
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int32_t nmbinputs
    cdef public numpy.int32_t nmboutputs
    cdef public double[:,:] distances
    cdef public numpy.int32_t[:,:] proximityorder
    cdef public double[:,:] weights
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public FluxSequences fluxes
    cdef public OutletSequences outlets
@cython.final
cdef class InletSequences:
    cdef double **inputs
    cdef public int len_inputs
    cdef public numpy.int32_t[:] _inputs_ready
    cdef public int _inputs_ndim
    cdef public int _inputs_length
    cdef public int _inputs_length_0
    cpdef inline alloc(self, name, numpy.int32_t length):
        if name == "inputs":
            self._inputs_length_0 = length
            self._inputs_ready = numpy.full(length, 0, dtype=numpy.int32)
            self.inputs = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc(self, name):
        if name == "inputs":
            PyMem_Free(self.inputs)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, int idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "inputs":
            self.inputs[idx] = pointer.p_value
            self._inputs_ready[idx] = 1
    cpdef get_value(self, str name):
        cdef int idx
        if name == "inputs":
            values = numpy.empty(self.len_inputs)
            for idx in range(self.len_inputs):
                pointerutils.check0(self._inputs_length_0)
                if self._inputs_ready[idx] == 0:
                    pointerutils.check1(self._inputs_length_0, idx)
                    pointerutils.check2(self._inputs_ready, idx)
                values[idx] = self.inputs[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "inputs":
            for idx in range(self.len_inputs):
                pointerutils.check0(self._inputs_length_0)
                if self._inputs_ready[idx] == 0:
                    pointerutils.check1(self._inputs_length_0, idx)
                    pointerutils.check2(self._inputs_ready, idx)
                self.inputs[idx][0] = value[idx]
@cython.final
cdef class FluxSequences:
    cdef public double[:] inputs
    cdef public int _inputs_ndim
    cdef public int _inputs_length
    cdef public int _inputs_length_0
    cdef public bint _inputs_diskflag
    cdef public str _inputs_path
    cdef FILE *_inputs_file
    cdef public bint _inputs_ramflag
    cdef public double[:,:] _inputs_array
    cdef public bint _inputs_outputflag
    cdef double *_inputs_outputpointer
    cdef public double[:] outputs
    cdef public int _outputs_ndim
    cdef public int _outputs_length
    cdef public int _outputs_length_0
    cdef public bint _outputs_diskflag
    cdef public str _outputs_path
    cdef FILE *_outputs_file
    cdef public bint _outputs_ramflag
    cdef public double[:,:] _outputs_array
    cdef public bint _outputs_outputflag
    cdef double *_outputs_outputpointer
    cpdef open_files(self, int idx):
        if self._inputs_diskflag:
            self._inputs_file = fopen(str(self._inputs_path).encode(), "rb+")
            fseek(self._inputs_file, idx*self._inputs_length*8, SEEK_SET)
        if self._outputs_diskflag:
            self._outputs_file = fopen(str(self._outputs_path).encode(), "rb+")
            fseek(self._outputs_file, idx*self._outputs_length*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._inputs_diskflag:
            fclose(self._inputs_file)
        if self._outputs_diskflag:
            fclose(self._outputs_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._inputs_diskflag:
            fread(&self.inputs[0], 8, self._inputs_length, self._inputs_file)
        elif self._inputs_ramflag:
            for jdx0 in range(self._inputs_length_0):
                self.inputs[jdx0] = self._inputs_array[idx, jdx0]
        if self._outputs_diskflag:
            fread(&self.outputs[0], 8, self._outputs_length, self._outputs_file)
        elif self._outputs_ramflag:
            for jdx0 in range(self._outputs_length_0):
                self.outputs[jdx0] = self._outputs_array[idx, jdx0]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._inputs_diskflag:
            fwrite(&self.inputs[0], 8, self._inputs_length, self._inputs_file)
        elif self._inputs_ramflag:
            for jdx0 in range(self._inputs_length_0):
                self._inputs_array[idx, jdx0] = self.inputs[jdx0]
        if self._outputs_diskflag:
            fwrite(&self.outputs[0], 8, self._outputs_length, self._outputs_file)
        elif self._outputs_ramflag:
            for jdx0 in range(self._outputs_length_0):
                self._outputs_array[idx, jdx0] = self.outputs[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) nogil:
        pass
@cython.final
cdef class OutletSequences:
    cdef double **outputs
    cdef public int len_outputs
    cdef public numpy.int32_t[:] _outputs_ready
    cdef public int _outputs_ndim
    cdef public int _outputs_length
    cdef public int _outputs_length_0
    cpdef inline alloc(self, name, numpy.int32_t length):
        if name == "outputs":
            self._outputs_length_0 = length
            self._outputs_ready = numpy.full(length, 0, dtype=numpy.int32)
            self.outputs = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc(self, name):
        if name == "outputs":
            PyMem_Free(self.outputs)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, int idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "outputs":
            self.outputs[idx] = pointer.p_value
            self._outputs_ready[idx] = 1
    cpdef get_value(self, str name):
        cdef int idx
        if name == "outputs":
            values = numpy.empty(self.len_outputs)
            for idx in range(self.len_outputs):
                pointerutils.check0(self._outputs_length_0)
                if self._outputs_ready[idx] == 0:
                    pointerutils.check1(self._outputs_length_0, idx)
                    pointerutils.check2(self._outputs_ready, idx)
                values[idx] = self.outputs[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "outputs":
            for idx in range(self.len_outputs):
                pointerutils.check0(self._outputs_length_0)
                if self._outputs_ready[idx] == 0:
                    pointerutils.check1(self._outputs_length_0, idx)
                    pointerutils.check2(self._outputs_ready, idx)
                self.outputs[idx][0] = value[idx]


@cython.final
cdef class Model:
    cdef public int idx_sim
    cdef public Parameters parameters
    cdef public Sequences sequences
    cpdef inline void simulate(self, int idx)  nogil:
        self.idx_sim = idx
        self.update_inlets()
        self.run()
        self.update_outlets()
        self.update_outputs()
    cpdef inline void open_files(self):
        self.sequences.fluxes.open_files(self.idx_sim)
    cpdef inline void close_files(self):
        self.sequences.fluxes.close_files()
    cpdef inline void save_data(self, int idx) nogil:
        self.sequences.fluxes.save_data(self.idx_sim)
    cpdef inline void run(self) nogil:
        self.calc_outputs_v2()
    cpdef inline void update_inlets(self) nogil:
        self.pick_inputs_v1()
    cpdef inline void update_outlets(self) nogil:
        self.pass_outputs_v1()
    cpdef inline void update_receivers(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_senders(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_outputs(self) nogil:
        pass

    cpdef inline void pick_inputs_v1(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputs[idx] = self.sequences.inlets.inputs[idx][0]
    cpdef inline void pick_inputs(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputs[idx] = self.sequences.inlets.inputs[idx][0]
    cpdef inline void calc_outputs_v2(self)  nogil:
        self.interpolate_inversedistance_v1(self.sequences.fluxes.inputs, self.sequences.fluxes.outputs)
    cpdef inline void calc_outputs(self)  nogil:
        self.interpolate_inversedistance_v1(self.sequences.fluxes.inputs, self.sequences.fluxes.outputs)
    cpdef inline void interpolate_inversedistance_v1(self, double[:] inputs, double[:] outputs)  nogil:
        cdef int idx_in
        cdef int idx_try
        cdef int counter_inf
        cdef double d_sumvalues_inf
        cdef double d_sumvalues
        cdef double d_sumweights
        cdef int idx_out
        for idx_out in range(self.parameters.derived.nmboutputs):
            d_sumweights = 0.0
            d_sumvalues = 0.0
            d_sumvalues_inf = 0.0
            counter_inf = 0
            for idx_try in range(self.parameters.control.maxnmbinputs):
                idx_in = self.parameters.derived.proximityorder[idx_out, idx_try]
                if not isnan(inputs[idx_in]):
                    if isinf(self.parameters.derived.weights[idx_out, idx_try]):
                        d_sumvalues_inf = d_sumvalues_inf + (inputs[idx_in])
                        counter_inf = counter_inf + (1)
                    else:
                        d_sumweights = d_sumweights + (self.parameters.derived.weights[idx_out, idx_try])
                        d_sumvalues = d_sumvalues + (self.parameters.derived.weights[idx_out, idx_try] * inputs[idx_in])
            if counter_inf:
                outputs[idx_out] = d_sumvalues_inf / counter_inf
            elif d_sumweights:
                outputs[idx_out] = d_sumvalues / d_sumweights
            else:
                outputs[idx_out] = nan
    cpdef inline void interpolate_inversedistance(self, double[:] inputs, double[:] outputs)  nogil:
        cdef int idx_in
        cdef int idx_try
        cdef int counter_inf
        cdef double d_sumvalues_inf
        cdef double d_sumvalues
        cdef double d_sumweights
        cdef int idx_out
        for idx_out in range(self.parameters.derived.nmboutputs):
            d_sumweights = 0.0
            d_sumvalues = 0.0
            d_sumvalues_inf = 0.0
            counter_inf = 0
            for idx_try in range(self.parameters.control.maxnmbinputs):
                idx_in = self.parameters.derived.proximityorder[idx_out, idx_try]
                if not isnan(inputs[idx_in]):
                    if isinf(self.parameters.derived.weights[idx_out, idx_try]):
                        d_sumvalues_inf = d_sumvalues_inf + (inputs[idx_in])
                        counter_inf = counter_inf + (1)
                    else:
                        d_sumweights = d_sumweights + (self.parameters.derived.weights[idx_out, idx_try])
                        d_sumvalues = d_sumvalues + (self.parameters.derived.weights[idx_out, idx_try] * inputs[idx_in])
            if counter_inf:
                outputs[idx_out] = d_sumvalues_inf / counter_inf
            elif d_sumweights:
                outputs[idx_out] = d_sumvalues / d_sumweights
            else:
                outputs[idx_out] = nan
    cpdef inline void pass_outputs_v1(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmboutputs):
            self.sequences.outlets.outputs[idx][0] = self.sequences.fluxes.outputs[idx]
    cpdef inline void pass_outputs(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmboutputs):
            self.sequences.outlets.outputs[idx][0] = self.sequences.fluxes.outputs[idx]
