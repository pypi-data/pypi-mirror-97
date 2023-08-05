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
    cdef public double[:] inputheights
    cdef public double[:] outputheights
    cdef public numpy.int32_t maxnmbinputs
    cdef public numpy.int32_t minnmbinputs
    cdef public double defaultconstant
    cdef public double defaultfactor
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
    cdef public double actualconstant
    cdef public int _actualconstant_ndim
    cdef public int _actualconstant_length
    cdef public bint _actualconstant_diskflag
    cdef public str _actualconstant_path
    cdef FILE *_actualconstant_file
    cdef public bint _actualconstant_ramflag
    cdef public double[:] _actualconstant_array
    cdef public bint _actualconstant_outputflag
    cdef double *_actualconstant_outputpointer
    cdef public double actualfactor
    cdef public int _actualfactor_ndim
    cdef public int _actualfactor_length
    cdef public bint _actualfactor_diskflag
    cdef public str _actualfactor_path
    cdef FILE *_actualfactor_file
    cdef public bint _actualfactor_ramflag
    cdef public double[:] _actualfactor_array
    cdef public bint _actualfactor_outputflag
    cdef double *_actualfactor_outputpointer
    cdef public double[:] inputpredictions
    cdef public int _inputpredictions_ndim
    cdef public int _inputpredictions_length
    cdef public int _inputpredictions_length_0
    cdef public bint _inputpredictions_diskflag
    cdef public str _inputpredictions_path
    cdef FILE *_inputpredictions_file
    cdef public bint _inputpredictions_ramflag
    cdef public double[:,:] _inputpredictions_array
    cdef public bint _inputpredictions_outputflag
    cdef double *_inputpredictions_outputpointer
    cdef public double[:] outputpredictions
    cdef public int _outputpredictions_ndim
    cdef public int _outputpredictions_length
    cdef public int _outputpredictions_length_0
    cdef public bint _outputpredictions_diskflag
    cdef public str _outputpredictions_path
    cdef FILE *_outputpredictions_file
    cdef public bint _outputpredictions_ramflag
    cdef public double[:,:] _outputpredictions_array
    cdef public bint _outputpredictions_outputflag
    cdef double *_outputpredictions_outputpointer
    cdef public double[:] inputresiduals
    cdef public int _inputresiduals_ndim
    cdef public int _inputresiduals_length
    cdef public int _inputresiduals_length_0
    cdef public bint _inputresiduals_diskflag
    cdef public str _inputresiduals_path
    cdef FILE *_inputresiduals_file
    cdef public bint _inputresiduals_ramflag
    cdef public double[:,:] _inputresiduals_array
    cdef public bint _inputresiduals_outputflag
    cdef double *_inputresiduals_outputpointer
    cdef public double[:] outputresiduals
    cdef public int _outputresiduals_ndim
    cdef public int _outputresiduals_length
    cdef public int _outputresiduals_length_0
    cdef public bint _outputresiduals_diskflag
    cdef public str _outputresiduals_path
    cdef FILE *_outputresiduals_file
    cdef public bint _outputresiduals_ramflag
    cdef public double[:,:] _outputresiduals_array
    cdef public bint _outputresiduals_outputflag
    cdef double *_outputresiduals_outputpointer
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
        if self._actualconstant_diskflag:
            self._actualconstant_file = fopen(str(self._actualconstant_path).encode(), "rb+")
            fseek(self._actualconstant_file, idx*8, SEEK_SET)
        if self._actualfactor_diskflag:
            self._actualfactor_file = fopen(str(self._actualfactor_path).encode(), "rb+")
            fseek(self._actualfactor_file, idx*8, SEEK_SET)
        if self._inputpredictions_diskflag:
            self._inputpredictions_file = fopen(str(self._inputpredictions_path).encode(), "rb+")
            fseek(self._inputpredictions_file, idx*self._inputpredictions_length*8, SEEK_SET)
        if self._outputpredictions_diskflag:
            self._outputpredictions_file = fopen(str(self._outputpredictions_path).encode(), "rb+")
            fseek(self._outputpredictions_file, idx*self._outputpredictions_length*8, SEEK_SET)
        if self._inputresiduals_diskflag:
            self._inputresiduals_file = fopen(str(self._inputresiduals_path).encode(), "rb+")
            fseek(self._inputresiduals_file, idx*self._inputresiduals_length*8, SEEK_SET)
        if self._outputresiduals_diskflag:
            self._outputresiduals_file = fopen(str(self._outputresiduals_path).encode(), "rb+")
            fseek(self._outputresiduals_file, idx*self._outputresiduals_length*8, SEEK_SET)
        if self._outputs_diskflag:
            self._outputs_file = fopen(str(self._outputs_path).encode(), "rb+")
            fseek(self._outputs_file, idx*self._outputs_length*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._inputs_diskflag:
            fclose(self._inputs_file)
        if self._actualconstant_diskflag:
            fclose(self._actualconstant_file)
        if self._actualfactor_diskflag:
            fclose(self._actualfactor_file)
        if self._inputpredictions_diskflag:
            fclose(self._inputpredictions_file)
        if self._outputpredictions_diskflag:
            fclose(self._outputpredictions_file)
        if self._inputresiduals_diskflag:
            fclose(self._inputresiduals_file)
        if self._outputresiduals_diskflag:
            fclose(self._outputresiduals_file)
        if self._outputs_diskflag:
            fclose(self._outputs_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._inputs_diskflag:
            fread(&self.inputs[0], 8, self._inputs_length, self._inputs_file)
        elif self._inputs_ramflag:
            for jdx0 in range(self._inputs_length_0):
                self.inputs[jdx0] = self._inputs_array[idx, jdx0]
        if self._actualconstant_diskflag:
            fread(&self.actualconstant, 8, 1, self._actualconstant_file)
        elif self._actualconstant_ramflag:
            self.actualconstant = self._actualconstant_array[idx]
        if self._actualfactor_diskflag:
            fread(&self.actualfactor, 8, 1, self._actualfactor_file)
        elif self._actualfactor_ramflag:
            self.actualfactor = self._actualfactor_array[idx]
        if self._inputpredictions_diskflag:
            fread(&self.inputpredictions[0], 8, self._inputpredictions_length, self._inputpredictions_file)
        elif self._inputpredictions_ramflag:
            for jdx0 in range(self._inputpredictions_length_0):
                self.inputpredictions[jdx0] = self._inputpredictions_array[idx, jdx0]
        if self._outputpredictions_diskflag:
            fread(&self.outputpredictions[0], 8, self._outputpredictions_length, self._outputpredictions_file)
        elif self._outputpredictions_ramflag:
            for jdx0 in range(self._outputpredictions_length_0):
                self.outputpredictions[jdx0] = self._outputpredictions_array[idx, jdx0]
        if self._inputresiduals_diskflag:
            fread(&self.inputresiduals[0], 8, self._inputresiduals_length, self._inputresiduals_file)
        elif self._inputresiduals_ramflag:
            for jdx0 in range(self._inputresiduals_length_0):
                self.inputresiduals[jdx0] = self._inputresiduals_array[idx, jdx0]
        if self._outputresiduals_diskflag:
            fread(&self.outputresiduals[0], 8, self._outputresiduals_length, self._outputresiduals_file)
        elif self._outputresiduals_ramflag:
            for jdx0 in range(self._outputresiduals_length_0):
                self.outputresiduals[jdx0] = self._outputresiduals_array[idx, jdx0]
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
        if self._actualconstant_diskflag:
            fwrite(&self.actualconstant, 8, 1, self._actualconstant_file)
        elif self._actualconstant_ramflag:
            self._actualconstant_array[idx] = self.actualconstant
        if self._actualfactor_diskflag:
            fwrite(&self.actualfactor, 8, 1, self._actualfactor_file)
        elif self._actualfactor_ramflag:
            self._actualfactor_array[idx] = self.actualfactor
        if self._inputpredictions_diskflag:
            fwrite(&self.inputpredictions[0], 8, self._inputpredictions_length, self._inputpredictions_file)
        elif self._inputpredictions_ramflag:
            for jdx0 in range(self._inputpredictions_length_0):
                self._inputpredictions_array[idx, jdx0] = self.inputpredictions[jdx0]
        if self._outputpredictions_diskflag:
            fwrite(&self.outputpredictions[0], 8, self._outputpredictions_length, self._outputpredictions_file)
        elif self._outputpredictions_ramflag:
            for jdx0 in range(self._outputpredictions_length_0):
                self._outputpredictions_array[idx, jdx0] = self.outputpredictions[jdx0]
        if self._inputresiduals_diskflag:
            fwrite(&self.inputresiduals[0], 8, self._inputresiduals_length, self._inputresiduals_file)
        elif self._inputresiduals_ramflag:
            for jdx0 in range(self._inputresiduals_length_0):
                self._inputresiduals_array[idx, jdx0] = self.inputresiduals[jdx0]
        if self._outputresiduals_diskflag:
            fwrite(&self.outputresiduals[0], 8, self._outputresiduals_length, self._outputresiduals_file)
        elif self._outputresiduals_ramflag:
            for jdx0 in range(self._outputresiduals_length_0):
                self._outputresiduals_array[idx, jdx0] = self.outputresiduals[jdx0]
        if self._outputs_diskflag:
            fwrite(&self.outputs[0], 8, self._outputs_length, self._outputs_file)
        elif self._outputs_ramflag:
            for jdx0 in range(self._outputs_length_0):
                self._outputs_array[idx, jdx0] = self.outputs[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "actualconstant":
            self._actualconstant_outputpointer = value.p_value
        if name == "actualfactor":
            self._actualfactor_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._actualconstant_outputflag:
            self._actualconstant_outputpointer[0] = self.actualconstant
        if self._actualfactor_outputflag:
            self._actualfactor_outputpointer[0] = self.actualfactor
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
        self.calc_actualconstant_actualfactor_v1()
        self.calc_inputpredictions_v1()
        self.calc_outputpredictions_v1()
        self.calc_inputresiduals_v1()
        self.calc_outputresiduals_v1()
        self.calc_outputs_v3()
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
        self.sequences.fluxes.update_outputs()

    cpdef inline void pick_inputs_v1(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputs[idx] = self.sequences.inlets.inputs[idx][0]
    cpdef inline void pick_inputs(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputs[idx] = self.sequences.inlets.inputs[idx][0]
    cpdef inline void calc_actualconstant_actualfactor_v1(self)  nogil:
        cdef double d_temp
        cdef double d_denominator
        cdef double d_nominator
        cdef double d_mean_inputs
        cdef double d_mean_height
        cdef int idx
        cdef int counter
        counter = 0
        for idx in range(self.parameters.derived.nmbinputs):
            if not isnan(self.sequences.fluxes.inputs[idx]):
                counter = counter + (1)
                if counter == self.parameters.control.minnmbinputs:
                    break
        else:
            self.sequences.fluxes.actualfactor = self.parameters.control.defaultfactor
            self.sequences.fluxes.actualconstant = self.parameters.control.defaultconstant
            return
        d_mean_height = self.return_mean_v1(            self.parameters.control.inputheights, self.sequences.fluxes.inputs, self.parameters.derived.nmbinputs        )
        d_mean_inputs = self.return_mean_v1(self.sequences.fluxes.inputs, self.sequences.fluxes.inputs, self.parameters.derived.nmbinputs)
        d_nominator = 0.0
        d_denominator = 0.0
        for idx in range(self.parameters.derived.nmbinputs):
            if not isnan(self.sequences.fluxes.inputs[idx]):
                d_temp = self.parameters.control.inputheights[idx] - d_mean_height
                d_nominator = d_nominator + (d_temp * (self.sequences.fluxes.inputs[idx] - d_mean_inputs))
                d_denominator = d_denominator + (d_temp * d_temp)
        if d_denominator > 0.0:
            self.sequences.fluxes.actualfactor = d_nominator / d_denominator
            self.sequences.fluxes.actualconstant = d_mean_inputs - self.sequences.fluxes.actualfactor * d_mean_height
        else:
            self.sequences.fluxes.actualfactor = self.parameters.control.defaultfactor
            self.sequences.fluxes.actualconstant = self.parameters.control.defaultconstant
        return
    cpdef inline void calc_inputpredictions_v1(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputpredictions[idx] = (                self.sequences.fluxes.actualconstant + self.sequences.fluxes.actualfactor * self.parameters.control.inputheights[idx]            )
    cpdef inline void calc_outputpredictions_v1(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmboutputs):
            self.sequences.fluxes.outputpredictions[idx] = (                self.sequences.fluxes.actualconstant + self.sequences.fluxes.actualfactor * self.parameters.control.outputheights[idx]            )
    cpdef inline void calc_inputresiduals_v1(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputresiduals[idx] = self.sequences.fluxes.inputs[idx] - self.sequences.fluxes.inputpredictions[idx]
    cpdef inline void calc_outputresiduals_v1(self)  nogil:
        self.interpolate_inversedistance_v1(self.sequences.fluxes.inputresiduals, self.sequences.fluxes.outputresiduals)
    cpdef inline void calc_outputs_v3(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmboutputs):
            self.sequences.fluxes.outputs[idx] = self.sequences.fluxes.outputpredictions[idx] + self.sequences.fluxes.outputresiduals[idx]
    cpdef inline void calc_actualconstant_actualfactor(self)  nogil:
        cdef double d_temp
        cdef double d_denominator
        cdef double d_nominator
        cdef double d_mean_inputs
        cdef double d_mean_height
        cdef int idx
        cdef int counter
        counter = 0
        for idx in range(self.parameters.derived.nmbinputs):
            if not isnan(self.sequences.fluxes.inputs[idx]):
                counter = counter + (1)
                if counter == self.parameters.control.minnmbinputs:
                    break
        else:
            self.sequences.fluxes.actualfactor = self.parameters.control.defaultfactor
            self.sequences.fluxes.actualconstant = self.parameters.control.defaultconstant
            return
        d_mean_height = self.return_mean_v1(            self.parameters.control.inputheights, self.sequences.fluxes.inputs, self.parameters.derived.nmbinputs        )
        d_mean_inputs = self.return_mean_v1(self.sequences.fluxes.inputs, self.sequences.fluxes.inputs, self.parameters.derived.nmbinputs)
        d_nominator = 0.0
        d_denominator = 0.0
        for idx in range(self.parameters.derived.nmbinputs):
            if not isnan(self.sequences.fluxes.inputs[idx]):
                d_temp = self.parameters.control.inputheights[idx] - d_mean_height
                d_nominator = d_nominator + (d_temp * (self.sequences.fluxes.inputs[idx] - d_mean_inputs))
                d_denominator = d_denominator + (d_temp * d_temp)
        if d_denominator > 0.0:
            self.sequences.fluxes.actualfactor = d_nominator / d_denominator
            self.sequences.fluxes.actualconstant = d_mean_inputs - self.sequences.fluxes.actualfactor * d_mean_height
        else:
            self.sequences.fluxes.actualfactor = self.parameters.control.defaultfactor
            self.sequences.fluxes.actualconstant = self.parameters.control.defaultconstant
        return
    cpdef inline void calc_inputpredictions(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputpredictions[idx] = (                self.sequences.fluxes.actualconstant + self.sequences.fluxes.actualfactor * self.parameters.control.inputheights[idx]            )
    cpdef inline void calc_outputpredictions(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmboutputs):
            self.sequences.fluxes.outputpredictions[idx] = (                self.sequences.fluxes.actualconstant + self.sequences.fluxes.actualfactor * self.parameters.control.outputheights[idx]            )
    cpdef inline void calc_inputresiduals(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmbinputs):
            self.sequences.fluxes.inputresiduals[idx] = self.sequences.fluxes.inputs[idx] - self.sequences.fluxes.inputpredictions[idx]
    cpdef inline void calc_outputresiduals(self)  nogil:
        self.interpolate_inversedistance_v1(self.sequences.fluxes.inputresiduals, self.sequences.fluxes.outputresiduals)
    cpdef inline void calc_outputs(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmboutputs):
            self.sequences.fluxes.outputs[idx] = self.sequences.fluxes.outputpredictions[idx] + self.sequences.fluxes.outputresiduals[idx]
    cpdef inline double return_mean_v1(self, double[:] values, double[:] mask, numpy.int32_t number)  nogil:
        cdef int idx
        cdef double d_result
        cdef int counter
        counter = 0
        d_result = 0.0
        for idx in range(number):
            if not isnan(mask[idx]):
                counter = counter + (1)
                d_result = d_result + (values[idx])
        if counter > 0:
            return d_result / counter
        return nan
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
    cpdef inline double return_mean(self, double[:] values, double[:] mask, numpy.int32_t number)  nogil:
        cdef int idx
        cdef double d_result
        cdef int counter
        counter = 0
        d_result = 0.0
        for idx in range(number):
            if not isnan(mask[idx]):
                counter = counter + (1)
                d_result = d_result + (values[idx])
        if counter > 0:
            return d_result / counter
        return nan
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
