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
cdef public numpy.int32_t SAND = 1
cdef public numpy.int32_t LOAMY_SAND = 2
cdef public numpy.int32_t SANDY_LOAM = 3
cdef public numpy.int32_t SILT_LOAM = 4
cdef public numpy.int32_t LOAM = 5
cdef public numpy.int32_t SANDY_CLAY_LOAM = 6
cdef public numpy.int32_t SILT_CLAY_LOAM = 7
cdef public numpy.int32_t CLAY_LOAM = 8
cdef public numpy.int32_t SANDY_CLAY = 9
cdef public numpy.int32_t SILTY_CLAY = 10
cdef public numpy.int32_t CLAY = 11
cdef public numpy.int32_t SEALED = 12
cdef public numpy.int32_t FIELD = 13
cdef public numpy.int32_t WINE = 14
cdef public numpy.int32_t ORCHARD = 15
cdef public numpy.int32_t SOIL = 16
cdef public numpy.int32_t PASTURE = 17
cdef public numpy.int32_t WETLAND = 18
cdef public numpy.int32_t TREES = 19
cdef public numpy.int32_t CONIFER = 20
cdef public numpy.int32_t DECIDIOUS = 21
cdef public numpy.int32_t MIXED = 22
@cython.final
cdef class Parameters:
    cdef public ControlParameters control
    cdef public DerivedParameters derived
    cdef public FixedParameters fixed
    cdef public SolverParameters solver
@cython.final
cdef class ControlParameters:
    cdef public double al
    cdef public double as_
    cdef public numpy.int32_t nu
    cdef public numpy.int32_t[:] lt
    cdef public double[:] aur
    cdef public double cp
    cdef public double cpet
    cdef public double[:,:] cpetl
    cdef public double[:] cpes
    cdef public double[:,:] lai
    cdef public double ih
    cdef public double tt
    cdef public double ti
    cdef public double[:] ddf
    cdef public double ddt
    cdef public double cw
    cdef public double cv
    cdef public double cg
    cdef public double cgf
    cdef public double cq
    cdef public double cd
    cdef public double cs
    cdef public double hsmin
    cdef public double xs
    cdef public double b
    cdef public double psiae
    cdef public double thetas
    cdef public double thetar
    cdef public double zeta1
    cdef public double zeta2
    cdef public double sh
    cdef public double st
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int32_t[:] moy
    cdef public numpy.int32_t nug
    cdef public double at
    cdef public double alr
    cdef public double asr
    cdef public double agr
    cdef public double qf
    cdef public double rh1
    cdef public double rh2
    cdef public double rt2
@cython.final
cdef class FixedParameters:
    cdef public double pi
@cython.final
cdef class SolverParameters:
    cdef public double abserrormax
    cdef public double relerrormax
    cdef public double reldtmin
    cdef public double reldtmax
