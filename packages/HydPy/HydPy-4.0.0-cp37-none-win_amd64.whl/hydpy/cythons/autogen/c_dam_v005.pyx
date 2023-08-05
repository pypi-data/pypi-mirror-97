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
    cdef public SolverParameters solver
@cython.final
cdef class ControlParameters:
    cdef public double catchmentarea
    cdef public numpy.int32_t nmblogentries
    cdef public double[:] remotedischargeminimum
    cdef public double[:] remotedischargesafety
    cdef public double[:] neardischargeminimumthreshold
    cdef public double[:] neardischargeminimumtolerance
    cdef public bint restricttargetedrelease
    cdef public double waterlevelminimumthreshold
    cdef public double waterlevelminimumtolerance
    cdef public double[:] highestremoterelieve
    cdef public double[:] waterlevelrelievethreshold
    cdef public double[:] waterlevelrelievetolerance
    cdef public double[:] highestremotesupply
    cdef public double[:] waterlevelsupplythreshold
    cdef public double[:] waterlevelsupplytolerance
    cdef public annutils.ANN watervolume2waterlevel
    cdef public annutils.SeasonalANN waterlevel2flooddischarge
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int32_t[:] toy
    cdef public double seconds
    cdef public double[:] remotedischargesmoothpar
    cdef public double[:] neardischargeminimumsmoothpar1
    cdef public double[:] neardischargeminimumsmoothpar2
    cdef public double waterlevelminimumsmoothpar
    cdef public double[:] waterlevelrelievesmoothpar
    cdef public double[:] waterlevelsupplysmoothpar
@cython.final
cdef class SolverParameters:
    cdef public double abserrormax
    cdef public double relerrormax
    cdef public double reldtmin
    cdef public double reldtmax
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public ReceiverSequences receivers
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public LogSequences logs
    cdef public AideSequences aides
    cdef public OutletSequences outlets
    cdef public SenderSequences senders
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InletSequences:
    cdef double *q
    cdef public int _q_ndim
    cdef public int _q_length
    cdef double *s
    cdef public int _s_ndim
    cdef public int _s_length
    cdef double *r
    cdef public int _r_ndim
    cdef public int _r_length
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "q":
            self.q = pointer.p_value
        if name == "s":
            self.s = pointer.p_value
        if name == "r":
            self.r = pointer.p_value
    cpdef get_value(self, str name):
        cdef int idx
        if name == "q":
            return self.q[0]
        if name == "s":
            return self.s[0]
        if name == "r":
            return self.r[0]
    cpdef set_value(self, str name, value):
        if name == "q":
            self.q[0] = value
        if name == "s":
            self.s[0] = value
        if name == "r":
            self.r[0] = value
