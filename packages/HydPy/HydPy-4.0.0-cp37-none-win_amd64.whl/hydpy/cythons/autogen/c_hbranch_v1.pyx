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
    cdef public double[:] xpoints
    cdef public double[:,:] ypoints
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int32_t nmbbranches
    cdef public numpy.int32_t nmbpoints
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public FluxSequences fluxes
    cdef public OutletSequences outlets
@cython.final
cdef class InletSequences:
    cdef double **total
    cdef public int len_total
    cdef public numpy.int32_t[:] _total_ready
    cdef public int _total_ndim
    cdef public int _total_length
    cdef public int _total_length_0
    cpdef inline alloc(self, name, numpy.int32_t length):
        if name == "total":
            self._total_length_0 = length
            self._total_ready = numpy.full(length, 0, dtype=numpy.int32)
            self.total = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc(self, name):
        if name == "total":
            PyMem_Free(self.total)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, int idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "total":
            self.total[idx] = pointer.p_value
            self._total_ready[idx] = 1
    cpdef get_value(self, str name):
        cdef int idx
        if name == "total":
            values = numpy.empty(self.len_total)
            for idx in range(self.len_total):
                pointerutils.check0(self._total_length_0)
                if self._total_ready[idx] == 0:
                    pointerutils.check1(self._total_length_0, idx)
                    pointerutils.check2(self._total_ready, idx)
                values[idx] = self.total[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "total":
            for idx in range(self.len_total):
                pointerutils.check0(self._total_length_0)
                if self._total_ready[idx] == 0:
                    pointerutils.check1(self._total_length_0, idx)
                    pointerutils.check2(self._total_ready, idx)
                self.total[idx][0] = value[idx]
@cython.final
cdef class FluxSequences:
    cdef public double input
    cdef public int _input_ndim
    cdef public int _input_length
    cdef public bint _input_diskflag
    cdef public str _input_path
    cdef FILE *_input_file
    cdef public bint _input_ramflag
    cdef public double[:] _input_array
    cdef public bint _input_outputflag
    cdef double *_input_outputpointer
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
        if self._input_diskflag:
            self._input_file = fopen(str(self._input_path).encode(), "rb+")
            fseek(self._input_file, idx*8, SEEK_SET)
        if self._outputs_diskflag:
            self._outputs_file = fopen(str(self._outputs_path).encode(), "rb+")
            fseek(self._outputs_file, idx*self._outputs_length*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._input_diskflag:
            fclose(self._input_file)
        if self._outputs_diskflag:
            fclose(self._outputs_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._input_diskflag:
            fread(&self.input, 8, 1, self._input_file)
        elif self._input_ramflag:
            self.input = self._input_array[idx]
        if self._outputs_diskflag:
            fread(&self.outputs[0], 8, self._outputs_length, self._outputs_file)
        elif self._outputs_ramflag:
            for jdx0 in range(self._outputs_length_0):
                self.outputs[jdx0] = self._outputs_array[idx, jdx0]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._input_diskflag:
            fwrite(&self.input, 8, 1, self._input_file)
        elif self._input_ramflag:
            self._input_array[idx] = self.input
        if self._outputs_diskflag:
            fwrite(&self.outputs[0], 8, self._outputs_length, self._outputs_file)
        elif self._outputs_ramflag:
            for jdx0 in range(self._outputs_length_0):
                self._outputs_array[idx, jdx0] = self.outputs[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "input":
            self._input_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._input_outputflag:
            self._input_outputpointer[0] = self.input
@cython.final
cdef class OutletSequences:
    cdef double **branched
    cdef public int len_branched
    cdef public numpy.int32_t[:] _branched_ready
    cdef public int _branched_ndim
    cdef public int _branched_length
    cdef public int _branched_length_0
    cpdef inline alloc(self, name, numpy.int32_t length):
        if name == "branched":
            self._branched_length_0 = length
            self._branched_ready = numpy.full(length, 0, dtype=numpy.int32)
            self.branched = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc(self, name):
        if name == "branched":
            PyMem_Free(self.branched)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, int idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "branched":
            self.branched[idx] = pointer.p_value
            self._branched_ready[idx] = 1
    cpdef get_value(self, str name):
        cdef int idx
        if name == "branched":
            values = numpy.empty(self.len_branched)
            for idx in range(self.len_branched):
                pointerutils.check0(self._branched_length_0)
                if self._branched_ready[idx] == 0:
                    pointerutils.check1(self._branched_length_0, idx)
                    pointerutils.check2(self._branched_ready, idx)
                values[idx] = self.branched[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "branched":
            for idx in range(self.len_branched):
                pointerutils.check0(self._branched_length_0)
                if self._branched_ready[idx] == 0:
                    pointerutils.check1(self._branched_length_0, idx)
                    pointerutils.check2(self._branched_ready, idx)
                self.branched[idx][0] = value[idx]


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
        self.calc_outputs_v1()
    cpdef inline void update_inlets(self) nogil:
        self.pick_input_v1()
    cpdef inline void update_outlets(self) nogil:
        self.pass_outputs_v1()
    cpdef inline void update_receivers(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_senders(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_outputs(self) nogil:
        self.sequences.fluxes.update_outputs()

    cpdef inline void pick_input_v1(self)  nogil:
        cdef int idx
        self.sequences.fluxes.input = 0.0
        for idx in range(self.sequences.inlets.len_total):
            self.sequences.fluxes.input = self.sequences.fluxes.input + (self.sequences.inlets.total[idx][0])
    cpdef inline void pick_input(self)  nogil:
        cdef int idx
        self.sequences.fluxes.input = 0.0
        for idx in range(self.sequences.inlets.len_total):
            self.sequences.fluxes.input = self.sequences.fluxes.input + (self.sequences.inlets.total[idx][0])
    cpdef inline void calc_outputs_v1(self)  nogil:
        cdef int bdx
        cdef int pdx
        for pdx in range(1, self.parameters.derived.nmbpoints):
            if self.parameters.control.xpoints[pdx] > self.sequences.fluxes.input:
                break
        for bdx in range(self.parameters.derived.nmbbranches):
            self.sequences.fluxes.outputs[bdx] = (self.sequences.fluxes.input - self.parameters.control.xpoints[pdx - 1]) * (                self.parameters.control.ypoints[bdx, pdx] - self.parameters.control.ypoints[bdx, pdx - 1]            ) / (self.parameters.control.xpoints[pdx] - self.parameters.control.xpoints[pdx - 1]) + self.parameters.control.ypoints[bdx, pdx - 1]
    cpdef inline void calc_outputs(self)  nogil:
        cdef int bdx
        cdef int pdx
        for pdx in range(1, self.parameters.derived.nmbpoints):
            if self.parameters.control.xpoints[pdx] > self.sequences.fluxes.input:
                break
        for bdx in range(self.parameters.derived.nmbbranches):
            self.sequences.fluxes.outputs[bdx] = (self.sequences.fluxes.input - self.parameters.control.xpoints[pdx - 1]) * (                self.parameters.control.ypoints[bdx, pdx] - self.parameters.control.ypoints[bdx, pdx - 1]            ) / (self.parameters.control.xpoints[pdx] - self.parameters.control.xpoints[pdx - 1]) + self.parameters.control.ypoints[bdx, pdx - 1]
    cpdef inline void pass_outputs_v1(self)  nogil:
        cdef int bdx
        for bdx in range(self.parameters.derived.nmbbranches):
            self.sequences.outlets.branched[bdx][0] = self.sequences.outlets.branched[bdx][0] + (self.sequences.fluxes.outputs[bdx])
    cpdef inline void pass_outputs(self)  nogil:
        cdef int bdx
        for bdx in range(self.parameters.derived.nmbbranches):
            self.sequences.outlets.branched[bdx][0] = self.sequences.outlets.branched[bdx][0] + (self.sequences.fluxes.outputs[bdx])
