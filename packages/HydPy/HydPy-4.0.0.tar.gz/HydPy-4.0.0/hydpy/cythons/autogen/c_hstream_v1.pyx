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
    cdef public double lag
    cdef public double damp
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int32_t nmbsegments
    cdef public double c1
    cdef public double c3
    cdef public double c2
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public StateSequences states
    cdef public OutletSequences outlets
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InletSequences:
    cdef double **q
    cdef public int len_q
    cdef public numpy.int32_t[:] _q_ready
    cdef public int _q_ndim
    cdef public int _q_length
    cdef public int _q_length_0
    cpdef inline alloc(self, name, numpy.int32_t length):
        if name == "q":
            self._q_length_0 = length
            self._q_ready = numpy.full(length, 0, dtype=numpy.int32)
            self.q = <double**> PyMem_Malloc(length * sizeof(double*))
    cpdef inline dealloc(self, name):
        if name == "q":
            PyMem_Free(self.q)
    cpdef inline set_pointer1d(self, str name, pointerutils.Double value, int idx):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "q":
            self.q[idx] = pointer.p_value
            self._q_ready[idx] = 1
    cpdef get_value(self, str name):
        cdef int idx
        if name == "q":
            values = numpy.empty(self.len_q)
            for idx in range(self.len_q):
                pointerutils.check0(self._q_length_0)
                if self._q_ready[idx] == 0:
                    pointerutils.check1(self._q_length_0, idx)
                    pointerutils.check2(self._q_ready, idx)
                values[idx] = self.q[idx][0]
            return values
    cpdef set_value(self, str name, value):
        if name == "q":
            for idx in range(self.len_q):
                pointerutils.check0(self._q_length_0)
                if self._q_ready[idx] == 0:
                    pointerutils.check1(self._q_length_0, idx)
                    pointerutils.check2(self._q_ready, idx)
                self.q[idx][0] = value[idx]
@cython.final
cdef class StateSequences:
    cdef public double[:] qjoints
    cdef public int _qjoints_ndim
    cdef public int _qjoints_length
    cdef public int _qjoints_length_0
    cdef public bint _qjoints_diskflag
    cdef public str _qjoints_path
    cdef FILE *_qjoints_file
    cdef public bint _qjoints_ramflag
    cdef public double[:,:] _qjoints_array
    cdef public bint _qjoints_outputflag
    cdef double *_qjoints_outputpointer
    cpdef open_files(self, int idx):
        if self._qjoints_diskflag:
            self._qjoints_file = fopen(str(self._qjoints_path).encode(), "rb+")
            fseek(self._qjoints_file, idx*self._qjoints_length*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._qjoints_diskflag:
            fclose(self._qjoints_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._qjoints_diskflag:
            fread(&self.qjoints[0], 8, self._qjoints_length, self._qjoints_file)
        elif self._qjoints_ramflag:
            for jdx0 in range(self._qjoints_length_0):
                self.qjoints[jdx0] = self._qjoints_array[idx, jdx0]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._qjoints_diskflag:
            fwrite(&self.qjoints[0], 8, self._qjoints_length, self._qjoints_file)
        elif self._qjoints_ramflag:
            for jdx0 in range(self._qjoints_length_0):
                self._qjoints_array[idx, jdx0] = self.qjoints[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) nogil:
        pass
@cython.final
cdef class OutletSequences:
    cdef double *q
    cdef public int _q_ndim
    cdef public int _q_length
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "q":
            self.q = pointer.p_value
    cpdef get_value(self, str name):
        cdef int idx
        if name == "q":
            return self.q[0]
    cpdef set_value(self, str name, value):
        if name == "q":
            self.q[0] = value


@cython.final
cdef class Model:
    cdef public int idx_sim
    cdef public Parameters parameters
    cdef public Sequences sequences
    cpdef inline void simulate(self, int idx)  nogil:
        self.idx_sim = idx
        self.update_inlets()
        self.run()
        self.new2old()
        self.update_outlets()
        self.update_outputs()
    cpdef inline void open_files(self):
        self.sequences.states.open_files(self.idx_sim)
    cpdef inline void close_files(self):
        self.sequences.states.close_files()
    cpdef inline void save_data(self, int idx) nogil:
        self.sequences.states.save_data(self.idx_sim)
    cpdef inline void new2old(self) nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        for jdx0 in range(self.sequences.states._qjoints_length_0):
            self.sequences.old_states.qjoints[jdx0] = self.sequences.new_states.qjoints[jdx0]
    cpdef inline void run(self) nogil:
        self.calc_qjoints_v1()
    cpdef inline void update_inlets(self) nogil:
        self.pick_q_v1()
    cpdef inline void update_outlets(self) nogil:
        self.pass_q_v1()
    cpdef inline void update_receivers(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_senders(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_outputs(self) nogil:
        pass

    cpdef inline void pick_q_v1(self)  nogil:
        cdef int idx
        self.sequences.new_states.qjoints[0] = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.new_states.qjoints[0] = self.sequences.new_states.qjoints[0] + (self.sequences.inlets.q[idx][0])
    cpdef inline void pick_q(self)  nogil:
        cdef int idx
        self.sequences.new_states.qjoints[0] = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.new_states.qjoints[0] = self.sequences.new_states.qjoints[0] + (self.sequences.inlets.q[idx][0])
    cpdef inline void calc_qjoints_v1(self)  nogil:
        cdef int j
        for j in range(self.parameters.derived.nmbsegments):
            self.sequences.new_states.qjoints[j + 1] = (                self.parameters.derived.c1 * self.sequences.new_states.qjoints[j]                + self.parameters.derived.c2 * self.sequences.old_states.qjoints[j]                + self.parameters.derived.c3 * self.sequences.old_states.qjoints[j + 1]            )
    cpdef inline void calc_qjoints(self)  nogil:
        cdef int j
        for j in range(self.parameters.derived.nmbsegments):
            self.sequences.new_states.qjoints[j + 1] = (                self.parameters.derived.c1 * self.sequences.new_states.qjoints[j]                + self.parameters.derived.c2 * self.sequences.old_states.qjoints[j]                + self.parameters.derived.c3 * self.sequences.old_states.qjoints[j + 1]            )
    cpdef inline void pass_q_v1(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.new_states.qjoints[self.parameters.derived.nmbsegments])
    cpdef inline void pass_q(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.new_states.qjoints[self.parameters.derived.nmbsegments])