@cython.final
cdef class ReceiverSequences:
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
cdef class FluxSequences:
    cdef public double inflow
    cdef public int _inflow_ndim
    cdef public int _inflow_length
    cdef public double[:] _inflow_points
    cdef public double[:] _inflow_results
    cdef public double[:] _inflow_integrals
    cdef public double _inflow_sum
    cdef public bint _inflow_diskflag
    cdef public str _inflow_path
    cdef FILE *_inflow_file
    cdef public bint _inflow_ramflag
    cdef public double[:] _inflow_array
    cdef public bint _inflow_outputflag
    cdef double *_inflow_outputpointer
    cdef public double totalremotedischarge
    cdef public int _totalremotedischarge_ndim
    cdef public int _totalremotedischarge_length
    cdef public bint _totalremotedischarge_diskflag
    cdef public str _totalremotedischarge_path
    cdef FILE *_totalremotedischarge_file
    cdef public bint _totalremotedischarge_ramflag
    cdef public double[:] _totalremotedischarge_array
    cdef public bint _totalremotedischarge_outputflag
    cdef double *_totalremotedischarge_outputpointer
    cdef public double naturalremotedischarge
    cdef public int _naturalremotedischarge_ndim
    cdef public int _naturalremotedischarge_length
    cdef public bint _naturalremotedischarge_diskflag
    cdef public str _naturalremotedischarge_path
    cdef FILE *_naturalremotedischarge_file
    cdef public bint _naturalremotedischarge_ramflag
    cdef public double[:] _naturalremotedischarge_array
    cdef public bint _naturalremotedischarge_outputflag
    cdef double *_naturalremotedischarge_outputpointer
    cdef public double remotedemand
    cdef public int _remotedemand_ndim
    cdef public int _remotedemand_length
    cdef public bint _remotedemand_diskflag
    cdef public str _remotedemand_path
    cdef FILE *_remotedemand_file
    cdef public bint _remotedemand_ramflag
    cdef public double[:] _remotedemand_array
    cdef public bint _remotedemand_outputflag
    cdef double *_remotedemand_outputpointer
    cdef public double remotefailure
    cdef public int _remotefailure_ndim
    cdef public int _remotefailure_length
    cdef public bint _remotefailure_diskflag
    cdef public str _remotefailure_path
    cdef FILE *_remotefailure_file
    cdef public bint _remotefailure_ramflag
    cdef public double[:] _remotefailure_array
    cdef public bint _remotefailure_outputflag
    cdef double *_remotefailure_outputpointer
    cdef public double requiredremoterelease
    cdef public int _requiredremoterelease_ndim
    cdef public int _requiredremoterelease_length
    cdef public bint _requiredremoterelease_diskflag
    cdef public str _requiredremoterelease_path
    cdef FILE *_requiredremoterelease_file
    cdef public bint _requiredremoterelease_ramflag
    cdef public double[:] _requiredremoterelease_array
    cdef public bint _requiredremoterelease_outputflag
    cdef double *_requiredremoterelease_outputpointer
    cdef public double allowedremoterelieve
    cdef public int _allowedremoterelieve_ndim
    cdef public int _allowedremoterelieve_length
    cdef public bint _allowedremoterelieve_diskflag
    cdef public str _allowedremoterelieve_path
    cdef FILE *_allowedremoterelieve_file
    cdef public bint _allowedremoterelieve_ramflag
    cdef public double[:] _allowedremoterelieve_array
    cdef public bint _allowedremoterelieve_outputflag
    cdef double *_allowedremoterelieve_outputpointer
    cdef public double requiredremotesupply
    cdef public int _requiredremotesupply_ndim
    cdef public int _requiredremotesupply_length
    cdef public bint _requiredremotesupply_diskflag
    cdef public str _requiredremotesupply_path
    cdef FILE *_requiredremotesupply_file
    cdef public bint _requiredremotesupply_ramflag
    cdef public double[:] _requiredremotesupply_array
    cdef public bint _requiredremotesupply_outputflag
    cdef double *_requiredremotesupply_outputpointer
    cdef public double requiredrelease
    cdef public int _requiredrelease_ndim
    cdef public int _requiredrelease_length
    cdef public bint _requiredrelease_diskflag
    cdef public str _requiredrelease_path
    cdef FILE *_requiredrelease_file
    cdef public bint _requiredrelease_ramflag
    cdef public double[:] _requiredrelease_array
    cdef public bint _requiredrelease_outputflag
    cdef double *_requiredrelease_outputpointer
    cdef public double targetedrelease
    cdef public int _targetedrelease_ndim
    cdef public int _targetedrelease_length
    cdef public bint _targetedrelease_diskflag
    cdef public str _targetedrelease_path
    cdef FILE *_targetedrelease_file
    cdef public bint _targetedrelease_ramflag
    cdef public double[:] _targetedrelease_array
    cdef public bint _targetedrelease_outputflag
    cdef double *_targetedrelease_outputpointer
    cdef public double actualrelease
    cdef public int _actualrelease_ndim
    cdef public int _actualrelease_length
    cdef public double[:] _actualrelease_points
    cdef public double[:] _actualrelease_results
    cdef public double[:] _actualrelease_integrals
    cdef public double _actualrelease_sum
    cdef public bint _actualrelease_diskflag
    cdef public str _actualrelease_path
    cdef FILE *_actualrelease_file
    cdef public bint _actualrelease_ramflag
    cdef public double[:] _actualrelease_array
    cdef public bint _actualrelease_outputflag
    cdef double *_actualrelease_outputpointer
    cdef public double missingremoterelease
    cdef public int _missingremoterelease_ndim
    cdef public int _missingremoterelease_length
    cdef public bint _missingremoterelease_diskflag
    cdef public str _missingremoterelease_path
    cdef FILE *_missingremoterelease_file
    cdef public bint _missingremoterelease_ramflag
    cdef public double[:] _missingremoterelease_array
    cdef public bint _missingremoterelease_outputflag
    cdef double *_missingremoterelease_outputpointer
    cdef public double flooddischarge
    cdef public int _flooddischarge_ndim
    cdef public int _flooddischarge_length
    cdef public double[:] _flooddischarge_points
    cdef public double[:] _flooddischarge_results
    cdef public double[:] _flooddischarge_integrals
    cdef public double _flooddischarge_sum
    cdef public bint _flooddischarge_diskflag
    cdef public str _flooddischarge_path
    cdef FILE *_flooddischarge_file
    cdef public bint _flooddischarge_ramflag
    cdef public double[:] _flooddischarge_array
    cdef public bint _flooddischarge_outputflag
    cdef double *_flooddischarge_outputpointer
    cdef public double outflow
    cdef public int _outflow_ndim
    cdef public int _outflow_length
    cdef public double[:] _outflow_points
    cdef public double[:] _outflow_results
    cdef public double[:] _outflow_integrals
    cdef public double _outflow_sum
    cdef public bint _outflow_diskflag
    cdef public str _outflow_path
    cdef FILE *_outflow_file
    cdef public bint _outflow_ramflag
    cdef public double[:] _outflow_array
    cdef public bint _outflow_outputflag
    cdef double *_outflow_outputpointer
    cpdef open_files(self, int idx):
        if self._inflow_diskflag:
            self._inflow_file = fopen(str(self._inflow_path).encode(), "rb+")
            fseek(self._inflow_file, idx*8, SEEK_SET)
        if self._totalremotedischarge_diskflag:
            self._totalremotedischarge_file = fopen(str(self._totalremotedischarge_path).encode(), "rb+")
            fseek(self._totalremotedischarge_file, idx*8, SEEK_SET)
        if self._naturalremotedischarge_diskflag:
            self._naturalremotedischarge_file = fopen(str(self._naturalremotedischarge_path).encode(), "rb+")
            fseek(self._naturalremotedischarge_file, idx*8, SEEK_SET)
        if self._remotedemand_diskflag:
            self._remotedemand_file = fopen(str(self._remotedemand_path).encode(), "rb+")
            fseek(self._remotedemand_file, idx*8, SEEK_SET)
        if self._remotefailure_diskflag:
            self._remotefailure_file = fopen(str(self._remotefailure_path).encode(), "rb+")
            fseek(self._remotefailure_file, idx*8, SEEK_SET)
        if self._requiredremoterelease_diskflag:
            self._requiredremoterelease_file = fopen(str(self._requiredremoterelease_path).encode(), "rb+")
            fseek(self._requiredremoterelease_file, idx*8, SEEK_SET)
        if self._allowedremoterelieve_diskflag:
            self._allowedremoterelieve_file = fopen(str(self._allowedremoterelieve_path).encode(), "rb+")
            fseek(self._allowedremoterelieve_file, idx*8, SEEK_SET)
        if self._requiredremotesupply_diskflag:
            self._requiredremotesupply_file = fopen(str(self._requiredremotesupply_path).encode(), "rb+")
            fseek(self._requiredremotesupply_file, idx*8, SEEK_SET)
        if self._requiredrelease_diskflag:
            self._requiredrelease_file = fopen(str(self._requiredrelease_path).encode(), "rb+")
            fseek(self._requiredrelease_file, idx*8, SEEK_SET)
        if self._targetedrelease_diskflag:
            self._targetedrelease_file = fopen(str(self._targetedrelease_path).encode(), "rb+")
            fseek(self._targetedrelease_file, idx*8, SEEK_SET)
        if self._actualrelease_diskflag:
            self._actualrelease_file = fopen(str(self._actualrelease_path).encode(), "rb+")
            fseek(self._actualrelease_file, idx*8, SEEK_SET)
        if self._missingremoterelease_diskflag:
            self._missingremoterelease_file = fopen(str(self._missingremoterelease_path).encode(), "rb+")
            fseek(self._missingremoterelease_file, idx*8, SEEK_SET)
        if self._flooddischarge_diskflag:
            self._flooddischarge_file = fopen(str(self._flooddischarge_path).encode(), "rb+")
            fseek(self._flooddischarge_file, idx*8, SEEK_SET)
        if self._outflow_diskflag:
            self._outflow_file = fopen(str(self._outflow_path).encode(), "rb+")
            fseek(self._outflow_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._inflow_diskflag:
            fclose(self._inflow_file)
        if self._totalremotedischarge_diskflag:
            fclose(self._totalremotedischarge_file)
        if self._naturalremotedischarge_diskflag:
            fclose(self._naturalremotedischarge_file)
        if self._remotedemand_diskflag:
            fclose(self._remotedemand_file)
        if self._remotefailure_diskflag:
            fclose(self._remotefailure_file)
        if self._requiredremoterelease_diskflag:
            fclose(self._requiredremoterelease_file)
        if self._allowedremoterelieve_diskflag:
            fclose(self._allowedremoterelieve_file)
        if self._requiredremotesupply_diskflag:
            fclose(self._requiredremotesupply_file)
        if self._requiredrelease_diskflag:
            fclose(self._requiredrelease_file)
        if self._targetedrelease_diskflag:
            fclose(self._targetedrelease_file)
        if self._actualrelease_diskflag:
            fclose(self._actualrelease_file)
        if self._missingremoterelease_diskflag:
            fclose(self._missingremoterelease_file)
        if self._flooddischarge_diskflag:
            fclose(self._flooddischarge_file)
        if self._outflow_diskflag:
            fclose(self._outflow_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._inflow_diskflag:
            fread(&self.inflow, 8, 1, self._inflow_file)
        elif self._inflow_ramflag:
            self.inflow = self._inflow_array[idx]
        if self._totalremotedischarge_diskflag:
            fread(&self.totalremotedischarge, 8, 1, self._totalremotedischarge_file)
        elif self._totalremotedischarge_ramflag:
            self.totalremotedischarge = self._totalremotedischarge_array[idx]
        if self._naturalremotedischarge_diskflag:
            fread(&self.naturalremotedischarge, 8, 1, self._naturalremotedischarge_file)
        elif self._naturalremotedischarge_ramflag:
            self.naturalremotedischarge = self._naturalremotedischarge_array[idx]
        if self._remotedemand_diskflag:
            fread(&self.remotedemand, 8, 1, self._remotedemand_file)
        elif self._remotedemand_ramflag:
            self.remotedemand = self._remotedemand_array[idx]
        if self._remotefailure_diskflag:
            fread(&self.remotefailure, 8, 1, self._remotefailure_file)
        elif self._remotefailure_ramflag:
            self.remotefailure = self._remotefailure_array[idx]
        if self._requiredremoterelease_diskflag:
            fread(&self.requiredremoterelease, 8, 1, self._requiredremoterelease_file)
        elif self._requiredremoterelease_ramflag:
            self.requiredremoterelease = self._requiredremoterelease_array[idx]
        if self._allowedremoterelieve_diskflag:
            fread(&self.allowedremoterelieve, 8, 1, self._allowedremoterelieve_file)
        elif self._allowedremoterelieve_ramflag:
            self.allowedremoterelieve = self._allowedremoterelieve_array[idx]
        if self._requiredremotesupply_diskflag:
            fread(&self.requiredremotesupply, 8, 1, self._requiredremotesupply_file)
        elif self._requiredremotesupply_ramflag:
            self.requiredremotesupply = self._requiredremotesupply_array[idx]
        if self._requiredrelease_diskflag:
            fread(&self.requiredrelease, 8, 1, self._requiredrelease_file)
        elif self._requiredrelease_ramflag:
            self.requiredrelease = self._requiredrelease_array[idx]
        if self._targetedrelease_diskflag:
            fread(&self.targetedrelease, 8, 1, self._targetedrelease_file)
        elif self._targetedrelease_ramflag:
            self.targetedrelease = self._targetedrelease_array[idx]
        if self._actualrelease_diskflag:
            fread(&self.actualrelease, 8, 1, self._actualrelease_file)
        elif self._actualrelease_ramflag:
            self.actualrelease = self._actualrelease_array[idx]
        if self._missingremoterelease_diskflag:
            fread(&self.missingremoterelease, 8, 1, self._missingremoterelease_file)
        elif self._missingremoterelease_ramflag:
            self.missingremoterelease = self._missingremoterelease_array[idx]
        if self._flooddischarge_diskflag:
            fread(&self.flooddischarge, 8, 1, self._flooddischarge_file)
        elif self._flooddischarge_ramflag:
            self.flooddischarge = self._flooddischarge_array[idx]
        if self._outflow_diskflag:
            fread(&self.outflow, 8, 1, self._outflow_file)
        elif self._outflow_ramflag:
            self.outflow = self._outflow_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._inflow_diskflag:
            fwrite(&self.inflow, 8, 1, self._inflow_file)
        elif self._inflow_ramflag:
            self._inflow_array[idx] = self.inflow
        if self._totalremotedischarge_diskflag:
            fwrite(&self.totalremotedischarge, 8, 1, self._totalremotedischarge_file)
        elif self._totalremotedischarge_ramflag:
            self._totalremotedischarge_array[idx] = self.totalremotedischarge
        if self._naturalremotedischarge_diskflag:
            fwrite(&self.naturalremotedischarge, 8, 1, self._naturalremotedischarge_file)
        elif self._naturalremotedischarge_ramflag:
            self._naturalremotedischarge_array[idx] = self.naturalremotedischarge
        if self._remotedemand_diskflag:
            fwrite(&self.remotedemand, 8, 1, self._remotedemand_file)
        elif self._remotedemand_ramflag:
            self._remotedemand_array[idx] = self.remotedemand
        if self._remotefailure_diskflag:
            fwrite(&self.remotefailure, 8, 1, self._remotefailure_file)
        elif self._remotefailure_ramflag:
            self._remotefailure_array[idx] = self.remotefailure
        if self._requiredremoterelease_diskflag:
            fwrite(&self.requiredremoterelease, 8, 1, self._requiredremoterelease_file)
        elif self._requiredremoterelease_ramflag:
            self._requiredremoterelease_array[idx] = self.requiredremoterelease
        if self._allowedremoterelieve_diskflag:
            fwrite(&self.allowedremoterelieve, 8, 1, self._allowedremoterelieve_file)
        elif self._allowedremoterelieve_ramflag:
            self._allowedremoterelieve_array[idx] = self.allowedremoterelieve
        if self._requiredremotesupply_diskflag:
            fwrite(&self.requiredremotesupply, 8, 1, self._requiredremotesupply_file)
        elif self._requiredremotesupply_ramflag:
            self._requiredremotesupply_array[idx] = self.requiredremotesupply
        if self._requiredrelease_diskflag:
            fwrite(&self.requiredrelease, 8, 1, self._requiredrelease_file)
        elif self._requiredrelease_ramflag:
            self._requiredrelease_array[idx] = self.requiredrelease
        if self._targetedrelease_diskflag:
            fwrite(&self.targetedrelease, 8, 1, self._targetedrelease_file)
        elif self._targetedrelease_ramflag:
            self._targetedrelease_array[idx] = self.targetedrelease
        if self._actualrelease_diskflag:
            fwrite(&self.actualrelease, 8, 1, self._actualrelease_file)
        elif self._actualrelease_ramflag:
            self._actualrelease_array[idx] = self.actualrelease
        if self._missingremoterelease_diskflag:
            fwrite(&self.missingremoterelease, 8, 1, self._missingremoterelease_file)
        elif self._missingremoterelease_ramflag:
            self._missingremoterelease_array[idx] = self.missingremoterelease
        if self._flooddischarge_diskflag:
            fwrite(&self.flooddischarge, 8, 1, self._flooddischarge_file)
        elif self._flooddischarge_ramflag:
            self._flooddischarge_array[idx] = self.flooddischarge
        if self._outflow_diskflag:
            fwrite(&self.outflow, 8, 1, self._outflow_file)
        elif self._outflow_ramflag:
            self._outflow_array[idx] = self.outflow
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "inflow":
            self._inflow_outputpointer = value.p_value
        if name == "totalremotedischarge":
            self._totalremotedischarge_outputpointer = value.p_value
        if name == "naturalremotedischarge":
            self._naturalremotedischarge_outputpointer = value.p_value
        if name == "remotedemand":
            self._remotedemand_outputpointer = value.p_value
        if name == "remotefailure":
            self._remotefailure_outputpointer = value.p_value
        if name == "requiredremoterelease":
            self._requiredremoterelease_outputpointer = value.p_value
        if name == "allowedremoterelieve":
            self._allowedremoterelieve_outputpointer = value.p_value
        if name == "requiredremotesupply":
            self._requiredremotesupply_outputpointer = value.p_value
        if name == "requiredrelease":
            self._requiredrelease_outputpointer = value.p_value
        if name == "targetedrelease":
            self._targetedrelease_outputpointer = value.p_value
        if name == "actualrelease":
            self._actualrelease_outputpointer = value.p_value
        if name == "missingremoterelease":
            self._missingremoterelease_outputpointer = value.p_value
        if name == "flooddischarge":
            self._flooddischarge_outputpointer = value.p_value
        if name == "outflow":
            self._outflow_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._inflow_outputflag:
            self._inflow_outputpointer[0] = self.inflow
        if self._totalremotedischarge_outputflag:
            self._totalremotedischarge_outputpointer[0] = self.totalremotedischarge
        if self._naturalremotedischarge_outputflag:
            self._naturalremotedischarge_outputpointer[0] = self.naturalremotedischarge
        if self._remotedemand_outputflag:
            self._remotedemand_outputpointer[0] = self.remotedemand
        if self._remotefailure_outputflag:
            self._remotefailure_outputpointer[0] = self.remotefailure
        if self._requiredremoterelease_outputflag:
            self._requiredremoterelease_outputpointer[0] = self.requiredremoterelease
        if self._allowedremoterelieve_outputflag:
            self._allowedremoterelieve_outputpointer[0] = self.allowedremoterelieve
        if self._requiredremotesupply_outputflag:
            self._requiredremotesupply_outputpointer[0] = self.requiredremotesupply
        if self._requiredrelease_outputflag:
            self._requiredrelease_outputpointer[0] = self.requiredrelease
        if self._targetedrelease_outputflag:
            self._targetedrelease_outputpointer[0] = self.targetedrelease
        if self._actualrelease_outputflag:
            self._actualrelease_outputpointer[0] = self.actualrelease
        if self._missingremoterelease_outputflag:
            self._missingremoterelease_outputpointer[0] = self.missingremoterelease
        if self._flooddischarge_outputflag:
            self._flooddischarge_outputpointer[0] = self.flooddischarge
        if self._outflow_outputflag:
            self._outflow_outputpointer[0] = self.outflow
@cython.final
cdef class StateSequences:
    cdef public double watervolume
    cdef public int _watervolume_ndim
    cdef public int _watervolume_length
    cdef public double[:] _watervolume_points
    cdef public double[:] _watervolume_results
    cdef public bint _watervolume_diskflag
    cdef public str _watervolume_path
    cdef FILE *_watervolume_file
    cdef public bint _watervolume_ramflag
    cdef public double[:] _watervolume_array
    cdef public bint _watervolume_outputflag
    cdef double *_watervolume_outputpointer
    cpdef open_files(self, int idx):
        if self._watervolume_diskflag:
            self._watervolume_file = fopen(str(self._watervolume_path).encode(), "rb+")
            fseek(self._watervolume_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._watervolume_diskflag:
            fclose(self._watervolume_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._watervolume_diskflag:
            fread(&self.watervolume, 8, 1, self._watervolume_file)
        elif self._watervolume_ramflag:
            self.watervolume = self._watervolume_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._watervolume_diskflag:
            fwrite(&self.watervolume, 8, 1, self._watervolume_file)
        elif self._watervolume_ramflag:
            self._watervolume_array[idx] = self.watervolume
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "watervolume":
            self._watervolume_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._watervolume_outputflag:
            self._watervolume_outputpointer[0] = self.watervolume
@cython.final
cdef class LogSequences:
    cdef public double[:] loggedtotalremotedischarge
    cdef public int _loggedtotalremotedischarge_ndim
    cdef public int _loggedtotalremotedischarge_length
    cdef public int _loggedtotalremotedischarge_length_0
    cdef public double[:] loggedoutflow
    cdef public int _loggedoutflow_ndim
    cdef public int _loggedoutflow_length
    cdef public int _loggedoutflow_length_0
@cython.final
cdef class AideSequences:
    cdef public double waterlevel
    cdef public int _waterlevel_ndim
    cdef public int _waterlevel_length
    cdef public double[:] _waterlevel_points
    cdef public double[:] _waterlevel_results
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
cdef class SenderSequences:
    cdef double *d
    cdef public int _d_ndim
    cdef public int _d_length
    cdef double *s
    cdef public int _s_ndim
    cdef public int _s_length
    cdef double *r
    cdef public int _r_ndim
    cdef public int _r_length
    cpdef inline set_pointer0d(self, str name, pointerutils.Double value):
        cdef pointerutils.PDouble pointer = pointerutils.PDouble(value)
        if name == "d":
            self.d = pointer.p_value
        if name == "s":
            self.s = pointer.p_value
        if name == "r":
            self.r = pointer.p_value
    cpdef get_value(self, str name):
        cdef int idx
        if name == "d":
            return self.d[0]
        if name == "s":
            return self.s[0]
        if name == "r":
            return self.r[0]
    cpdef set_value(self, str name, value):
        if name == "d":
            self.d[0] = value
        if name == "s":
            self.s[0] = value
        if name == "r":
            self.r[0] = value
@cython.final
cdef class NumConsts:
    cdef public numpy.int32_t nmb_methods
    cdef public numpy.int32_t nmb_stages
    cdef public double dt_increase
    cdef public double dt_decrease
    cdef public configutils.Config pub
    cdef public double[:, :, :] a_coefs
cdef class NumVars:
    cdef public bint use_relerror
    cdef public numpy.int32_t nmb_calls
    cdef public numpy.int32_t idx_method
    cdef public numpy.int32_t idx_stage
    cdef public double t0
    cdef public double t1
    cdef public double dt
    cdef public double dt_est
    cdef public double abserror
    cdef public double relerror
    cdef public double last_abserror
    cdef public double last_relerror
    cdef public double extrapolated_abserror
    cdef public double extrapolated_relerror
    cdef public bint f0_ready

@cython.final
cdef class Model:
    cdef public int idx_sim
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public NumConsts numconsts
    cdef public NumVars numvars
    cpdef inline void simulate(self, int idx)  nogil:
        self.idx_sim = idx
        self.update_inlets()
        self.solve()
        self.update_outlets()
        self.update_outputs()
    cpdef inline void open_files(self):
        self.sequences.fluxes.open_files(self.idx_sim)
        self.sequences.states.open_files(self.idx_sim)
    cpdef inline void close_files(self):
        self.sequences.fluxes.close_files()
        self.sequences.states.close_files()
    cpdef inline void save_data(self, int idx) nogil:
        self.sequences.fluxes.save_data(self.idx_sim)
        self.sequences.states.save_data(self.idx_sim)
    cpdef inline void new2old(self) nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        self.sequences.old_states.watervolume = self.sequences.new_states.watervolume
    cpdef inline void update_inlets(self) nogil:
        self.pic_inflow_v2()
        self.calc_naturalremotedischarge_v1()
        self.calc_remotedemand_v1()
        self.calc_remotefailure_v1()
        self.calc_requiredremoterelease_v1()
        self.calc_requiredrelease_v1()
        self.calc_targetedrelease_v1()
    cpdef inline void update_outlets(self) nogil:
        self.pass_outflow_v1()
        self.update_loggedoutflow_v1()
    cpdef inline void update_receivers(self, int idx) nogil:
        self.idx_sim = idx
        self.pic_totalremotedischarge_v1()
        self.update_loggedtotalremotedischarge_v1()
    cpdef inline void update_senders(self, int idx) nogil:
        self.idx_sim = idx
        self.calc_missingremoterelease_v1()
        self.pass_missingremoterelease_v1()
        self.calc_allowedremoterelieve_v2()
        self.pass_allowedremoterelieve_v1()
        self.calc_requiredremotesupply_v1()
        self.pass_requiredremotesupply_v1()
    cpdef inline void update_outputs(self) nogil:
        self.sequences.fluxes.update_outputs()
        self.sequences.states.update_outputs()
    cpdef inline void solve(self)  nogil:
        cdef int decrease_dt
        self.numvars.use_relerror = not isnan(            self.parameters.solver.relerrormax        )
        self.numvars.t0, self.numvars.t1 = 0.0, 1.0
        self.numvars.dt_est = 1.0 * self.parameters.solver.reldtmax
        self.numvars.f0_ready = False
        self.reset_sum_fluxes()
        while self.numvars.t0 < self.numvars.t1 - 1e-14:
            self.numvars.last_abserror = inf
            self.numvars.last_relerror = inf
            self.numvars.dt = min(                self.numvars.t1 - self.numvars.t0,                1.0 * self.parameters.solver.reldtmax,                max(self.numvars.dt_est, self.parameters.solver.reldtmin),            )
            if not self.numvars.f0_ready:
                self.calculate_single_terms()
                self.numvars.idx_method = 0
                self.numvars.idx_stage = 0
                self.set_point_fluxes()
                self.set_point_states()
                self.set_result_states()
            for self.numvars.idx_method in range(1, self.numconsts.nmb_methods + 1):
                for self.numvars.idx_stage in range(1, self.numvars.idx_method):
                    self.get_point_states()
                    self.calculate_single_terms()
                    self.set_point_fluxes()
                for self.numvars.idx_stage in range(1, self.numvars.idx_method + 1):
                    self.integrate_fluxes()
                    self.calculate_full_terms()
                    self.set_point_states()
                self.set_result_fluxes()
                self.set_result_states()
                self.calculate_error()
                self.extrapolate_error()
                if self.numvars.idx_method == 1:
                    continue
                if (self.numvars.abserror <= self.parameters.solver.abserrormax) or (                    self.numvars.relerror <= self.parameters.solver.relerrormax                ):
                    self.numvars.dt_est = self.numconsts.dt_increase * self.numvars.dt
                    self.numvars.f0_ready = False
                    self.addup_fluxes()
                    self.numvars.t0 = self.numvars.t0 + self.numvars.dt
                    self.new2old()
                    break
                decrease_dt = self.numvars.dt > self.parameters.solver.reldtmin
                decrease_dt = decrease_dt and (                    self.numvars.extrapolated_abserror                    > self.parameters.solver.abserrormax                )
                if self.numvars.use_relerror:
                    decrease_dt = decrease_dt and (                        self.numvars.extrapolated_relerror                        > self.parameters.solver.relerrormax                    )
                if decrease_dt:
                    self.numvars.f0_ready = True
                    self.numvars.dt_est = self.numvars.dt / self.numconsts.dt_decrease
                    break
                self.numvars.last_abserror = self.numvars.abserror
                self.numvars.last_relerror = self.numvars.relerror
                self.numvars.f0_ready = True
            else:
                if self.numvars.dt <= self.parameters.solver.reldtmin:
                    self.numvars.f0_ready = False
                    self.addup_fluxes()
                    self.numvars.t0 = self.numvars.t0 + self.numvars.dt
                    self.new2old()
                else:
                    self.numvars.f0_ready = True
                    self.numvars.dt_est = self.numvars.dt / self.numconsts.dt_decrease
        self.get_sum_fluxes()
    cpdef inline void calculate_single_terms(self) nogil:
        self.numvars.nmb_calls =self.numvars.nmb_calls+1
        self.pic_inflow_v2()
        self.calc_waterlevel_v1()
        self.calc_actualrelease_v1()
        self.calc_flooddischarge_v1()
        self.calc_outflow_v1()
    cpdef inline void calculate_full_terms(self) nogil:
        self.update_watervolume_v1()
    cpdef inline void get_point_states(self) nogil:
        self.sequences.states.watervolume = self.sequences.states._watervolume_points[self.numvars.idx_stage]
    cpdef inline void set_point_states(self) nogil:
        self.sequences.states._watervolume_points[self.numvars.idx_stage] = self.sequences.states.watervolume
    cpdef inline void set_result_states(self) nogil:
        self.sequences.states._watervolume_results[self.numvars.idx_method] = self.sequences.states.watervolume
    cpdef inline void get_sum_fluxes(self) nogil:
        self.sequences.fluxes.inflow = self.sequences.fluxes._inflow_sum
        self.sequences.fluxes.actualrelease = self.sequences.fluxes._actualrelease_sum
        self.sequences.fluxes.flooddischarge = self.sequences.fluxes._flooddischarge_sum
        self.sequences.fluxes.outflow = self.sequences.fluxes._outflow_sum
    cpdef inline void set_point_fluxes(self) nogil:
        self.sequences.fluxes._inflow_points[self.numvars.idx_stage] = self.sequences.fluxes.inflow
        self.sequences.fluxes._actualrelease_points[self.numvars.idx_stage] = self.sequences.fluxes.actualrelease
        self.sequences.fluxes._flooddischarge_points[self.numvars.idx_stage] = self.sequences.fluxes.flooddischarge
        self.sequences.fluxes._outflow_points[self.numvars.idx_stage] = self.sequences.fluxes.outflow
    cpdef inline void set_result_fluxes(self) nogil:
        self.sequences.fluxes._inflow_results[self.numvars.idx_method] = self.sequences.fluxes.inflow
        self.sequences.fluxes._actualrelease_results[self.numvars.idx_method] = self.sequences.fluxes.actualrelease
        self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method] = self.sequences.fluxes.flooddischarge
        self.sequences.fluxes._outflow_results[self.numvars.idx_method] = self.sequences.fluxes.outflow
    cpdef inline void integrate_fluxes(self) nogil:
        cdef int jdx
        self.sequences.fluxes.inflow = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.inflow = self.sequences.fluxes.inflow +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._inflow_points[jdx]
        self.sequences.fluxes.actualrelease = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.actualrelease = self.sequences.fluxes.actualrelease +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._actualrelease_points[jdx]
        self.sequences.fluxes.flooddischarge = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.flooddischarge = self.sequences.fluxes.flooddischarge +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._flooddischarge_points[jdx]
        self.sequences.fluxes.outflow = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.outflow = self.sequences.fluxes.outflow +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._outflow_points[jdx]
    cpdef inline void reset_sum_fluxes(self) nogil:
        self.sequences.fluxes._inflow_sum = 0.
        self.sequences.fluxes._actualrelease_sum = 0.
        self.sequences.fluxes._flooddischarge_sum = 0.
        self.sequences.fluxes._outflow_sum = 0.
    cpdef inline void addup_fluxes(self) nogil:
        self.sequences.fluxes._inflow_sum = self.sequences.fluxes._inflow_sum + self.sequences.fluxes.inflow
        self.sequences.fluxes._actualrelease_sum = self.sequences.fluxes._actualrelease_sum + self.sequences.fluxes.actualrelease
        self.sequences.fluxes._flooddischarge_sum = self.sequences.fluxes._flooddischarge_sum + self.sequences.fluxes.flooddischarge
        self.sequences.fluxes._outflow_sum = self.sequences.fluxes._outflow_sum + self.sequences.fluxes.outflow
    cpdef inline void calculate_error(self) nogil:
        cdef double abserror
        self.numvars.abserror = 0.
        if self.numvars.use_relerror:
            self.numvars.relerror = 0.
        else:
            self.numvars.relerror = inf
        abserror = fabs(self.sequences.fluxes._inflow_results[self.numvars.idx_method]-self.sequences.fluxes._inflow_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._inflow_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._inflow_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._actualrelease_results[self.numvars.idx_method]-self.sequences.fluxes._actualrelease_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._actualrelease_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._actualrelease_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method]-self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._flooddischarge_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._outflow_results[self.numvars.idx_method]-self.sequences.fluxes._outflow_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._outflow_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._outflow_results[self.numvars.idx_method]))
    cpdef inline void extrapolate_error(self)  nogil:
        if self.numvars.abserror <= 0.0:
            self.numvars.extrapolated_abserror = 0.0
            self.numvars.extrapolated_relerror = 0.0
        else:
            if self.numvars.idx_method > 2:
                self.numvars.extrapolated_abserror = exp(                    log(self.numvars.abserror)                    + (                        log(self.numvars.abserror)                        - log(self.numvars.last_abserror)                    )                    * (self.numconsts.nmb_methods - self.numvars.idx_method)                )
            else:
                self.numvars.extrapolated_abserror = -999.9
            if self.numvars.use_relerror:
                if self.numvars.idx_method > 2:
                    if isinf(self.numvars.relerror):
                        self.numvars.extrapolated_relerror = inf
                    else:
                        self.numvars.extrapolated_relerror = exp(                            log(self.numvars.relerror)                            + (                                log(self.numvars.relerror)                                - log(self.numvars.last_relerror)                            )                            * (self.numconsts.nmb_methods - self.numvars.idx_method)                        )
                else:
                    self.numvars.extrapolated_relerror = -999.9
            else:
                self.numvars.extrapolated_relerror = inf
    cpdef inline void pic_totalremotedischarge_v1(self)  nogil:
        self.sequences.fluxes.totalremotedischarge = self.sequences.receivers.q[0]
    cpdef inline void update_loggedtotalremotedischarge_v1(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.control.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedtotalremotedischarge[idx] = self.sequences.logs.loggedtotalremotedischarge[                idx - 1            ]
        self.sequences.logs.loggedtotalremotedischarge[0] = self.sequences.fluxes.totalremotedischarge
    cpdef inline void pic_totalremotedischarge(self)  nogil:
        self.sequences.fluxes.totalremotedischarge = self.sequences.receivers.q[0]
    cpdef inline void update_loggedtotalremotedischarge(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.control.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedtotalremotedischarge[idx] = self.sequences.logs.loggedtotalremotedischarge[                idx - 1            ]
        self.sequences.logs.loggedtotalremotedischarge[0] = self.sequences.fluxes.totalremotedischarge
    cpdef inline void pic_inflow_v2(self)  nogil:
        self.sequences.fluxes.inflow = self.sequences.inlets.q[0] + self.sequences.inlets.s[0] + self.sequences.inlets.r[0]
    cpdef inline void calc_naturalremotedischarge_v1(self)  nogil:
        cdef int idx
        self.sequences.fluxes.naturalremotedischarge = 0.0
        for idx in range(self.parameters.control.nmblogentries):
            self.sequences.fluxes.naturalremotedischarge = self.sequences.fluxes.naturalremotedischarge + ((                self.sequences.logs.loggedtotalremotedischarge[idx] - self.sequences.logs.loggedoutflow[idx]            ))
        if self.sequences.fluxes.naturalremotedischarge > 0.0:
            self.sequences.fluxes.naturalremotedischarge = self.sequences.fluxes.naturalremotedischarge / (self.parameters.control.nmblogentries)
        else:
            self.sequences.fluxes.naturalremotedischarge = 0.0
    cpdef inline void calc_remotedemand_v1(self)  nogil:
        self.sequences.fluxes.remotedemand = max(            self.parameters.control.remotedischargeminimum[self.parameters.derived.toy[self.idx_sim]]            - self.sequences.fluxes.naturalremotedischarge,            0.0,        )
    cpdef inline void calc_remotefailure_v1(self)  nogil:
        cdef int idx
        self.sequences.fluxes.remotefailure = 0
        for idx in range(self.parameters.control.nmblogentries):
            self.sequences.fluxes.remotefailure = self.sequences.fluxes.remotefailure - (self.sequences.logs.loggedtotalremotedischarge[idx])
        self.sequences.fluxes.remotefailure = self.sequences.fluxes.remotefailure / (self.parameters.control.nmblogentries)
        self.sequences.fluxes.remotefailure = self.sequences.fluxes.remotefailure + (self.parameters.control.remotedischargeminimum[self.parameters.derived.toy[self.idx_sim]])
    cpdef inline void calc_requiredremoterelease_v1(self)  nogil:
        self.sequences.fluxes.requiredremoterelease = self.sequences.fluxes.remotedemand + self.parameters.control.remotedischargesafety[            self.parameters.derived.toy[self.idx_sim]        ] * smoothutils.smooth_logistic1(            self.sequences.fluxes.remotefailure, self.parameters.derived.remotedischargesmoothpar[self.parameters.derived.toy[self.idx_sim]]        )
    cpdef inline void calc_requiredrelease_v1(self)  nogil:
        self.sequences.fluxes.requiredrelease = self.parameters.control.neardischargeminimumthreshold[self.parameters.derived.toy[self.idx_sim]]
        self.sequences.fluxes.requiredrelease = self.sequences.fluxes.requiredrelease + smoothutils.smooth_logistic2(            self.sequences.fluxes.requiredremoterelease - self.sequences.fluxes.requiredrelease,            self.parameters.derived.neardischargeminimumsmoothpar2[self.parameters.derived.toy[self.idx_sim]],        )
    cpdef inline void calc_targetedrelease_v1(self)  nogil:
        if self.parameters.control.restricttargetedrelease:
            self.sequences.fluxes.targetedrelease = smoothutils.smooth_logistic1(                self.sequences.fluxes.inflow - self.parameters.control.neardischargeminimumthreshold[self.parameters.derived.toy[self.idx_sim]],                self.parameters.derived.neardischargeminimumsmoothpar1[self.parameters.derived.toy[self.idx_sim]],            )
            self.sequences.fluxes.targetedrelease = (                self.sequences.fluxes.targetedrelease * self.sequences.fluxes.requiredrelease                + (1.0 - self.sequences.fluxes.targetedrelease) * self.sequences.fluxes.inflow            )
        else:
            self.sequences.fluxes.targetedrelease = self.sequences.fluxes.requiredrelease
    cpdef inline void pic_inflow(self)  nogil:
        self.sequences.fluxes.inflow = self.sequences.inlets.q[0] + self.sequences.inlets.s[0] + self.sequences.inlets.r[0]
    cpdef inline void calc_naturalremotedischarge(self)  nogil:
        cdef int idx
        self.sequences.fluxes.naturalremotedischarge = 0.0
        for idx in range(self.parameters.control.nmblogentries):
            self.sequences.fluxes.naturalremotedischarge = self.sequences.fluxes.naturalremotedischarge + ((                self.sequences.logs.loggedtotalremotedischarge[idx] - self.sequences.logs.loggedoutflow[idx]            ))
        if self.sequences.fluxes.naturalremotedischarge > 0.0:
            self.sequences.fluxes.naturalremotedischarge = self.sequences.fluxes.naturalremotedischarge / (self.parameters.control.nmblogentries)
        else:
            self.sequences.fluxes.naturalremotedischarge = 0.0
    cpdef inline void calc_remotedemand(self)  nogil:
        self.sequences.fluxes.remotedemand = max(            self.parameters.control.remotedischargeminimum[self.parameters.derived.toy[self.idx_sim]]            - self.sequences.fluxes.naturalremotedischarge,            0.0,        )
    cpdef inline void calc_remotefailure(self)  nogil:
        cdef int idx
        self.sequences.fluxes.remotefailure = 0
        for idx in range(self.parameters.control.nmblogentries):
            self.sequences.fluxes.remotefailure = self.sequences.fluxes.remotefailure - (self.sequences.logs.loggedtotalremotedischarge[idx])
        self.sequences.fluxes.remotefailure = self.sequences.fluxes.remotefailure / (self.parameters.control.nmblogentries)
        self.sequences.fluxes.remotefailure = self.sequences.fluxes.remotefailure + (self.parameters.control.remotedischargeminimum[self.parameters.derived.toy[self.idx_sim]])
    cpdef inline void calc_requiredremoterelease(self)  nogil:
        self.sequences.fluxes.requiredremoterelease = self.sequences.fluxes.remotedemand + self.parameters.control.remotedischargesafety[            self.parameters.derived.toy[self.idx_sim]        ] * smoothutils.smooth_logistic1(            self.sequences.fluxes.remotefailure, self.parameters.derived.remotedischargesmoothpar[self.parameters.derived.toy[self.idx_sim]]        )
    cpdef inline void calc_requiredrelease(self)  nogil:
        self.sequences.fluxes.requiredrelease = self.parameters.control.neardischargeminimumthreshold[self.parameters.derived.toy[self.idx_sim]]
        self.sequences.fluxes.requiredrelease = self.sequences.fluxes.requiredrelease + smoothutils.smooth_logistic2(            self.sequences.fluxes.requiredremoterelease - self.sequences.fluxes.requiredrelease,            self.parameters.derived.neardischargeminimumsmoothpar2[self.parameters.derived.toy[self.idx_sim]],        )
    cpdef inline void calc_targetedrelease(self)  nogil:
        if self.parameters.control.restricttargetedrelease:
            self.sequences.fluxes.targetedrelease = smoothutils.smooth_logistic1(                self.sequences.fluxes.inflow - self.parameters.control.neardischargeminimumthreshold[self.parameters.derived.toy[self.idx_sim]],                self.parameters.derived.neardischargeminimumsmoothpar1[self.parameters.derived.toy[self.idx_sim]],            )
            self.sequences.fluxes.targetedrelease = (                self.sequences.fluxes.targetedrelease * self.sequences.fluxes.requiredrelease                + (1.0 - self.sequences.fluxes.targetedrelease) * self.sequences.fluxes.inflow            )
        else:
            self.sequences.fluxes.targetedrelease = self.sequences.fluxes.requiredrelease
    cpdef inline void calc_waterlevel_v1(self)  nogil:
        self.parameters.control.watervolume2waterlevel.inputs[0] = self.sequences.new_states.watervolume
        self.parameters.control.watervolume2waterlevel.calculate_values()
        self.sequences.aides.waterlevel = self.parameters.control.watervolume2waterlevel.outputs[0]
    cpdef inline void calc_actualrelease_v1(self)  nogil:
        self.sequences.fluxes.actualrelease = self.sequences.fluxes.targetedrelease * smoothutils.smooth_logistic1(            self.sequences.aides.waterlevel - self.parameters.control.waterlevelminimumthreshold,            self.parameters.derived.waterlevelminimumsmoothpar,        )
    cpdef inline void calc_flooddischarge_v1(self)  nogil:
        self.parameters.control.waterlevel2flooddischarge.inputs[0] = self.sequences.aides.waterlevel
        self.parameters.control.waterlevel2flooddischarge.calculate_values(self.parameters.derived.toy[self.idx_sim])
        self.sequences.fluxes.flooddischarge = self.parameters.control.waterlevel2flooddischarge.outputs[0]
    cpdef inline void calc_outflow_v1(self)  nogil:
        self.sequences.fluxes.outflow = max(self.sequences.fluxes.actualrelease + self.sequences.fluxes.flooddischarge, 0.0)
    cpdef inline void calc_waterlevel(self)  nogil:
        self.parameters.control.watervolume2waterlevel.inputs[0] = self.sequences.new_states.watervolume
        self.parameters.control.watervolume2waterlevel.calculate_values()
        self.sequences.aides.waterlevel = self.parameters.control.watervolume2waterlevel.outputs[0]
    cpdef inline void calc_actualrelease(self)  nogil:
        self.sequences.fluxes.actualrelease = self.sequences.fluxes.targetedrelease * smoothutils.smooth_logistic1(            self.sequences.aides.waterlevel - self.parameters.control.waterlevelminimumthreshold,            self.parameters.derived.waterlevelminimumsmoothpar,        )
    cpdef inline void calc_flooddischarge(self)  nogil:
        self.parameters.control.waterlevel2flooddischarge.inputs[0] = self.sequences.aides.waterlevel
        self.parameters.control.waterlevel2flooddischarge.calculate_values(self.parameters.derived.toy[self.idx_sim])
        self.sequences.fluxes.flooddischarge = self.parameters.control.waterlevel2flooddischarge.outputs[0]
    cpdef inline void calc_outflow(self)  nogil:
        self.sequences.fluxes.outflow = max(self.sequences.fluxes.actualrelease + self.sequences.fluxes.flooddischarge, 0.0)
    cpdef inline void update_watervolume_v1(self)  nogil:
        self.sequences.new_states.watervolume = (            self.sequences.old_states.watervolume + self.parameters.derived.seconds * (self.sequences.fluxes.inflow - self.sequences.fluxes.outflow) / 1e6        )
    cpdef inline void update_watervolume(self)  nogil:
        self.sequences.new_states.watervolume = (            self.sequences.old_states.watervolume + self.parameters.derived.seconds * (self.sequences.fluxes.inflow - self.sequences.fluxes.outflow) / 1e6        )
    cpdef inline void pass_outflow_v1(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.outflow)
    cpdef inline void update_loggedoutflow_v1(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.control.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedoutflow[idx] = self.sequences.logs.loggedoutflow[idx - 1]
        self.sequences.logs.loggedoutflow[0] = self.sequences.fluxes.outflow
    cpdef inline void pass_outflow(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.outflow)
    cpdef inline void update_loggedoutflow(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.control.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedoutflow[idx] = self.sequences.logs.loggedoutflow[idx - 1]
        self.sequences.logs.loggedoutflow[0] = self.sequences.fluxes.outflow
    cpdef inline void calc_missingremoterelease_v1(self)  nogil:
        self.sequences.fluxes.missingremoterelease = max(            self.sequences.fluxes.requiredremoterelease - self.sequences.fluxes.actualrelease, 0.0        )
    cpdef inline void pass_missingremoterelease_v1(self)  nogil:
        self.sequences.senders.d[0] = self.sequences.senders.d[0] + (self.sequences.fluxes.missingremoterelease)
    cpdef inline void calc_allowedremoterelieve_v2(self)  nogil:
        cdef int toy
        toy = self.parameters.derived.toy[self.idx_sim]
        self.sequences.fluxes.allowedremoterelieve = self.parameters.control.highestremoterelieve[            toy        ] * smoothutils.smooth_logistic1(            self.parameters.control.waterlevelrelievethreshold[toy] - self.sequences.aides.waterlevel,            self.parameters.derived.waterlevelrelievesmoothpar[toy],        )
    cpdef inline void pass_allowedremoterelieve_v1(self)  nogil:
        self.sequences.senders.r[0] = self.sequences.senders.r[0] + (self.sequences.fluxes.allowedremoterelieve)
    cpdef inline void calc_requiredremotesupply_v1(self)  nogil:
        cdef int toy
        toy = self.parameters.derived.toy[self.idx_sim]
        self.sequences.fluxes.requiredremotesupply = self.parameters.control.highestremotesupply[            toy        ] * smoothutils.smooth_logistic1(            self.parameters.control.waterlevelsupplythreshold[toy] - self.sequences.aides.waterlevel,            self.parameters.derived.waterlevelsupplysmoothpar[toy],        )
    cpdef inline void pass_requiredremotesupply_v1(self)  nogil:
        self.sequences.senders.s[0] = self.sequences.senders.s[0] + (self.sequences.fluxes.requiredremotesupply)
    cpdef inline void calc_missingremoterelease(self)  nogil:
        self.sequences.fluxes.missingremoterelease = max(            self.sequences.fluxes.requiredremoterelease - self.sequences.fluxes.actualrelease, 0.0        )
    cpdef inline void pass_missingremoterelease(self)  nogil:
        self.sequences.senders.d[0] = self.sequences.senders.d[0] + (self.sequences.fluxes.missingremoterelease)
    cpdef inline void calc_allowedremoterelieve(self)  nogil:
        cdef int toy
        toy = self.parameters.derived.toy[self.idx_sim]
        self.sequences.fluxes.allowedremoterelieve = self.parameters.control.highestremoterelieve[            toy        ] * smoothutils.smooth_logistic1(            self.parameters.control.waterlevelrelievethreshold[toy] - self.sequences.aides.waterlevel,            self.parameters.derived.waterlevelrelievesmoothpar[toy],        )
    cpdef inline void pass_allowedremoterelieve(self)  nogil:
        self.sequences.senders.r[0] = self.sequences.senders.r[0] + (self.sequences.fluxes.allowedremoterelieve)
    cpdef inline void calc_requiredremotesupply(self)  nogil:
        cdef int toy
        toy = self.parameters.derived.toy[self.idx_sim]
        self.sequences.fluxes.requiredremotesupply = self.parameters.control.highestremotesupply[            toy        ] * smoothutils.smooth_logistic1(            self.parameters.control.waterlevelsupplythreshold[toy] - self.sequences.aides.waterlevel,            self.parameters.derived.waterlevelsupplysmoothpar[toy],        )
    cpdef inline void pass_requiredremotesupply(self)  nogil:
        self.sequences.senders.s[0] = self.sequences.senders.s[0] + (self.sequences.fluxes.requiredremotesupply)