@cython.final
cdef class Sequences:
    cdef public InputSequences inputs
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public AideSequences aides
    cdef public OutletSequences outlets
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InputSequences:
    cdef public double t
    cdef public int _t_ndim
    cdef public int _t_length
    cdef public bint _t_diskflag
    cdef public str _t_path
    cdef FILE *_t_file
    cdef public bint _t_ramflag
    cdef public double[:] _t_array
    cdef public bint _t_inputflag
    cdef double *_t_inputpointer
    cdef public double p
    cdef public int _p_ndim
    cdef public int _p_length
    cdef public bint _p_diskflag
    cdef public str _p_path
    cdef FILE *_p_file
    cdef public bint _p_ramflag
    cdef public double[:] _p_array
    cdef public bint _p_inputflag
    cdef double *_p_inputpointer
    cdef public double pet
    cdef public int _pet_ndim
    cdef public int _pet_length
    cdef public bint _pet_diskflag
    cdef public str _pet_path
    cdef FILE *_pet_file
    cdef public bint _pet_ramflag
    cdef public double[:] _pet_array
    cdef public bint _pet_inputflag
    cdef double *_pet_inputpointer
    cdef public double fxg
    cdef public int _fxg_ndim
    cdef public int _fxg_length
    cdef public double[:] _fxg_points
    cdef public double[:] _fxg_results
    cdef public bint _fxg_diskflag
    cdef public str _fxg_path
    cdef FILE *_fxg_file
    cdef public bint _fxg_ramflag
    cdef public double[:] _fxg_array
    cdef public bint _fxg_inputflag
    cdef double *_fxg_inputpointer
    cdef public double fxs
    cdef public int _fxs_ndim
    cdef public int _fxs_length
    cdef public bint _fxs_diskflag
    cdef public str _fxs_path
    cdef FILE *_fxs_file
    cdef public bint _fxs_ramflag
    cdef public double[:] _fxs_array
    cdef public bint _fxs_inputflag
    cdef double *_fxs_inputpointer
    cpdef open_files(self, int idx):
        if self._t_diskflag:
            self._t_file = fopen(str(self._t_path).encode(), "rb+")
            fseek(self._t_file, idx*8, SEEK_SET)
        if self._p_diskflag:
            self._p_file = fopen(str(self._p_path).encode(), "rb+")
            fseek(self._p_file, idx*8, SEEK_SET)
        if self._pet_diskflag:
            self._pet_file = fopen(str(self._pet_path).encode(), "rb+")
            fseek(self._pet_file, idx*8, SEEK_SET)
        if self._fxg_diskflag:
            self._fxg_file = fopen(str(self._fxg_path).encode(), "rb+")
            fseek(self._fxg_file, idx*8, SEEK_SET)
        if self._fxs_diskflag:
            self._fxs_file = fopen(str(self._fxs_path).encode(), "rb+")
            fseek(self._fxs_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._t_diskflag:
            fclose(self._t_file)
        if self._p_diskflag:
            fclose(self._p_file)
        if self._pet_diskflag:
            fclose(self._pet_file)
        if self._fxg_diskflag:
            fclose(self._fxg_file)
        if self._fxs_diskflag:
            fclose(self._fxs_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._t_inputflag:
            self.t = self._t_inputpointer[0]
        elif self._t_diskflag:
            fread(&self.t, 8, 1, self._t_file)
        elif self._t_ramflag:
            self.t = self._t_array[idx]
        if self._p_inputflag:
            self.p = self._p_inputpointer[0]
        elif self._p_diskflag:
            fread(&self.p, 8, 1, self._p_file)
        elif self._p_ramflag:
            self.p = self._p_array[idx]
        if self._pet_inputflag:
            self.pet = self._pet_inputpointer[0]
        elif self._pet_diskflag:
            fread(&self.pet, 8, 1, self._pet_file)
        elif self._pet_ramflag:
            self.pet = self._pet_array[idx]
        if self._fxg_inputflag:
            self.fxg = self._fxg_inputpointer[0]
        elif self._fxg_diskflag:
            fread(&self.fxg, 8, 1, self._fxg_file)
        elif self._fxg_ramflag:
            self.fxg = self._fxg_array[idx]
        if self._fxs_inputflag:
            self.fxs = self._fxs_inputpointer[0]
        elif self._fxs_diskflag:
            fread(&self.fxs, 8, 1, self._fxs_file)
        elif self._fxs_ramflag:
            self.fxs = self._fxs_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._t_inputflag:
            if self._t_diskflag:
                fwrite(&self.t, 8, 1, self._t_file)
            elif self._t_ramflag:
                self._t_array[idx] = self.t
        if self._p_inputflag:
            if self._p_diskflag:
                fwrite(&self.p, 8, 1, self._p_file)
            elif self._p_ramflag:
                self._p_array[idx] = self.p
        if self._pet_inputflag:
            if self._pet_diskflag:
                fwrite(&self.pet, 8, 1, self._pet_file)
            elif self._pet_ramflag:
                self._pet_array[idx] = self.pet
        if self._fxg_inputflag:
            if self._fxg_diskflag:
                fwrite(&self.fxg, 8, 1, self._fxg_file)
            elif self._fxg_ramflag:
                self._fxg_array[idx] = self.fxg
        if self._fxs_inputflag:
            if self._fxs_diskflag:
                fwrite(&self.fxs, 8, 1, self._fxs_file)
            elif self._fxs_ramflag:
                self._fxs_array[idx] = self.fxs
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "t":
            self._t_inputpointer = value.p_value
        if name == "p":
            self._p_inputpointer = value.p_value
        if name == "pet":
            self._pet_inputpointer = value.p_value
        if name == "fxg":
            self._fxg_inputpointer = value.p_value
        if name == "fxs":
            self._fxs_inputpointer = value.p_value
@cython.final
cdef class FluxSequences:
    cdef public double pc
    cdef public int _pc_ndim
    cdef public int _pc_length
    cdef public double[:] _pc_points
    cdef public double[:] _pc_results
    cdef public double[:] _pc_integrals
    cdef public double _pc_sum
    cdef public bint _pc_diskflag
    cdef public str _pc_path
    cdef FILE *_pc_file
    cdef public bint _pc_ramflag
    cdef public double[:] _pc_array
    cdef public bint _pc_outputflag
    cdef double *_pc_outputpointer
    cdef public double[:] petl
    cdef public int _petl_ndim
    cdef public int _petl_length
    cdef public int _petl_length_0
    cdef public double[:,:] _petl_points
    cdef public double[:,:] _petl_results
    cdef public double[:,:] _petl_integrals
    cdef public double[:] _petl_sum
    cdef public bint _petl_diskflag
    cdef public str _petl_path
    cdef FILE *_petl_file
    cdef public bint _petl_ramflag
    cdef public double[:,:] _petl_array
    cdef public bint _petl_outputflag
    cdef double *_petl_outputpointer
    cdef public double pes
    cdef public int _pes_ndim
    cdef public int _pes_length
    cdef public double[:] _pes_points
    cdef public double[:] _pes_results
    cdef public double[:] _pes_integrals
    cdef public double _pes_sum
    cdef public bint _pes_diskflag
    cdef public str _pes_path
    cdef FILE *_pes_file
    cdef public bint _pes_ramflag
    cdef public double[:] _pes_array
    cdef public bint _pes_outputflag
    cdef double *_pes_outputpointer
    cdef public double[:] tf
    cdef public int _tf_ndim
    cdef public int _tf_length
    cdef public int _tf_length_0
    cdef public double[:,:] _tf_points
    cdef public double[:,:] _tf_results
    cdef public double[:,:] _tf_integrals
    cdef public double[:] _tf_sum
    cdef public bint _tf_diskflag
    cdef public str _tf_path
    cdef FILE *_tf_file
    cdef public bint _tf_ramflag
    cdef public double[:,:] _tf_array
    cdef public bint _tf_outputflag
    cdef double *_tf_outputpointer
    cdef public double[:] ei
    cdef public int _ei_ndim
    cdef public int _ei_length
    cdef public int _ei_length_0
    cdef public double[:,:] _ei_points
    cdef public double[:,:] _ei_results
    cdef public double[:,:] _ei_integrals
    cdef public double[:] _ei_sum
    cdef public bint _ei_diskflag
    cdef public str _ei_path
    cdef FILE *_ei_file
    cdef public bint _ei_ramflag
    cdef public double[:,:] _ei_array
    cdef public bint _ei_outputflag
    cdef double *_ei_outputpointer
    cdef public double[:] rf
    cdef public int _rf_ndim
    cdef public int _rf_length
    cdef public int _rf_length_0
    cdef public double[:,:] _rf_points
    cdef public double[:,:] _rf_results
    cdef public double[:,:] _rf_integrals
    cdef public double[:] _rf_sum
    cdef public bint _rf_diskflag
    cdef public str _rf_path
    cdef FILE *_rf_file
    cdef public bint _rf_ramflag
    cdef public double[:,:] _rf_array
    cdef public bint _rf_outputflag
    cdef double *_rf_outputpointer
    cdef public double[:] sf
    cdef public int _sf_ndim
    cdef public int _sf_length
    cdef public int _sf_length_0
    cdef public double[:,:] _sf_points
    cdef public double[:,:] _sf_results
    cdef public double[:,:] _sf_integrals
    cdef public double[:] _sf_sum
    cdef public bint _sf_diskflag
    cdef public str _sf_path
    cdef FILE *_sf_file
    cdef public bint _sf_ramflag
    cdef public double[:,:] _sf_array
    cdef public bint _sf_outputflag
    cdef double *_sf_outputpointer
    cdef public double[:] pm
    cdef public int _pm_ndim
    cdef public int _pm_length
    cdef public int _pm_length_0
    cdef public bint _pm_diskflag
    cdef public str _pm_path
    cdef FILE *_pm_file
    cdef public bint _pm_ramflag
    cdef public double[:,:] _pm_array
    cdef public bint _pm_outputflag
    cdef double *_pm_outputpointer
    cdef public double[:] am
    cdef public int _am_ndim
    cdef public int _am_length
    cdef public int _am_length_0
    cdef public double[:,:] _am_points
    cdef public double[:,:] _am_results
    cdef public double[:,:] _am_integrals
    cdef public double[:] _am_sum
    cdef public bint _am_diskflag
    cdef public str _am_path
    cdef FILE *_am_file
    cdef public bint _am_ramflag
    cdef public double[:,:] _am_array
    cdef public bint _am_outputflag
    cdef double *_am_outputpointer
    cdef public double ps
    cdef public int _ps_ndim
    cdef public int _ps_length
    cdef public double[:] _ps_points
    cdef public double[:] _ps_results
    cdef public double[:] _ps_integrals
    cdef public double _ps_sum
    cdef public bint _ps_diskflag
    cdef public str _ps_path
    cdef FILE *_ps_file
    cdef public bint _ps_ramflag
    cdef public double[:] _ps_array
    cdef public bint _ps_outputflag
    cdef double *_ps_outputpointer
    cdef public double pv
    cdef public int _pv_ndim
    cdef public int _pv_length
    cdef public double[:] _pv_points
    cdef public double[:] _pv_results
    cdef public double[:] _pv_integrals
    cdef public double _pv_sum
    cdef public bint _pv_diskflag
    cdef public str _pv_path
    cdef FILE *_pv_file
    cdef public bint _pv_ramflag
    cdef public double[:] _pv_array
    cdef public bint _pv_outputflag
    cdef double *_pv_outputpointer
    cdef public double pq
    cdef public int _pq_ndim
    cdef public int _pq_length
    cdef public double[:] _pq_points
    cdef public double[:] _pq_results
    cdef public double[:] _pq_integrals
    cdef public double _pq_sum
    cdef public bint _pq_diskflag
    cdef public str _pq_path
    cdef FILE *_pq_file
    cdef public bint _pq_ramflag
    cdef public double[:] _pq_array
    cdef public bint _pq_outputflag
    cdef double *_pq_outputpointer
    cdef public double etv
    cdef public int _etv_ndim
    cdef public int _etv_length
    cdef public double[:] _etv_points
    cdef public double[:] _etv_results
    cdef public double[:] _etv_integrals
    cdef public double _etv_sum
    cdef public bint _etv_diskflag
    cdef public str _etv_path
    cdef FILE *_etv_file
    cdef public bint _etv_ramflag
    cdef public double[:] _etv_array
    cdef public bint _etv_outputflag
    cdef double *_etv_outputpointer
    cdef public double es
    cdef public int _es_ndim
    cdef public int _es_length
    cdef public double[:] _es_points
    cdef public double[:] _es_results
    cdef public double[:] _es_integrals
    cdef public double _es_sum
    cdef public bint _es_diskflag
    cdef public str _es_path
    cdef FILE *_es_file
    cdef public bint _es_ramflag
    cdef public double[:] _es_array
    cdef public bint _es_outputflag
    cdef double *_es_outputpointer
    cdef public double et
    cdef public int _et_ndim
    cdef public int _et_length
    cdef public bint _et_diskflag
    cdef public str _et_path
    cdef FILE *_et_file
    cdef public bint _et_ramflag
    cdef public double[:] _et_array
    cdef public bint _et_outputflag
    cdef double *_et_outputpointer
    cdef public double fxs
    cdef public int _fxs_ndim
    cdef public int _fxs_length
    cdef public double[:] _fxs_points
    cdef public double[:] _fxs_results
    cdef public double[:] _fxs_integrals
    cdef public double _fxs_sum
    cdef public bint _fxs_diskflag
    cdef public str _fxs_path
    cdef FILE *_fxs_file
    cdef public bint _fxs_ramflag
    cdef public double[:] _fxs_array
    cdef public bint _fxs_outputflag
    cdef double *_fxs_outputpointer
    cdef public double fxg
    cdef public int _fxg_ndim
    cdef public int _fxg_length
    cdef public double[:] _fxg_points
    cdef public double[:] _fxg_results
    cdef public double[:] _fxg_integrals
    cdef public double _fxg_sum
    cdef public bint _fxg_diskflag
    cdef public str _fxg_path
    cdef FILE *_fxg_file
    cdef public bint _fxg_ramflag
    cdef public double[:] _fxg_array
    cdef public bint _fxg_outputflag
    cdef double *_fxg_outputpointer
    cdef public double cdg
    cdef public int _cdg_ndim
    cdef public int _cdg_length
    cdef public double[:] _cdg_points
    cdef public double[:] _cdg_results
    cdef public double[:] _cdg_integrals
    cdef public double _cdg_sum
    cdef public bint _cdg_diskflag
    cdef public str _cdg_path
    cdef FILE *_cdg_file
    cdef public bint _cdg_ramflag
    cdef public double[:] _cdg_array
    cdef public bint _cdg_outputflag
    cdef double *_cdg_outputpointer
    cdef public double fgs
    cdef public int _fgs_ndim
    cdef public int _fgs_length
    cdef public double[:] _fgs_points
    cdef public double[:] _fgs_results
    cdef public double[:] _fgs_integrals
    cdef public double _fgs_sum
    cdef public bint _fgs_diskflag
    cdef public str _fgs_path
    cdef FILE *_fgs_file
    cdef public bint _fgs_ramflag
    cdef public double[:] _fgs_array
    cdef public bint _fgs_outputflag
    cdef double *_fgs_outputpointer
    cdef public double fqs
    cdef public int _fqs_ndim
    cdef public int _fqs_length
    cdef public double[:] _fqs_points
    cdef public double[:] _fqs_results
    cdef public double[:] _fqs_integrals
    cdef public double _fqs_sum
    cdef public bint _fqs_diskflag
    cdef public str _fqs_path
    cdef FILE *_fqs_file
    cdef public bint _fqs_ramflag
    cdef public double[:] _fqs_array
    cdef public bint _fqs_outputflag
    cdef double *_fqs_outputpointer
    cdef public double rh
    cdef public int _rh_ndim
    cdef public int _rh_length
    cdef public double[:] _rh_points
    cdef public double[:] _rh_results
    cdef public double[:] _rh_integrals
    cdef public double _rh_sum
    cdef public bint _rh_diskflag
    cdef public str _rh_path
    cdef FILE *_rh_file
    cdef public bint _rh_ramflag
    cdef public double[:] _rh_array
    cdef public bint _rh_outputflag
    cdef double *_rh_outputpointer
    cdef public double r
    cdef public int _r_ndim
    cdef public int _r_length
    cdef public bint _r_diskflag
    cdef public str _r_path
    cdef FILE *_r_file
    cdef public bint _r_ramflag
    cdef public double[:] _r_array
    cdef public bint _r_outputflag
    cdef double *_r_outputpointer
    cpdef open_files(self, int idx):
        if self._pc_diskflag:
            self._pc_file = fopen(str(self._pc_path).encode(), "rb+")
            fseek(self._pc_file, idx*8, SEEK_SET)
        if self._petl_diskflag:
            self._petl_file = fopen(str(self._petl_path).encode(), "rb+")
            fseek(self._petl_file, idx*self._petl_length*8, SEEK_SET)
        if self._pes_diskflag:
            self._pes_file = fopen(str(self._pes_path).encode(), "rb+")
            fseek(self._pes_file, idx*8, SEEK_SET)
        if self._tf_diskflag:
            self._tf_file = fopen(str(self._tf_path).encode(), "rb+")
            fseek(self._tf_file, idx*self._tf_length*8, SEEK_SET)
        if self._ei_diskflag:
            self._ei_file = fopen(str(self._ei_path).encode(), "rb+")
            fseek(self._ei_file, idx*self._ei_length*8, SEEK_SET)
        if self._rf_diskflag:
            self._rf_file = fopen(str(self._rf_path).encode(), "rb+")
            fseek(self._rf_file, idx*self._rf_length*8, SEEK_SET)
        if self._sf_diskflag:
            self._sf_file = fopen(str(self._sf_path).encode(), "rb+")
            fseek(self._sf_file, idx*self._sf_length*8, SEEK_SET)
        if self._pm_diskflag:
            self._pm_file = fopen(str(self._pm_path).encode(), "rb+")
            fseek(self._pm_file, idx*self._pm_length*8, SEEK_SET)
        if self._am_diskflag:
            self._am_file = fopen(str(self._am_path).encode(), "rb+")
            fseek(self._am_file, idx*self._am_length*8, SEEK_SET)
        if self._ps_diskflag:
            self._ps_file = fopen(str(self._ps_path).encode(), "rb+")
            fseek(self._ps_file, idx*8, SEEK_SET)
        if self._pv_diskflag:
            self._pv_file = fopen(str(self._pv_path).encode(), "rb+")
            fseek(self._pv_file, idx*8, SEEK_SET)
        if self._pq_diskflag:
            self._pq_file = fopen(str(self._pq_path).encode(), "rb+")
            fseek(self._pq_file, idx*8, SEEK_SET)
        if self._etv_diskflag:
            self._etv_file = fopen(str(self._etv_path).encode(), "rb+")
            fseek(self._etv_file, idx*8, SEEK_SET)
        if self._es_diskflag:
            self._es_file = fopen(str(self._es_path).encode(), "rb+")
            fseek(self._es_file, idx*8, SEEK_SET)
        if self._et_diskflag:
            self._et_file = fopen(str(self._et_path).encode(), "rb+")
            fseek(self._et_file, idx*8, SEEK_SET)
        if self._fxs_diskflag:
            self._fxs_file = fopen(str(self._fxs_path).encode(), "rb+")
            fseek(self._fxs_file, idx*8, SEEK_SET)
        if self._fxg_diskflag:
            self._fxg_file = fopen(str(self._fxg_path).encode(), "rb+")
            fseek(self._fxg_file, idx*8, SEEK_SET)
        if self._cdg_diskflag:
            self._cdg_file = fopen(str(self._cdg_path).encode(), "rb+")
            fseek(self._cdg_file, idx*8, SEEK_SET)
        if self._fgs_diskflag:
            self._fgs_file = fopen(str(self._fgs_path).encode(), "rb+")
            fseek(self._fgs_file, idx*8, SEEK_SET)
        if self._fqs_diskflag:
            self._fqs_file = fopen(str(self._fqs_path).encode(), "rb+")
            fseek(self._fqs_file, idx*8, SEEK_SET)
        if self._rh_diskflag:
            self._rh_file = fopen(str(self._rh_path).encode(), "rb+")
            fseek(self._rh_file, idx*8, SEEK_SET)
        if self._r_diskflag:
            self._r_file = fopen(str(self._r_path).encode(), "rb+")
            fseek(self._r_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._pc_diskflag:
            fclose(self._pc_file)
        if self._petl_diskflag:
            fclose(self._petl_file)
        if self._pes_diskflag:
            fclose(self._pes_file)
        if self._tf_diskflag:
            fclose(self._tf_file)
        if self._ei_diskflag:
            fclose(self._ei_file)
        if self._rf_diskflag:
            fclose(self._rf_file)
        if self._sf_diskflag:
            fclose(self._sf_file)
        if self._pm_diskflag:
            fclose(self._pm_file)
        if self._am_diskflag:
            fclose(self._am_file)
        if self._ps_diskflag:
            fclose(self._ps_file)
        if self._pv_diskflag:
            fclose(self._pv_file)
        if self._pq_diskflag:
            fclose(self._pq_file)
        if self._etv_diskflag:
            fclose(self._etv_file)
        if self._es_diskflag:
            fclose(self._es_file)
        if self._et_diskflag:
            fclose(self._et_file)
        if self._fxs_diskflag:
            fclose(self._fxs_file)
        if self._fxg_diskflag:
            fclose(self._fxg_file)
        if self._cdg_diskflag:
            fclose(self._cdg_file)
        if self._fgs_diskflag:
            fclose(self._fgs_file)
        if self._fqs_diskflag:
            fclose(self._fqs_file)
        if self._rh_diskflag:
            fclose(self._rh_file)
        if self._r_diskflag:
            fclose(self._r_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._pc_diskflag:
            fread(&self.pc, 8, 1, self._pc_file)
        elif self._pc_ramflag:
            self.pc = self._pc_array[idx]
        if self._petl_diskflag:
            fread(&self.petl[0], 8, self._petl_length, self._petl_file)
        elif self._petl_ramflag:
            for jdx0 in range(self._petl_length_0):
                self.petl[jdx0] = self._petl_array[idx, jdx0]
        if self._pes_diskflag:
            fread(&self.pes, 8, 1, self._pes_file)
        elif self._pes_ramflag:
            self.pes = self._pes_array[idx]
        if self._tf_diskflag:
            fread(&self.tf[0], 8, self._tf_length, self._tf_file)
        elif self._tf_ramflag:
            for jdx0 in range(self._tf_length_0):
                self.tf[jdx0] = self._tf_array[idx, jdx0]
        if self._ei_diskflag:
            fread(&self.ei[0], 8, self._ei_length, self._ei_file)
        elif self._ei_ramflag:
            for jdx0 in range(self._ei_length_0):
                self.ei[jdx0] = self._ei_array[idx, jdx0]
        if self._rf_diskflag:
            fread(&self.rf[0], 8, self._rf_length, self._rf_file)
        elif self._rf_ramflag:
            for jdx0 in range(self._rf_length_0):
                self.rf[jdx0] = self._rf_array[idx, jdx0]
        if self._sf_diskflag:
            fread(&self.sf[0], 8, self._sf_length, self._sf_file)
        elif self._sf_ramflag:
            for jdx0 in range(self._sf_length_0):
                self.sf[jdx0] = self._sf_array[idx, jdx0]
        if self._pm_diskflag:
            fread(&self.pm[0], 8, self._pm_length, self._pm_file)
        elif self._pm_ramflag:
            for jdx0 in range(self._pm_length_0):
                self.pm[jdx0] = self._pm_array[idx, jdx0]
        if self._am_diskflag:
            fread(&self.am[0], 8, self._am_length, self._am_file)
        elif self._am_ramflag:
            for jdx0 in range(self._am_length_0):
                self.am[jdx0] = self._am_array[idx, jdx0]
        if self._ps_diskflag:
            fread(&self.ps, 8, 1, self._ps_file)
        elif self._ps_ramflag:
            self.ps = self._ps_array[idx]
        if self._pv_diskflag:
            fread(&self.pv, 8, 1, self._pv_file)
        elif self._pv_ramflag:
            self.pv = self._pv_array[idx]
        if self._pq_diskflag:
            fread(&self.pq, 8, 1, self._pq_file)
        elif self._pq_ramflag:
            self.pq = self._pq_array[idx]
        if self._etv_diskflag:
            fread(&self.etv, 8, 1, self._etv_file)
        elif self._etv_ramflag:
            self.etv = self._etv_array[idx]
        if self._es_diskflag:
            fread(&self.es, 8, 1, self._es_file)
        elif self._es_ramflag:
            self.es = self._es_array[idx]
        if self._et_diskflag:
            fread(&self.et, 8, 1, self._et_file)
        elif self._et_ramflag:
            self.et = self._et_array[idx]
        if self._fxs_diskflag:
            fread(&self.fxs, 8, 1, self._fxs_file)
        elif self._fxs_ramflag:
            self.fxs = self._fxs_array[idx]
        if self._fxg_diskflag:
            fread(&self.fxg, 8, 1, self._fxg_file)
        elif self._fxg_ramflag:
            self.fxg = self._fxg_array[idx]
        if self._cdg_diskflag:
            fread(&self.cdg, 8, 1, self._cdg_file)
        elif self._cdg_ramflag:
            self.cdg = self._cdg_array[idx]
        if self._fgs_diskflag:
            fread(&self.fgs, 8, 1, self._fgs_file)
        elif self._fgs_ramflag:
            self.fgs = self._fgs_array[idx]
        if self._fqs_diskflag:
            fread(&self.fqs, 8, 1, self._fqs_file)
        elif self._fqs_ramflag:
            self.fqs = self._fqs_array[idx]
        if self._rh_diskflag:
            fread(&self.rh, 8, 1, self._rh_file)
        elif self._rh_ramflag:
            self.rh = self._rh_array[idx]
        if self._r_diskflag:
            fread(&self.r, 8, 1, self._r_file)
        elif self._r_ramflag:
            self.r = self._r_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._pc_diskflag:
            fwrite(&self.pc, 8, 1, self._pc_file)
        elif self._pc_ramflag:
            self._pc_array[idx] = self.pc
        if self._petl_diskflag:
            fwrite(&self.petl[0], 8, self._petl_length, self._petl_file)
        elif self._petl_ramflag:
            for jdx0 in range(self._petl_length_0):
                self._petl_array[idx, jdx0] = self.petl[jdx0]
        if self._pes_diskflag:
            fwrite(&self.pes, 8, 1, self._pes_file)
        elif self._pes_ramflag:
            self._pes_array[idx] = self.pes
        if self._tf_diskflag:
            fwrite(&self.tf[0], 8, self._tf_length, self._tf_file)
        elif self._tf_ramflag:
            for jdx0 in range(self._tf_length_0):
                self._tf_array[idx, jdx0] = self.tf[jdx0]
        if self._ei_diskflag:
            fwrite(&self.ei[0], 8, self._ei_length, self._ei_file)
        elif self._ei_ramflag:
            for jdx0 in range(self._ei_length_0):
                self._ei_array[idx, jdx0] = self.ei[jdx0]
        if self._rf_diskflag:
            fwrite(&self.rf[0], 8, self._rf_length, self._rf_file)
        elif self._rf_ramflag:
            for jdx0 in range(self._rf_length_0):
                self._rf_array[idx, jdx0] = self.rf[jdx0]
        if self._sf_diskflag:
            fwrite(&self.sf[0], 8, self._sf_length, self._sf_file)
        elif self._sf_ramflag:
            for jdx0 in range(self._sf_length_0):
                self._sf_array[idx, jdx0] = self.sf[jdx0]
        if self._pm_diskflag:
            fwrite(&self.pm[0], 8, self._pm_length, self._pm_file)
        elif self._pm_ramflag:
            for jdx0 in range(self._pm_length_0):
                self._pm_array[idx, jdx0] = self.pm[jdx0]
        if self._am_diskflag:
            fwrite(&self.am[0], 8, self._am_length, self._am_file)
        elif self._am_ramflag:
            for jdx0 in range(self._am_length_0):
                self._am_array[idx, jdx0] = self.am[jdx0]
        if self._ps_diskflag:
            fwrite(&self.ps, 8, 1, self._ps_file)
        elif self._ps_ramflag:
            self._ps_array[idx] = self.ps
        if self._pv_diskflag:
            fwrite(&self.pv, 8, 1, self._pv_file)
        elif self._pv_ramflag:
            self._pv_array[idx] = self.pv
        if self._pq_diskflag:
            fwrite(&self.pq, 8, 1, self._pq_file)
        elif self._pq_ramflag:
            self._pq_array[idx] = self.pq
        if self._etv_diskflag:
            fwrite(&self.etv, 8, 1, self._etv_file)
        elif self._etv_ramflag:
            self._etv_array[idx] = self.etv
        if self._es_diskflag:
            fwrite(&self.es, 8, 1, self._es_file)
        elif self._es_ramflag:
            self._es_array[idx] = self.es
        if self._et_diskflag:
            fwrite(&self.et, 8, 1, self._et_file)
        elif self._et_ramflag:
            self._et_array[idx] = self.et
        if self._fxs_diskflag:
            fwrite(&self.fxs, 8, 1, self._fxs_file)
        elif self._fxs_ramflag:
            self._fxs_array[idx] = self.fxs
        if self._fxg_diskflag:
            fwrite(&self.fxg, 8, 1, self._fxg_file)
        elif self._fxg_ramflag:
            self._fxg_array[idx] = self.fxg
        if self._cdg_diskflag:
            fwrite(&self.cdg, 8, 1, self._cdg_file)
        elif self._cdg_ramflag:
            self._cdg_array[idx] = self.cdg
        if self._fgs_diskflag:
            fwrite(&self.fgs, 8, 1, self._fgs_file)
        elif self._fgs_ramflag:
            self._fgs_array[idx] = self.fgs
        if self._fqs_diskflag:
            fwrite(&self.fqs, 8, 1, self._fqs_file)
        elif self._fqs_ramflag:
            self._fqs_array[idx] = self.fqs
        if self._rh_diskflag:
            fwrite(&self.rh, 8, 1, self._rh_file)
        elif self._rh_ramflag:
            self._rh_array[idx] = self.rh
        if self._r_diskflag:
            fwrite(&self.r, 8, 1, self._r_file)
        elif self._r_ramflag:
            self._r_array[idx] = self.r
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "pc":
            self._pc_outputpointer = value.p_value
        if name == "pes":
            self._pes_outputpointer = value.p_value
        if name == "ps":
            self._ps_outputpointer = value.p_value
        if name == "pv":
            self._pv_outputpointer = value.p_value
        if name == "pq":
            self._pq_outputpointer = value.p_value
        if name == "etv":
            self._etv_outputpointer = value.p_value
        if name == "es":
            self._es_outputpointer = value.p_value
        if name == "et":
            self._et_outputpointer = value.p_value
        if name == "fxs":
            self._fxs_outputpointer = value.p_value
        if name == "fxg":
            self._fxg_outputpointer = value.p_value
        if name == "cdg":
            self._cdg_outputpointer = value.p_value
        if name == "fgs":
            self._fgs_outputpointer = value.p_value
        if name == "fqs":
            self._fqs_outputpointer = value.p_value
        if name == "rh":
            self._rh_outputpointer = value.p_value
        if name == "r":
            self._r_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._pc_outputflag:
            self._pc_outputpointer[0] = self.pc
        if self._pes_outputflag:
            self._pes_outputpointer[0] = self.pes
        if self._ps_outputflag:
            self._ps_outputpointer[0] = self.ps
        if self._pv_outputflag:
            self._pv_outputpointer[0] = self.pv
        if self._pq_outputflag:
            self._pq_outputpointer[0] = self.pq
        if self._etv_outputflag:
            self._etv_outputpointer[0] = self.etv
        if self._es_outputflag:
            self._es_outputpointer[0] = self.es
        if self._et_outputflag:
            self._et_outputpointer[0] = self.et
        if self._fxs_outputflag:
            self._fxs_outputpointer[0] = self.fxs
        if self._fxg_outputflag:
            self._fxg_outputpointer[0] = self.fxg
        if self._cdg_outputflag:
            self._cdg_outputpointer[0] = self.cdg
        if self._fgs_outputflag:
            self._fgs_outputpointer[0] = self.fgs
        if self._fqs_outputflag:
            self._fqs_outputpointer[0] = self.fqs
        if self._rh_outputflag:
            self._rh_outputpointer[0] = self.rh
        if self._r_outputflag:
            self._r_outputpointer[0] = self.r
@cython.final
cdef class StateSequences:
    cdef public double[:] ic
    cdef public int _ic_ndim
    cdef public int _ic_length
    cdef public int _ic_length_0
    cdef public double[:,:] _ic_points
    cdef public double[:,:] _ic_results
    cdef public bint _ic_diskflag
    cdef public str _ic_path
    cdef FILE *_ic_file
    cdef public bint _ic_ramflag
    cdef public double[:,:] _ic_array
    cdef public bint _ic_outputflag
    cdef double *_ic_outputpointer
    cdef public double[:] sp
    cdef public int _sp_ndim
    cdef public int _sp_length
    cdef public int _sp_length_0
    cdef public double[:,:] _sp_points
    cdef public double[:,:] _sp_results
    cdef public bint _sp_diskflag
    cdef public str _sp_path
    cdef FILE *_sp_file
    cdef public bint _sp_ramflag
    cdef public double[:,:] _sp_array
    cdef public bint _sp_outputflag
    cdef double *_sp_outputpointer
    cdef public double dv
    cdef public int _dv_ndim
    cdef public int _dv_length
    cdef public double[:] _dv_points
    cdef public double[:] _dv_results
    cdef public bint _dv_diskflag
    cdef public str _dv_path
    cdef FILE *_dv_file
    cdef public bint _dv_ramflag
    cdef public double[:] _dv_array
    cdef public bint _dv_outputflag
    cdef double *_dv_outputpointer
    cdef public double dg
    cdef public int _dg_ndim
    cdef public int _dg_length
    cdef public double[:] _dg_points
    cdef public double[:] _dg_results
    cdef public bint _dg_diskflag
    cdef public str _dg_path
    cdef FILE *_dg_file
    cdef public bint _dg_ramflag
    cdef public double[:] _dg_array
    cdef public bint _dg_outputflag
    cdef double *_dg_outputpointer
    cdef public double hq
    cdef public int _hq_ndim
    cdef public int _hq_length
    cdef public double[:] _hq_points
    cdef public double[:] _hq_results
    cdef public bint _hq_diskflag
    cdef public str _hq_path
    cdef FILE *_hq_file
    cdef public bint _hq_ramflag
    cdef public double[:] _hq_array
    cdef public bint _hq_outputflag
    cdef double *_hq_outputpointer
    cdef public double hs
    cdef public int _hs_ndim
    cdef public int _hs_length
    cdef public double[:] _hs_points
    cdef public double[:] _hs_results
    cdef public bint _hs_diskflag
    cdef public str _hs_path
    cdef FILE *_hs_file
    cdef public bint _hs_ramflag
    cdef public double[:] _hs_array
    cdef public bint _hs_outputflag
    cdef double *_hs_outputpointer
    cpdef open_files(self, int idx):
        if self._ic_diskflag:
            self._ic_file = fopen(str(self._ic_path).encode(), "rb+")
            fseek(self._ic_file, idx*self._ic_length*8, SEEK_SET)
        if self._sp_diskflag:
            self._sp_file = fopen(str(self._sp_path).encode(), "rb+")
            fseek(self._sp_file, idx*self._sp_length*8, SEEK_SET)
        if self._dv_diskflag:
            self._dv_file = fopen(str(self._dv_path).encode(), "rb+")
            fseek(self._dv_file, idx*8, SEEK_SET)
        if self._dg_diskflag:
            self._dg_file = fopen(str(self._dg_path).encode(), "rb+")
            fseek(self._dg_file, idx*8, SEEK_SET)
        if self._hq_diskflag:
            self._hq_file = fopen(str(self._hq_path).encode(), "rb+")
            fseek(self._hq_file, idx*8, SEEK_SET)
        if self._hs_diskflag:
            self._hs_file = fopen(str(self._hs_path).encode(), "rb+")
            fseek(self._hs_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._ic_diskflag:
            fclose(self._ic_file)
        if self._sp_diskflag:
            fclose(self._sp_file)
        if self._dv_diskflag:
            fclose(self._dv_file)
        if self._dg_diskflag:
            fclose(self._dg_file)
        if self._hq_diskflag:
            fclose(self._hq_file)
        if self._hs_diskflag:
            fclose(self._hs_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._ic_diskflag:
            fread(&self.ic[0], 8, self._ic_length, self._ic_file)
        elif self._ic_ramflag:
            for jdx0 in range(self._ic_length_0):
                self.ic[jdx0] = self._ic_array[idx, jdx0]
        if self._sp_diskflag:
            fread(&self.sp[0], 8, self._sp_length, self._sp_file)
        elif self._sp_ramflag:
            for jdx0 in range(self._sp_length_0):
                self.sp[jdx0] = self._sp_array[idx, jdx0]
        if self._dv_diskflag:
            fread(&self.dv, 8, 1, self._dv_file)
        elif self._dv_ramflag:
            self.dv = self._dv_array[idx]
        if self._dg_diskflag:
            fread(&self.dg, 8, 1, self._dg_file)
        elif self._dg_ramflag:
            self.dg = self._dg_array[idx]
        if self._hq_diskflag:
            fread(&self.hq, 8, 1, self._hq_file)
        elif self._hq_ramflag:
            self.hq = self._hq_array[idx]
        if self._hs_diskflag:
            fread(&self.hs, 8, 1, self._hs_file)
        elif self._hs_ramflag:
            self.hs = self._hs_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._ic_diskflag:
            fwrite(&self.ic[0], 8, self._ic_length, self._ic_file)
        elif self._ic_ramflag:
            for jdx0 in range(self._ic_length_0):
                self._ic_array[idx, jdx0] = self.ic[jdx0]
        if self._sp_diskflag:
            fwrite(&self.sp[0], 8, self._sp_length, self._sp_file)
        elif self._sp_ramflag:
            for jdx0 in range(self._sp_length_0):
                self._sp_array[idx, jdx0] = self.sp[jdx0]
        if self._dv_diskflag:
            fwrite(&self.dv, 8, 1, self._dv_file)
        elif self._dv_ramflag:
            self._dv_array[idx] = self.dv
        if self._dg_diskflag:
            fwrite(&self.dg, 8, 1, self._dg_file)
        elif self._dg_ramflag:
            self._dg_array[idx] = self.dg
        if self._hq_diskflag:
            fwrite(&self.hq, 8, 1, self._hq_file)
        elif self._hq_ramflag:
            self._hq_array[idx] = self.hq
        if self._hs_diskflag:
            fwrite(&self.hs, 8, 1, self._hs_file)
        elif self._hs_ramflag:
            self._hs_array[idx] = self.hs
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "dv":
            self._dv_outputpointer = value.p_value
        if name == "dg":
            self._dg_outputpointer = value.p_value
        if name == "hq":
            self._hq_outputpointer = value.p_value
        if name == "hs":
            self._hs_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._dv_outputflag:
            self._dv_outputpointer[0] = self.dv
        if self._dg_outputflag:
            self._dg_outputpointer[0] = self.dg
        if self._hq_outputflag:
            self._hq_outputpointer[0] = self.hq
        if self._hs_outputflag:
            self._hs_outputpointer[0] = self.hs
@cython.final
cdef class AideSequences:
    cdef public double fr
    cdef public int _fr_ndim
    cdef public int _fr_length
    cdef public double w
    cdef public int _w_ndim
    cdef public int _w_length
    cdef public double beta
    cdef public int _beta_ndim
    cdef public int _beta_length
    cdef public double dveq
    cdef public int _dveq_ndim
    cdef public int _dveq_length
    cdef public double dgeq
    cdef public int _dgeq_ndim
    cdef public int _dgeq_length
    cdef public double gf
    cdef public int _gf_ndim
    cdef public int _gf_length
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
cdef class PegasusDGEq(rootutils.PegasusBase):
    cpdef public Model model
    def __init__(self, Model model):
        self.model = model
    cpdef double apply_method0(self, double x) nogil:
        return self.model.return_errordv_v1(x)
@cython.final
cdef class QuadDVEq_V1(quadutils.QuadBase):
    cpdef public Model model
    def __init__(self, Model model):
        self.model = model
    cpdef double apply_method0(self, double x) nogil:
        return self.model.return_dvh_v1(x)
@cython.final
cdef class QuadDVEq_V2(quadutils.QuadBase):
    cpdef public Model model
    def __init__(self, Model model):
        self.model = model
    cpdef double apply_method0(self, double x) nogil:
        return self.model.return_dvh_v2(x)
@cython.final
cdef class Model:
    cdef public int idx_sim
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public PegasusDGEq pegasusdgeq
    cdef public QuadDVEq_V1 quaddveq_v1
    cdef public QuadDVEq_V2 quaddveq_v2
    cdef public NumConsts numconsts
    cdef public NumVars numvars
    def __init__(self):
        self.pegasusdgeq = PegasusDGEq(self)
        self.quaddveq_v1 = QuadDVEq_V1(self)
        self.quaddveq_v2 = QuadDVEq_V2(self)
    cpdef inline void simulate(self, int idx)  nogil:
        self.idx_sim = idx
        self.load_data()
        self.update_inlets()
        self.solve()
        self.update_outlets()
        self.update_outputs()
    cpdef inline void open_files(self):
        self.sequences.inputs.open_files(self.idx_sim)
        self.sequences.fluxes.open_files(self.idx_sim)
        self.sequences.states.open_files(self.idx_sim)
    cpdef inline void close_files(self):
        self.sequences.inputs.close_files()
        self.sequences.fluxes.close_files()
        self.sequences.states.close_files()
    cpdef inline void load_data(self) nogil:
        self.sequences.inputs.load_data(self.idx_sim)
    cpdef inline void save_data(self, int idx) nogil:
        self.sequences.inputs.save_data(self.idx_sim)
        self.sequences.fluxes.save_data(self.idx_sim)
        self.sequences.states.save_data(self.idx_sim)
    cpdef inline void new2old(self) nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        for jdx0 in range(self.sequences.states._ic_length_0):
            self.sequences.old_states.ic[jdx0] = self.sequences.new_states.ic[jdx0]
        for jdx0 in range(self.sequences.states._sp_length_0):
            self.sequences.old_states.sp[jdx0] = self.sequences.new_states.sp[jdx0]
        self.sequences.old_states.dv = self.sequences.new_states.dv
        self.sequences.old_states.dg = self.sequences.new_states.dg
        self.sequences.old_states.hq = self.sequences.new_states.hq
        self.sequences.old_states.hs = self.sequences.new_states.hs
    cpdef inline void update_inlets(self) nogil:
        self.calc_fr_v1()
        self.calc_pm_v1()
    cpdef inline void update_outlets(self) nogil:
        self.calc_et_v1()
        self.calc_r_v1()
        self.pass_r_v1()
    cpdef inline void update_receivers(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_senders(self, int idx) nogil:
        self.idx_sim = idx
        pass
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
        self.calc_fxs_v1()
        self.calc_fxg_v1()
        self.calc_pc_v1()
        self.calc_petl_v1()
        self.calc_pes_v1()
        self.calc_tf_v1()
        self.calc_ei_v1()
        self.calc_sf_v1()
        self.calc_rf_v1()
        self.calc_am_v1()
        self.calc_ps_v1()
        self.calc_w_v1()
        self.calc_pv_v1()
        self.calc_pq_v1()
        self.calc_beta_v1()
        self.calc_etv_v1()
        self.calc_es_v1()
        self.calc_fqs_v1()
        self.calc_fgs_v1()
        self.calc_rh_v1()
        self.calc_dveq_v1()
        self.calc_dveq_v2()
        self.calc_dveq_v3()
        self.calc_dveq_v4()
        self.calc_dgeq_v1()
        self.calc_gf_v1()
        self.calc_cdg_v1()
        self.calc_cdg_v2()
    cpdef inline void calculate_full_terms(self) nogil:
        self.update_ic_v1()
        self.update_sp_v1()
        self.update_dv_v1()
        self.update_dg_v1()
        self.update_hq_v1()
        self.update_hs_v1()
    cpdef inline void get_point_states(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.states._ic_length):
            self.sequences.states.ic[idx0] = self.sequences.states._ic_points[self.numvars.idx_stage][idx0]
        for idx0 in range(self.sequences.states._sp_length):
            self.sequences.states.sp[idx0] = self.sequences.states._sp_points[self.numvars.idx_stage][idx0]
        self.sequences.states.dv = self.sequences.states._dv_points[self.numvars.idx_stage]
        self.sequences.states.dg = self.sequences.states._dg_points[self.numvars.idx_stage]
        self.sequences.states.hq = self.sequences.states._hq_points[self.numvars.idx_stage]
        self.sequences.states.hs = self.sequences.states._hs_points[self.numvars.idx_stage]
    cpdef inline void set_point_states(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.states._ic_length):
            self.sequences.states._ic_points[self.numvars.idx_stage][idx0] = self.sequences.states.ic[idx0]
        for idx0 in range(self.sequences.states._sp_length):
            self.sequences.states._sp_points[self.numvars.idx_stage][idx0] = self.sequences.states.sp[idx0]
        self.sequences.states._dv_points[self.numvars.idx_stage] = self.sequences.states.dv
        self.sequences.states._dg_points[self.numvars.idx_stage] = self.sequences.states.dg
        self.sequences.states._hq_points[self.numvars.idx_stage] = self.sequences.states.hq
        self.sequences.states._hs_points[self.numvars.idx_stage] = self.sequences.states.hs
    cpdef inline void set_result_states(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.states._ic_length):
            self.sequences.states._ic_results[self.numvars.idx_method][idx0] = self.sequences.states.ic[idx0]
        for idx0 in range(self.sequences.states._sp_length):
            self.sequences.states._sp_results[self.numvars.idx_method][idx0] = self.sequences.states.sp[idx0]
        self.sequences.states._dv_results[self.numvars.idx_method] = self.sequences.states.dv
        self.sequences.states._dg_results[self.numvars.idx_method] = self.sequences.states.dg
        self.sequences.states._hq_results[self.numvars.idx_method] = self.sequences.states.hq
        self.sequences.states._hs_results[self.numvars.idx_method] = self.sequences.states.hs
    cpdef inline void get_sum_fluxes(self) nogil:
        cdef int idx0
        self.sequences.fluxes.pc = self.sequences.fluxes._pc_sum
        for idx0 in range(self.sequences.fluxes._petl_length):
            self.sequences.fluxes.petl[idx0] = self.sequences.fluxes._petl_sum[idx0]
        self.sequences.fluxes.pes = self.sequences.fluxes._pes_sum
        for idx0 in range(self.sequences.fluxes._tf_length):
            self.sequences.fluxes.tf[idx0] = self.sequences.fluxes._tf_sum[idx0]
        for idx0 in range(self.sequences.fluxes._ei_length):
            self.sequences.fluxes.ei[idx0] = self.sequences.fluxes._ei_sum[idx0]
        for idx0 in range(self.sequences.fluxes._rf_length):
            self.sequences.fluxes.rf[idx0] = self.sequences.fluxes._rf_sum[idx0]
        for idx0 in range(self.sequences.fluxes._sf_length):
            self.sequences.fluxes.sf[idx0] = self.sequences.fluxes._sf_sum[idx0]
        for idx0 in range(self.sequences.fluxes._am_length):
            self.sequences.fluxes.am[idx0] = self.sequences.fluxes._am_sum[idx0]
        self.sequences.fluxes.ps = self.sequences.fluxes._ps_sum
        self.sequences.fluxes.pv = self.sequences.fluxes._pv_sum
        self.sequences.fluxes.pq = self.sequences.fluxes._pq_sum
        self.sequences.fluxes.etv = self.sequences.fluxes._etv_sum
        self.sequences.fluxes.es = self.sequences.fluxes._es_sum
        self.sequences.fluxes.fxs = self.sequences.fluxes._fxs_sum
        self.sequences.fluxes.fxg = self.sequences.fluxes._fxg_sum
        self.sequences.fluxes.cdg = self.sequences.fluxes._cdg_sum
        self.sequences.fluxes.fgs = self.sequences.fluxes._fgs_sum
        self.sequences.fluxes.fqs = self.sequences.fluxes._fqs_sum
        self.sequences.fluxes.rh = self.sequences.fluxes._rh_sum
    cpdef inline void set_point_fluxes(self) nogil:
        cdef int idx0
        self.sequences.fluxes._pc_points[self.numvars.idx_stage] = self.sequences.fluxes.pc
        for idx0 in range(self.sequences.fluxes._petl_length):
            self.sequences.fluxes._petl_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.petl[idx0]
        self.sequences.fluxes._pes_points[self.numvars.idx_stage] = self.sequences.fluxes.pes
        for idx0 in range(self.sequences.fluxes._tf_length):
            self.sequences.fluxes._tf_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.tf[idx0]
        for idx0 in range(self.sequences.fluxes._ei_length):
            self.sequences.fluxes._ei_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.ei[idx0]
        for idx0 in range(self.sequences.fluxes._rf_length):
            self.sequences.fluxes._rf_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.rf[idx0]
        for idx0 in range(self.sequences.fluxes._sf_length):
            self.sequences.fluxes._sf_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.sf[idx0]
        for idx0 in range(self.sequences.fluxes._am_length):
            self.sequences.fluxes._am_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.am[idx0]
        self.sequences.fluxes._ps_points[self.numvars.idx_stage] = self.sequences.fluxes.ps
        self.sequences.fluxes._pv_points[self.numvars.idx_stage] = self.sequences.fluxes.pv
        self.sequences.fluxes._pq_points[self.numvars.idx_stage] = self.sequences.fluxes.pq
        self.sequences.fluxes._etv_points[self.numvars.idx_stage] = self.sequences.fluxes.etv
        self.sequences.fluxes._es_points[self.numvars.idx_stage] = self.sequences.fluxes.es
        self.sequences.fluxes._fxs_points[self.numvars.idx_stage] = self.sequences.fluxes.fxs
        self.sequences.fluxes._fxg_points[self.numvars.idx_stage] = self.sequences.fluxes.fxg
        self.sequences.fluxes._cdg_points[self.numvars.idx_stage] = self.sequences.fluxes.cdg
        self.sequences.fluxes._fgs_points[self.numvars.idx_stage] = self.sequences.fluxes.fgs
        self.sequences.fluxes._fqs_points[self.numvars.idx_stage] = self.sequences.fluxes.fqs
        self.sequences.fluxes._rh_points[self.numvars.idx_stage] = self.sequences.fluxes.rh
    cpdef inline void set_result_fluxes(self) nogil:
        cdef int idx0
        self.sequences.fluxes._pc_results[self.numvars.idx_method] = self.sequences.fluxes.pc
        for idx0 in range(self.sequences.fluxes._petl_length):
            self.sequences.fluxes._petl_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.petl[idx0]
        self.sequences.fluxes._pes_results[self.numvars.idx_method] = self.sequences.fluxes.pes
        for idx0 in range(self.sequences.fluxes._tf_length):
            self.sequences.fluxes._tf_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.tf[idx0]
        for idx0 in range(self.sequences.fluxes._ei_length):
            self.sequences.fluxes._ei_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.ei[idx0]
        for idx0 in range(self.sequences.fluxes._rf_length):
            self.sequences.fluxes._rf_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.rf[idx0]
        for idx0 in range(self.sequences.fluxes._sf_length):
            self.sequences.fluxes._sf_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.sf[idx0]
        for idx0 in range(self.sequences.fluxes._am_length):
            self.sequences.fluxes._am_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.am[idx0]
        self.sequences.fluxes._ps_results[self.numvars.idx_method] = self.sequences.fluxes.ps
        self.sequences.fluxes._pv_results[self.numvars.idx_method] = self.sequences.fluxes.pv
        self.sequences.fluxes._pq_results[self.numvars.idx_method] = self.sequences.fluxes.pq
        self.sequences.fluxes._etv_results[self.numvars.idx_method] = self.sequences.fluxes.etv
        self.sequences.fluxes._es_results[self.numvars.idx_method] = self.sequences.fluxes.es
        self.sequences.fluxes._fxs_results[self.numvars.idx_method] = self.sequences.fluxes.fxs
        self.sequences.fluxes._fxg_results[self.numvars.idx_method] = self.sequences.fluxes.fxg
        self.sequences.fluxes._cdg_results[self.numvars.idx_method] = self.sequences.fluxes.cdg
        self.sequences.fluxes._fgs_results[self.numvars.idx_method] = self.sequences.fluxes.fgs
        self.sequences.fluxes._fqs_results[self.numvars.idx_method] = self.sequences.fluxes.fqs
        self.sequences.fluxes._rh_results[self.numvars.idx_method] = self.sequences.fluxes.rh
    cpdef inline void integrate_fluxes(self) nogil:
        cdef int jdx, idx0
        self.sequences.fluxes.pc = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.pc = self.sequences.fluxes.pc +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._pc_points[jdx]
        for idx0 in range(self.sequences.fluxes._petl_length):
            self.sequences.fluxes.petl[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.petl[idx0] = self.sequences.fluxes.petl[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._petl_points[jdx, idx0]
        self.sequences.fluxes.pes = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.pes = self.sequences.fluxes.pes +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._pes_points[jdx]
        for idx0 in range(self.sequences.fluxes._tf_length):
            self.sequences.fluxes.tf[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.tf[idx0] = self.sequences.fluxes.tf[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._tf_points[jdx, idx0]
        for idx0 in range(self.sequences.fluxes._ei_length):
            self.sequences.fluxes.ei[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.ei[idx0] = self.sequences.fluxes.ei[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._ei_points[jdx, idx0]
        for idx0 in range(self.sequences.fluxes._rf_length):
            self.sequences.fluxes.rf[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.rf[idx0] = self.sequences.fluxes.rf[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._rf_points[jdx, idx0]
        for idx0 in range(self.sequences.fluxes._sf_length):
            self.sequences.fluxes.sf[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.sf[idx0] = self.sequences.fluxes.sf[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._sf_points[jdx, idx0]
        for idx0 in range(self.sequences.fluxes._am_length):
            self.sequences.fluxes.am[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.am[idx0] = self.sequences.fluxes.am[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._am_points[jdx, idx0]
        self.sequences.fluxes.ps = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.ps = self.sequences.fluxes.ps +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._ps_points[jdx]
        self.sequences.fluxes.pv = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.pv = self.sequences.fluxes.pv +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._pv_points[jdx]
        self.sequences.fluxes.pq = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.pq = self.sequences.fluxes.pq +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._pq_points[jdx]
        self.sequences.fluxes.etv = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.etv = self.sequences.fluxes.etv +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._etv_points[jdx]
        self.sequences.fluxes.es = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.es = self.sequences.fluxes.es +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._es_points[jdx]
        self.sequences.fluxes.fxs = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.fxs = self.sequences.fluxes.fxs +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._fxs_points[jdx]
        self.sequences.fluxes.fxg = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.fxg = self.sequences.fluxes.fxg +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._fxg_points[jdx]
        self.sequences.fluxes.cdg = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.cdg = self.sequences.fluxes.cdg +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._cdg_points[jdx]
        self.sequences.fluxes.fgs = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.fgs = self.sequences.fluxes.fgs +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._fgs_points[jdx]
        self.sequences.fluxes.fqs = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.fqs = self.sequences.fluxes.fqs +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._fqs_points[jdx]
        self.sequences.fluxes.rh = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.rh = self.sequences.fluxes.rh +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._rh_points[jdx]
    cpdef inline void reset_sum_fluxes(self) nogil:
        cdef int idx0
        self.sequences.fluxes._pc_sum = 0.
        for idx0 in range(self.sequences.fluxes._petl_length):
            self.sequences.fluxes._petl_sum[idx0] = 0.
        self.sequences.fluxes._pes_sum = 0.
        for idx0 in range(self.sequences.fluxes._tf_length):
            self.sequences.fluxes._tf_sum[idx0] = 0.
        for idx0 in range(self.sequences.fluxes._ei_length):
            self.sequences.fluxes._ei_sum[idx0] = 0.
        for idx0 in range(self.sequences.fluxes._rf_length):
            self.sequences.fluxes._rf_sum[idx0] = 0.
        for idx0 in range(self.sequences.fluxes._sf_length):
            self.sequences.fluxes._sf_sum[idx0] = 0.
        for idx0 in range(self.sequences.fluxes._am_length):
            self.sequences.fluxes._am_sum[idx0] = 0.
        self.sequences.fluxes._ps_sum = 0.
        self.sequences.fluxes._pv_sum = 0.
        self.sequences.fluxes._pq_sum = 0.
        self.sequences.fluxes._etv_sum = 0.
        self.sequences.fluxes._es_sum = 0.
        self.sequences.fluxes._fxs_sum = 0.
        self.sequences.fluxes._fxg_sum = 0.
        self.sequences.fluxes._cdg_sum = 0.
        self.sequences.fluxes._fgs_sum = 0.
        self.sequences.fluxes._fqs_sum = 0.
        self.sequences.fluxes._rh_sum = 0.
    cpdef inline void addup_fluxes(self) nogil:
        cdef int idx0
        self.sequences.fluxes._pc_sum = self.sequences.fluxes._pc_sum + self.sequences.fluxes.pc
        for idx0 in range(self.sequences.fluxes._petl_length):
            self.sequences.fluxes._petl_sum[idx0] = self.sequences.fluxes._petl_sum[idx0] + self.sequences.fluxes.petl[idx0]
        self.sequences.fluxes._pes_sum = self.sequences.fluxes._pes_sum + self.sequences.fluxes.pes
        for idx0 in range(self.sequences.fluxes._tf_length):
            self.sequences.fluxes._tf_sum[idx0] = self.sequences.fluxes._tf_sum[idx0] + self.sequences.fluxes.tf[idx0]
        for idx0 in range(self.sequences.fluxes._ei_length):
            self.sequences.fluxes._ei_sum[idx0] = self.sequences.fluxes._ei_sum[idx0] + self.sequences.fluxes.ei[idx0]
        for idx0 in range(self.sequences.fluxes._rf_length):
            self.sequences.fluxes._rf_sum[idx0] = self.sequences.fluxes._rf_sum[idx0] + self.sequences.fluxes.rf[idx0]
        for idx0 in range(self.sequences.fluxes._sf_length):
            self.sequences.fluxes._sf_sum[idx0] = self.sequences.fluxes._sf_sum[idx0] + self.sequences.fluxes.sf[idx0]
        for idx0 in range(self.sequences.fluxes._am_length):
            self.sequences.fluxes._am_sum[idx0] = self.sequences.fluxes._am_sum[idx0] + self.sequences.fluxes.am[idx0]
        self.sequences.fluxes._ps_sum = self.sequences.fluxes._ps_sum + self.sequences.fluxes.ps
        self.sequences.fluxes._pv_sum = self.sequences.fluxes._pv_sum + self.sequences.fluxes.pv
        self.sequences.fluxes._pq_sum = self.sequences.fluxes._pq_sum + self.sequences.fluxes.pq
        self.sequences.fluxes._etv_sum = self.sequences.fluxes._etv_sum + self.sequences.fluxes.etv
        self.sequences.fluxes._es_sum = self.sequences.fluxes._es_sum + self.sequences.fluxes.es
        self.sequences.fluxes._fxs_sum = self.sequences.fluxes._fxs_sum + self.sequences.fluxes.fxs
        self.sequences.fluxes._fxg_sum = self.sequences.fluxes._fxg_sum + self.sequences.fluxes.fxg
        self.sequences.fluxes._cdg_sum = self.sequences.fluxes._cdg_sum + self.sequences.fluxes.cdg
        self.sequences.fluxes._fgs_sum = self.sequences.fluxes._fgs_sum + self.sequences.fluxes.fgs
        self.sequences.fluxes._fqs_sum = self.sequences.fluxes._fqs_sum + self.sequences.fluxes.fqs
        self.sequences.fluxes._rh_sum = self.sequences.fluxes._rh_sum + self.sequences.fluxes.rh
    cpdef inline void calculate_error(self) nogil:
        cdef int idx0
        cdef double abserror
        self.numvars.abserror = 0.
        if self.numvars.use_relerror:
            self.numvars.relerror = 0.
        else:
            self.numvars.relerror = inf
        abserror = fabs(self.sequences.fluxes._pc_results[self.numvars.idx_method]-self.sequences.fluxes._pc_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._pc_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._pc_results[self.numvars.idx_method]))
        for idx0 in range(self.sequences.fluxes._petl_length):
            abserror = fabs(self.sequences.fluxes._petl_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._petl_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._petl_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._petl_results[self.numvars.idx_method, idx0]))
        abserror = fabs(self.sequences.fluxes._pes_results[self.numvars.idx_method]-self.sequences.fluxes._pes_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._pes_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._pes_results[self.numvars.idx_method]))
        for idx0 in range(self.sequences.fluxes._tf_length):
            abserror = fabs(self.sequences.fluxes._tf_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._tf_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._tf_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._tf_results[self.numvars.idx_method, idx0]))
        for idx0 in range(self.sequences.fluxes._ei_length):
            abserror = fabs(self.sequences.fluxes._ei_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._ei_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._ei_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._ei_results[self.numvars.idx_method, idx0]))
        for idx0 in range(self.sequences.fluxes._rf_length):
            abserror = fabs(self.sequences.fluxes._rf_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._rf_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._rf_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._rf_results[self.numvars.idx_method, idx0]))
        for idx0 in range(self.sequences.fluxes._sf_length):
            abserror = fabs(self.sequences.fluxes._sf_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._sf_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._sf_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._sf_results[self.numvars.idx_method, idx0]))
        for idx0 in range(self.sequences.fluxes._am_length):
            abserror = fabs(self.sequences.fluxes._am_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._am_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._am_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._am_results[self.numvars.idx_method, idx0]))
        abserror = fabs(self.sequences.fluxes._ps_results[self.numvars.idx_method]-self.sequences.fluxes._ps_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._ps_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._ps_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._pv_results[self.numvars.idx_method]-self.sequences.fluxes._pv_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._pv_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._pv_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._pq_results[self.numvars.idx_method]-self.sequences.fluxes._pq_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._pq_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._pq_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._etv_results[self.numvars.idx_method]-self.sequences.fluxes._etv_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._etv_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._etv_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._es_results[self.numvars.idx_method]-self.sequences.fluxes._es_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._es_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._es_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._fxs_results[self.numvars.idx_method]-self.sequences.fluxes._fxs_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._fxs_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._fxs_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._fxg_results[self.numvars.idx_method]-self.sequences.fluxes._fxg_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._fxg_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._fxg_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._cdg_results[self.numvars.idx_method]-self.sequences.fluxes._cdg_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._cdg_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._cdg_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._fgs_results[self.numvars.idx_method]-self.sequences.fluxes._fgs_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._fgs_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._fgs_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._fqs_results[self.numvars.idx_method]-self.sequences.fluxes._fqs_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._fqs_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._fqs_results[self.numvars.idx_method]))
        abserror = fabs(self.sequences.fluxes._rh_results[self.numvars.idx_method]-self.sequences.fluxes._rh_results[self.numvars.idx_method-1])
        self.numvars.abserror = max(self.numvars.abserror, abserror)
        if self.numvars.use_relerror:
            if self.sequences.fluxes._rh_results[self.numvars.idx_method] == 0.:
                self.numvars.relerror = inf
            else:
                self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._rh_results[self.numvars.idx_method]))
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
    cpdef inline void calc_fr_v1(self)  nogil:
        if self.sequences.inputs.t >= (self.parameters.control.tt + self.parameters.control.ti / 2.0):
            self.sequences.aides.fr = 1.0
        elif self.sequences.inputs.t <= (self.parameters.control.tt - self.parameters.control.ti / 2.0):
            self.sequences.aides.fr = 0.0
        else:
            self.sequences.aides.fr = (self.sequences.inputs.t - (self.parameters.control.tt - self.parameters.control.ti / 2.0)) / self.parameters.control.ti
    cpdef inline void calc_pm_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.fluxes.pm[k] = self.parameters.control.ddf[k] * smoothutils.smooth_logistic2(                self.sequences.inputs.t - self.parameters.control.ddt, self.parameters.derived.rt2            )
    cpdef inline void calc_fr(self)  nogil:
        if self.sequences.inputs.t >= (self.parameters.control.tt + self.parameters.control.ti / 2.0):
            self.sequences.aides.fr = 1.0
        elif self.sequences.inputs.t <= (self.parameters.control.tt - self.parameters.control.ti / 2.0):
            self.sequences.aides.fr = 0.0
        else:
            self.sequences.aides.fr = (self.sequences.inputs.t - (self.parameters.control.tt - self.parameters.control.ti / 2.0)) / self.parameters.control.ti
    cpdef inline void calc_pm(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.fluxes.pm[k] = self.parameters.control.ddf[k] * smoothutils.smooth_logistic2(                self.sequences.inputs.t - self.parameters.control.ddt, self.parameters.derived.rt2            )
    cpdef inline void calc_fxs_v1(self)  nogil:
        if self.sequences.inputs.fxs == 0.0:
            self.sequences.fluxes.fxs = 0.0
        elif self.parameters.derived.asr > 0.0:
            self.sequences.fluxes.fxs = self.sequences.inputs.fxs / self.parameters.derived.asr
        else:
            self.sequences.fluxes.fxs = inf
    cpdef inline void calc_fxg_v1(self)  nogil:
        cdef double d_ra
        if self.sequences.inputs.fxg == 0.0:
            self.sequences.fluxes.fxg = 0.0
        else:
            d_ra = self.parameters.derived.alr * self.parameters.derived.agr
            if d_ra > 0.0:
                self.sequences.fluxes.fxg = self.sequences.inputs.fxg / d_ra
            else:
                self.sequences.fluxes.fxg = inf
    cpdef inline void calc_pc_v1(self)  nogil:
        self.sequences.fluxes.pc = self.parameters.control.cp * self.sequences.inputs.p
    cpdef inline void calc_petl_v1(self)  nogil:
        cdef double d_cpetl
        cdef int k
        for k in range(self.parameters.control.nu):
            d_cpetl = self.parameters.control.cpetl[self.parameters.control.lt[k] - SEALED, self.parameters.derived.moy[self.idx_sim]]
            self.sequences.fluxes.petl[k] = self.parameters.control.cpet * d_cpetl * self.sequences.inputs.pet
    cpdef inline void calc_pes_v1(self)  nogil:
        cdef double d_cpes
        d_cpes = self.parameters.control.cpes[self.parameters.derived.moy[self.idx_sim]]
        self.sequences.fluxes.pes = self.parameters.control.cpet * d_cpes * self.sequences.inputs.pet
    cpdef inline void calc_tf_v1(self)  nogil:
        cdef double d_lai
        cdef int k
        for k in range(self.parameters.control.nu):
            d_lai = self.parameters.control.lai[self.parameters.control.lt[k] - SEALED, self.parameters.derived.moy[self.idx_sim]]
            self.sequences.fluxes.tf[k] = self.sequences.fluxes.pc * smoothutils.smooth_logistic1(                self.sequences.states.ic[k] - self.parameters.control.ih * d_lai, self.parameters.derived.rh1            )
    cpdef inline void calc_ei_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.fluxes.ei[k] = self.sequences.fluxes.petl[k] * (smoothutils.smooth_logistic1(self.sequences.states.ic[k], self.parameters.derived.rh1))
    cpdef inline void calc_sf_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.fluxes.sf[k] = (1.0 - self.sequences.aides.fr) * self.sequences.fluxes.tf[k]
    cpdef inline void calc_rf_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.fluxes.rf[k] = self.sequences.aides.fr * self.sequences.fluxes.tf[k]
    cpdef inline void calc_am_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.fluxes.am[k] = self.sequences.fluxes.pm[k] * smoothutils.smooth_logistic1(self.sequences.states.sp[k], self.parameters.derived.rh1)
    cpdef inline void calc_ps_v1(self)  nogil:
        self.sequences.fluxes.ps = self.sequences.fluxes.pc
    cpdef inline void calc_w_v1(self)  nogil:
        self.sequences.aides.w = 0.5 + 0.5 * cos(            max(min(self.sequences.states.dv, self.parameters.control.cw), 0.0) * self.parameters.fixed.pi / self.parameters.control.cw        )
    cpdef inline void calc_pv_v1(self)  nogil:
        cdef int k
        self.sequences.fluxes.pv = 0.0
        for k in range(self.parameters.control.nu):
            if self.parameters.control.lt[k] != SEALED:
                self.sequences.fluxes.pv = self.sequences.fluxes.pv + ((1.0 - self.sequences.aides.w) * self.parameters.control.aur[k] / self.parameters.derived.agr * (self.sequences.fluxes.rf[k] + self.sequences.fluxes.am[k]))
    cpdef inline void calc_pq_v1(self)  nogil:
        cdef double d_pq
        cdef int k
        self.sequences.fluxes.pq = 0.0
        for k in range(self.parameters.control.nu):
            d_pq = self.parameters.control.aur[k] * (self.sequences.fluxes.rf[k] + self.sequences.fluxes.am[k])
            if self.parameters.control.lt[k] != SEALED:
                d_pq = d_pq * (self.sequences.aides.w)
            self.sequences.fluxes.pq = self.sequences.fluxes.pq + (d_pq)
    cpdef inline void calc_beta_v1(self)  nogil:
        cdef double d_temp
        d_temp = self.parameters.control.zeta1 * (self.sequences.states.dv - self.parameters.control.zeta2)
        if d_temp > 700.0:
            self.sequences.aides.beta = 0.0
        else:
            d_temp = exp(d_temp)
            self.sequences.aides.beta = 0.5 + 0.5 * (1.0 - d_temp) / (1.0 + d_temp)
    cpdef inline void calc_etv_v1(self)  nogil:
        cdef int k
        self.sequences.fluxes.etv = 0.0
        for k in range(self.parameters.control.nu):
            if self.parameters.control.lt[k] != SEALED:
                self.sequences.fluxes.etv = self.sequences.fluxes.etv + (self.sequences.aides.beta * self.parameters.control.aur[k] / self.parameters.derived.agr * (self.sequences.fluxes.petl[k] - self.sequences.fluxes.ei[k]))
    cpdef inline void calc_es_v1(self)  nogil:
        self.sequences.fluxes.es = self.sequences.fluxes.pes * smoothutils.smooth_logistic1(self.sequences.states.hs, self.parameters.derived.rh1)
    cpdef inline void calc_fqs_v1(self)  nogil:
        if self.parameters.control.nu:
            self.sequences.fluxes.fqs = self.sequences.states.hq / self.parameters.control.cq
        else:
            self.sequences.fluxes.fqs = 0.0
    cpdef inline void calc_fgs_v1(self)  nogil:
        cdef double d_conductivity
        cdef double d_excess
        cdef double d_contactsurface
        cdef double d_gradient
        if self.parameters.derived.nug:
            d_gradient = self.parameters.control.cd - self.sequences.states.dg - self.sequences.states.hs
            d_contactsurface = smoothutils.smooth_max1(self.parameters.control.cd - self.sequences.states.dg, self.sequences.states.hs, self.parameters.derived.rh2)
            d_excess = smoothutils.smooth_max2(-self.sequences.states.dg, self.sequences.states.hs - self.parameters.control.cd, 0.0, self.parameters.derived.rh2)
            d_conductivity = (1.0 + self.parameters.control.cgf * d_excess) / self.parameters.control.cg
            self.sequences.fluxes.fgs = d_gradient * d_contactsurface * d_conductivity
        else:
            self.sequences.fluxes.fgs = 0.0
    cpdef inline void calc_rh_v1(self)  nogil:
        cdef double d_hs
        d_hs = smoothutils.smooth_logistic2(self.sequences.states.hs - self.parameters.control.hsmin, self.parameters.derived.rh2)
        self.sequences.fluxes.rh = self.parameters.control.cs * (d_hs / (self.parameters.control.cd - self.parameters.control.hsmin)) ** self.parameters.control.xs
    cpdef inline void calc_dveq_v1(self)  nogil:
        if self.parameters.derived.nug:
            if self.sequences.states.dg < self.parameters.control.psiae:
                self.sequences.aides.dveq = 0.0
            else:
                self.sequences.aides.dveq = self.parameters.control.thetas * (                    self.sequences.states.dg                    - self.sequences.states.dg ** (1.0 - 1.0 / self.parameters.control.b)                    / (1.0 - 1.0 / self.parameters.control.b)                    / self.parameters.control.psiae ** (-1.0 / self.parameters.control.b)                    - self.parameters.control.psiae / (1.0 - self.parameters.control.b)                )
        else:
            self.sequences.aides.dveq = nan
    cpdef inline void calc_dveq_v2(self)  nogil:
        cdef double d_above
        cdef double d_below
        cdef double d_x0
        if self.parameters.derived.nug:
            d_x0 = -10.0 * self.parameters.control.sh
            if self.sequences.states.dg > self.parameters.control.psiae:
                d_below = self.quaddveq_v1.integrate(d_x0, self.parameters.control.psiae, 2, 20, 1e-8)
                d_above = self.quaddveq_v1.integrate(self.parameters.control.psiae, self.sequences.states.dg, 2, 20, 1e-8)
                self.sequences.aides.dveq = d_below + d_above
            else:
                self.sequences.aides.dveq = self.quaddveq_v1.integrate(d_x0, self.sequences.states.dg, 2, 20, 1e-8)
        else:
            self.sequences.aides.dveq = nan
    cpdef inline void calc_dveq_v3(self)  nogil:
        if self.parameters.derived.nug:
            if self.sequences.states.dg < self.parameters.control.psiae:
                self.sequences.aides.dveq = self.parameters.control.thetar * self.sequences.states.dg
            else:
                self.sequences.aides.dveq = (self.parameters.control.thetas - self.parameters.control.thetar) * (                    self.sequences.states.dg                    - self.sequences.states.dg ** (1.0 - 1.0 / self.parameters.control.b)                    / (1.0 - 1.0 / self.parameters.control.b)                    / self.parameters.control.psiae ** (-1.0 / self.parameters.control.b)                    - self.parameters.control.psiae / (1.0 - self.parameters.control.b)                ) + self.parameters.control.thetar * self.sequences.states.dg
        else:
            self.sequences.aides.dveq = nan
    cpdef inline void calc_dveq_v4(self)  nogil:
        cdef double d_above
        cdef double d_below
        cdef double d_x0
        if self.parameters.derived.nug:
            d_x0 = -10.0 * self.parameters.control.sh
            if self.sequences.states.dg > self.parameters.control.psiae:
                d_below = self.quaddveq_v2.integrate(d_x0, self.parameters.control.psiae, 2, 20, 1e-8)
                d_above = self.quaddveq_v2.integrate(self.parameters.control.psiae, self.sequences.states.dg, 2, 20, 1e-8)
                self.sequences.aides.dveq = d_below + d_above
            else:
                self.sequences.aides.dveq = self.quaddveq_v2.integrate(d_x0, self.sequences.states.dg, 2, 20, 1e-8)
        else:
            self.sequences.aides.dveq = nan
    cpdef inline void calc_dgeq_v1(self)  nogil:
        cdef double d_error
        if self.sequences.states.dv > 0.0:
            d_error = self.return_errordv_v1(self.parameters.control.psiae)
            if d_error <= 0.0:
                self.sequences.aides.dgeq = self.pegasusdgeq.find_x(                    self.parameters.control.psiae,                    10000.0,                    self.parameters.control.psiae,                    1000000.0,                    0.0,                    1e-8,                    20,                )
            else:
                self.sequences.aides.dgeq = self.pegasusdgeq.find_x(                    0.0,                    self.parameters.control.psiae,                    0.0,                    self.parameters.control.psiae,                    0.0,                    1e-8,                    20,                )
        else:
            self.sequences.aides.dgeq = 0.0
    cpdef inline void calc_gf_v1(self)  nogil:
        self.sequences.aides.gf = smoothutils.smooth_logistic1(self.sequences.states.dg, self.parameters.derived.rh1) / self.return_dvh_v2(            self.sequences.aides.dgeq - self.sequences.states.dg        )
    cpdef inline void calc_cdg_v1(self)  nogil:
        cdef double d_target
        if self.parameters.derived.nug:
            d_target = smoothutils.smooth_min1(self.sequences.aides.dveq, self.sequences.states.dg, self.parameters.derived.rh1)
            self.sequences.fluxes.cdg = (self.sequences.states.dv - d_target) / self.parameters.control.cv
        else:
            self.sequences.fluxes.cdg = 0.0
    cpdef inline void calc_cdg_v2(self)  nogil:
        cdef double d_cdg_fast
        cdef double d_cdg_slow
        cdef double d_target
        if self.parameters.derived.nug:
            d_target = smoothutils.smooth_min1(self.sequences.aides.dveq, self.sequences.states.dg, self.parameters.derived.rh1)
            d_cdg_slow = (self.sequences.states.dv - d_target) / self.parameters.control.cv
            d_cdg_fast = self.sequences.aides.gf * (self.sequences.fluxes.fgs - self.sequences.fluxes.pv - self.sequences.fluxes.fxg)
            self.sequences.fluxes.cdg = d_cdg_slow + d_cdg_fast
        else:
            self.sequences.fluxes.cdg = 0.0
    cpdef inline void calc_fxs(self)  nogil:
        if self.sequences.inputs.fxs == 0.0:
            self.sequences.fluxes.fxs = 0.0
        elif self.parameters.derived.asr > 0.0:
            self.sequences.fluxes.fxs = self.sequences.inputs.fxs / self.parameters.derived.asr
        else:
            self.sequences.fluxes.fxs = inf
    cpdef inline void calc_fxg(self)  nogil:
        cdef double d_ra
        if self.sequences.inputs.fxg == 0.0:
            self.sequences.fluxes.fxg = 0.0
        else:
            d_ra = self.parameters.derived.alr * self.parameters.derived.agr
            if d_ra > 0.0:
                self.sequences.fluxes.fxg = self.sequences.inputs.fxg / d_ra
            else:
                self.sequences.fluxes.fxg = inf
    cpdef inline void calc_pc(self)  nogil:
        self.sequences.fluxes.pc = self.parameters.control.cp * self.sequences.inputs.p
    cpdef inline void calc_petl(self)  nogil:
        cdef double d_cpetl
        cdef int k
        for k in range(self.parameters.control.nu):
            d_cpetl = self.parameters.control.cpetl[self.parameters.control.lt[k] - SEALED, self.parameters.derived.moy[self.idx_sim]]
            self.sequences.fluxes.petl[k] = self.parameters.control.cpet * d_cpetl * self.sequences.inputs.pet
    cpdef inline void calc_pes(self)  nogil:
        cdef double d_cpes
        d_cpes = self.parameters.control.cpes[self.parameters.derived.moy[self.idx_sim]]
        self.sequences.fluxes.pes = self.parameters.control.cpet * d_cpes * self.sequences.inputs.pet
    cpdef inline void calc_tf(self)  nogil:
        cdef double d_lai
        cdef int k
        for k in range(self.parameters.control.nu):
            d_lai = self.parameters.control.lai[self.parameters.control.lt[k] - SEALED, self.parameters.derived.moy[self.idx_sim]]
            self.sequences.fluxes.tf[k] = self.sequences.fluxes.pc * smoothutils.smooth_logistic1(                self.sequences.states.ic[k] - self.parameters.control.ih * d_lai, self.parameters.derived.rh1            )
    cpdef inline void calc_ei(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.fluxes.ei[k] = self.sequences.fluxes.petl[k] * (smoothutils.smooth_logistic1(self.sequences.states.ic[k], self.parameters.derived.rh1))
    cpdef inline void calc_sf(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.fluxes.sf[k] = (1.0 - self.sequences.aides.fr) * self.sequences.fluxes.tf[k]
    cpdef inline void calc_rf(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.fluxes.rf[k] = self.sequences.aides.fr * self.sequences.fluxes.tf[k]
    cpdef inline void calc_am(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.fluxes.am[k] = self.sequences.fluxes.pm[k] * smoothutils.smooth_logistic1(self.sequences.states.sp[k], self.parameters.derived.rh1)
    cpdef inline void calc_ps(self)  nogil:
        self.sequences.fluxes.ps = self.sequences.fluxes.pc
    cpdef inline void calc_w(self)  nogil:
        self.sequences.aides.w = 0.5 + 0.5 * cos(            max(min(self.sequences.states.dv, self.parameters.control.cw), 0.0) * self.parameters.fixed.pi / self.parameters.control.cw        )
    cpdef inline void calc_pv(self)  nogil:
        cdef int k
        self.sequences.fluxes.pv = 0.0
        for k in range(self.parameters.control.nu):
            if self.parameters.control.lt[k] != SEALED:
                self.sequences.fluxes.pv = self.sequences.fluxes.pv + ((1.0 - self.sequences.aides.w) * self.parameters.control.aur[k] / self.parameters.derived.agr * (self.sequences.fluxes.rf[k] + self.sequences.fluxes.am[k]))
    cpdef inline void calc_pq(self)  nogil:
        cdef double d_pq
        cdef int k
        self.sequences.fluxes.pq = 0.0
        for k in range(self.parameters.control.nu):
            d_pq = self.parameters.control.aur[k] * (self.sequences.fluxes.rf[k] + self.sequences.fluxes.am[k])
            if self.parameters.control.lt[k] != SEALED:
                d_pq = d_pq * (self.sequences.aides.w)
            self.sequences.fluxes.pq = self.sequences.fluxes.pq + (d_pq)
    cpdef inline void calc_beta(self)  nogil:
        cdef double d_temp
        d_temp = self.parameters.control.zeta1 * (self.sequences.states.dv - self.parameters.control.zeta2)
        if d_temp > 700.0:
            self.sequences.aides.beta = 0.0
        else:
            d_temp = exp(d_temp)
            self.sequences.aides.beta = 0.5 + 0.5 * (1.0 - d_temp) / (1.0 + d_temp)
    cpdef inline void calc_etv(self)  nogil:
        cdef int k
        self.sequences.fluxes.etv = 0.0
        for k in range(self.parameters.control.nu):
            if self.parameters.control.lt[k] != SEALED:
                self.sequences.fluxes.etv = self.sequences.fluxes.etv + (self.sequences.aides.beta * self.parameters.control.aur[k] / self.parameters.derived.agr * (self.sequences.fluxes.petl[k] - self.sequences.fluxes.ei[k]))
    cpdef inline void calc_es(self)  nogil:
        self.sequences.fluxes.es = self.sequences.fluxes.pes * smoothutils.smooth_logistic1(self.sequences.states.hs, self.parameters.derived.rh1)
    cpdef inline void calc_fqs(self)  nogil:
        if self.parameters.control.nu:
            self.sequences.fluxes.fqs = self.sequences.states.hq / self.parameters.control.cq
        else:
            self.sequences.fluxes.fqs = 0.0
    cpdef inline void calc_fgs(self)  nogil:
        cdef double d_conductivity
        cdef double d_excess
        cdef double d_contactsurface
        cdef double d_gradient
        if self.parameters.derived.nug:
            d_gradient = self.parameters.control.cd - self.sequences.states.dg - self.sequences.states.hs
            d_contactsurface = smoothutils.smooth_max1(self.parameters.control.cd - self.sequences.states.dg, self.sequences.states.hs, self.parameters.derived.rh2)
            d_excess = smoothutils.smooth_max2(-self.sequences.states.dg, self.sequences.states.hs - self.parameters.control.cd, 0.0, self.parameters.derived.rh2)
            d_conductivity = (1.0 + self.parameters.control.cgf * d_excess) / self.parameters.control.cg
            self.sequences.fluxes.fgs = d_gradient * d_contactsurface * d_conductivity
        else:
            self.sequences.fluxes.fgs = 0.0
    cpdef inline void calc_rh(self)  nogil:
        cdef double d_hs
        d_hs = smoothutils.smooth_logistic2(self.sequences.states.hs - self.parameters.control.hsmin, self.parameters.derived.rh2)
        self.sequences.fluxes.rh = self.parameters.control.cs * (d_hs / (self.parameters.control.cd - self.parameters.control.hsmin)) ** self.parameters.control.xs
    cpdef inline void calc_dgeq(self)  nogil:
        cdef double d_error
        if self.sequences.states.dv > 0.0:
            d_error = self.return_errordv_v1(self.parameters.control.psiae)
            if d_error <= 0.0:
                self.sequences.aides.dgeq = self.pegasusdgeq.find_x(                    self.parameters.control.psiae,                    10000.0,                    self.parameters.control.psiae,                    1000000.0,                    0.0,                    1e-8,                    20,                )
            else:
                self.sequences.aides.dgeq = self.pegasusdgeq.find_x(                    0.0,                    self.parameters.control.psiae,                    0.0,                    self.parameters.control.psiae,                    0.0,                    1e-8,                    20,                )
        else:
            self.sequences.aides.dgeq = 0.0
    cpdef inline void calc_gf(self)  nogil:
        self.sequences.aides.gf = smoothutils.smooth_logistic1(self.sequences.states.dg, self.parameters.derived.rh1) / self.return_dvh_v2(            self.sequences.aides.dgeq - self.sequences.states.dg        )
    cpdef inline void update_ic_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.new_states.ic[k] = self.sequences.old_states.ic[k] + (self.sequences.fluxes.pc - self.sequences.fluxes.tf[k] - self.sequences.fluxes.ei[k])
    cpdef inline void update_sp_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.new_states.sp[k] = self.sequences.old_states.sp[k] + (self.sequences.fluxes.sf[k] - self.sequences.fluxes.am[k])
    cpdef inline void update_dv_v1(self)  nogil:
        if self.parameters.derived.nug:
            self.sequences.new_states.dv = self.sequences.old_states.dv - (self.sequences.fluxes.fxg + self.sequences.fluxes.pv - self.sequences.fluxes.etv - self.sequences.fluxes.fgs)
        else:
            self.sequences.new_states.dv = nan
    cpdef inline void update_dg_v1(self)  nogil:
        if self.parameters.derived.nug:
            self.sequences.new_states.dg = self.sequences.old_states.dg + self.sequences.fluxes.cdg
        else:
            self.sequences.new_states.dg = nan
    cpdef inline void update_hq_v1(self)  nogil:
        self.sequences.new_states.hq = self.sequences.old_states.hq + (self.sequences.fluxes.pq - self.sequences.fluxes.fqs)
    cpdef inline void update_hs_v1(self)  nogil:
        self.sequences.new_states.hs = (            self.sequences.old_states.hs            + (self.sequences.fluxes.fxs + self.sequences.fluxes.ps - self.sequences.fluxes.es)            - self.sequences.fluxes.rh / self.parameters.derived.asr            + self.parameters.derived.alr / self.parameters.derived.asr * self.sequences.fluxes.fqs            + (self.parameters.derived.alr * self.parameters.derived.agr) / self.parameters.derived.asr * self.sequences.fluxes.fgs        )
    cpdef inline void update_ic(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.new_states.ic[k] = self.sequences.old_states.ic[k] + (self.sequences.fluxes.pc - self.sequences.fluxes.tf[k] - self.sequences.fluxes.ei[k])
    cpdef inline void update_sp(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nu):
            self.sequences.new_states.sp[k] = self.sequences.old_states.sp[k] + (self.sequences.fluxes.sf[k] - self.sequences.fluxes.am[k])
    cpdef inline void update_dv(self)  nogil:
        if self.parameters.derived.nug:
            self.sequences.new_states.dv = self.sequences.old_states.dv - (self.sequences.fluxes.fxg + self.sequences.fluxes.pv - self.sequences.fluxes.etv - self.sequences.fluxes.fgs)
        else:
            self.sequences.new_states.dv = nan
    cpdef inline void update_dg(self)  nogil:
        if self.parameters.derived.nug:
            self.sequences.new_states.dg = self.sequences.old_states.dg + self.sequences.fluxes.cdg
        else:
            self.sequences.new_states.dg = nan
    cpdef inline void update_hq(self)  nogil:
        self.sequences.new_states.hq = self.sequences.old_states.hq + (self.sequences.fluxes.pq - self.sequences.fluxes.fqs)
    cpdef inline void update_hs(self)  nogil:
        self.sequences.new_states.hs = (            self.sequences.old_states.hs            + (self.sequences.fluxes.fxs + self.sequences.fluxes.ps - self.sequences.fluxes.es)            - self.sequences.fluxes.rh / self.parameters.derived.asr            + self.parameters.derived.alr / self.parameters.derived.asr * self.sequences.fluxes.fqs            + (self.parameters.derived.alr * self.parameters.derived.agr) / self.parameters.derived.asr * self.sequences.fluxes.fgs        )
    cpdef inline double return_errordv_v1(self, double dg)  nogil:
        cdef double d_delta
        cdef double d_dg
        cdef double d_dveq
        d_dveq, d_dg = self.sequences.aides.dveq, self.sequences.states.dg
        self.sequences.states.dg = dg
        self.calc_dveq_v3()
        d_delta = self.sequences.aides.dveq - self.sequences.states.dv
        self.sequences.aides.dveq, self.sequences.states.dg = d_dveq, d_dg
        return d_delta
    cpdef inline double return_dvh_v1(self, double h)  nogil:
        cdef double d_h
        d_h = smoothutils.smooth_max1(h, self.parameters.control.psiae, self.parameters.derived.rh1)
        return self.parameters.control.thetas * (1.0 - (d_h / self.parameters.control.psiae) ** (-1.0 / self.parameters.control.b))
    cpdef inline double return_dvh_v2(self, double h)  nogil:
        cdef double d_h
        d_h = smoothutils.smooth_max1(h, self.parameters.control.psiae, self.parameters.derived.rh1)
        return self.parameters.control.thetar + (            (self.parameters.control.thetas - self.parameters.control.thetar) * (1.0 - (d_h / self.parameters.control.psiae) ** (-1.0 / self.parameters.control.b))        )
    cpdef inline double return_errordv(self, double dg)  nogil:
        cdef double d_delta
        cdef double d_dg
        cdef double d_dveq
        d_dveq, d_dg = self.sequences.aides.dveq, self.sequences.states.dg
        self.sequences.states.dg = dg
        self.calc_dveq_v3()
        d_delta = self.sequences.aides.dveq - self.sequences.states.dv
        self.sequences.aides.dveq, self.sequences.states.dg = d_dveq, d_dg
        return d_delta
    cpdef inline void calc_et_v1(self)  nogil:
        cdef int k
        cdef double d_ei
        d_ei = 0.0
        for k in range(self.parameters.control.nu):
            d_ei = d_ei + (self.parameters.control.aur[k] * self.sequences.fluxes.ei[k])
        self.sequences.fluxes.et = self.parameters.derived.alr * (d_ei + self.parameters.derived.agr * self.sequences.fluxes.etv) + self.parameters.derived.asr * self.sequences.fluxes.es
    cpdef inline void calc_r_v1(self)  nogil:
        self.sequences.fluxes.r = self.parameters.derived.qf * self.sequences.fluxes.rh
    cpdef inline void pass_r_v1(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.r)
    cpdef inline void calc_et(self)  nogil:
        cdef int k
        cdef double d_ei
        d_ei = 0.0
        for k in range(self.parameters.control.nu):
            d_ei = d_ei + (self.parameters.control.aur[k] * self.sequences.fluxes.ei[k])
        self.sequences.fluxes.et = self.parameters.derived.alr * (d_ei + self.parameters.derived.agr * self.sequences.fluxes.etv) + self.parameters.derived.asr * self.sequences.fluxes.es
    cpdef inline void calc_r(self)  nogil:
        self.sequences.fluxes.r = self.parameters.derived.qf * self.sequences.fluxes.rh
    cpdef inline void pass_r(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.r)
