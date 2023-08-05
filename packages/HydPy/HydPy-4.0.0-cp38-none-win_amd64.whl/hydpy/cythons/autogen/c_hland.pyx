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
cdef public numpy.int32_t FIELD = 1
cdef public numpy.int32_t FOREST = 2
cdef public numpy.int32_t GLACIER = 3
cdef public numpy.int32_t ILAKE = 4
@cython.final
cdef class Parameters:
    cdef public ControlParameters control
    cdef public DerivedParameters derived
@cython.final
cdef class ControlParameters:
    cdef public double area
    cdef public numpy.int32_t nmbzones
    cdef public numpy.int32_t[:] zonetype
    cdef public double[:] zonearea
    cdef public double[:] zonez
    cdef public double zrelp
    cdef public double zrelt
    cdef public double zrele
    cdef public double[:] pcorr
    cdef public double[:] pcalt
    cdef public double[:] rfcf
    cdef public double[:] sfcf
    cdef public double[:] tcalt
    cdef public double[:] ecorr
    cdef public double[:] ecalt
    cdef public double[:] epf
    cdef public double[:] etf
    cdef public double[:] ered
    cdef public double[:] ttice
    cdef public double[:] icmax
    cdef public double[:] tt
    cdef public double[:] ttint
    cdef public double[:] dttm
    cdef public double[:] cfmax
    cdef public double[:] gmelt
    cdef public double[:] cfr
    cdef public double[:] whc
    cdef public double[:] fc
    cdef public double[:] lp
    cdef public double[:] beta
    cdef public double percmax
    cdef public double[:] cflux
    cdef public bint resparea
    cdef public numpy.int32_t recstep
    cdef public double alpha
    cdef public double k
    cdef public double k4
    cdef public double gamma
    cdef public double maxbaz
    cdef public double abstr
@cython.final
cdef class DerivedParameters:
    cdef public double relsoilarea
    cdef public double rellandarea
    cdef public double[:] relzonearea
    cdef public double[:] relsoilzonearea
    cdef public double[:] rellandzonearea
    cdef public double[:] ttm
    cdef public double dt
    cdef public double[:] uh
    cdef public double qfactor
@cython.final
cdef class Sequences:
    cdef public InputSequences inputs
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public LogSequences logs
    cdef public OutletSequences outlets
    cdef public StateSequences old_states
    cdef public StateSequences new_states
@cython.final
cdef class InputSequences:
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
    cdef public double tn
    cdef public int _tn_ndim
    cdef public int _tn_length
    cdef public bint _tn_diskflag
    cdef public str _tn_path
    cdef FILE *_tn_file
    cdef public bint _tn_ramflag
    cdef public double[:] _tn_array
    cdef public bint _tn_inputflag
    cdef double *_tn_inputpointer
    cdef public double epn
    cdef public int _epn_ndim
    cdef public int _epn_length
    cdef public bint _epn_diskflag
    cdef public str _epn_path
    cdef FILE *_epn_file
    cdef public bint _epn_ramflag
    cdef public double[:] _epn_array
    cdef public bint _epn_inputflag
    cdef double *_epn_inputpointer
    cpdef open_files(self, int idx):
        if self._p_diskflag:
            self._p_file = fopen(str(self._p_path).encode(), "rb+")
            fseek(self._p_file, idx*8, SEEK_SET)
        if self._t_diskflag:
            self._t_file = fopen(str(self._t_path).encode(), "rb+")
            fseek(self._t_file, idx*8, SEEK_SET)
        if self._tn_diskflag:
            self._tn_file = fopen(str(self._tn_path).encode(), "rb+")
            fseek(self._tn_file, idx*8, SEEK_SET)
        if self._epn_diskflag:
            self._epn_file = fopen(str(self._epn_path).encode(), "rb+")
            fseek(self._epn_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._p_diskflag:
            fclose(self._p_file)
        if self._t_diskflag:
            fclose(self._t_file)
        if self._tn_diskflag:
            fclose(self._tn_file)
        if self._epn_diskflag:
            fclose(self._epn_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._p_inputflag:
            self.p = self._p_inputpointer[0]
        elif self._p_diskflag:
            fread(&self.p, 8, 1, self._p_file)
        elif self._p_ramflag:
            self.p = self._p_array[idx]
        if self._t_inputflag:
            self.t = self._t_inputpointer[0]
        elif self._t_diskflag:
            fread(&self.t, 8, 1, self._t_file)
        elif self._t_ramflag:
            self.t = self._t_array[idx]
        if self._tn_inputflag:
            self.tn = self._tn_inputpointer[0]
        elif self._tn_diskflag:
            fread(&self.tn, 8, 1, self._tn_file)
        elif self._tn_ramflag:
            self.tn = self._tn_array[idx]
        if self._epn_inputflag:
            self.epn = self._epn_inputpointer[0]
        elif self._epn_diskflag:
            fread(&self.epn, 8, 1, self._epn_file)
        elif self._epn_ramflag:
            self.epn = self._epn_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._p_inputflag:
            if self._p_diskflag:
                fwrite(&self.p, 8, 1, self._p_file)
            elif self._p_ramflag:
                self._p_array[idx] = self.p
        if self._t_inputflag:
            if self._t_diskflag:
                fwrite(&self.t, 8, 1, self._t_file)
            elif self._t_ramflag:
                self._t_array[idx] = self.t
        if self._tn_inputflag:
            if self._tn_diskflag:
                fwrite(&self.tn, 8, 1, self._tn_file)
            elif self._tn_ramflag:
                self._tn_array[idx] = self.tn
        if self._epn_inputflag:
            if self._epn_diskflag:
                fwrite(&self.epn, 8, 1, self._epn_file)
            elif self._epn_ramflag:
                self._epn_array[idx] = self.epn
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "p":
            self._p_inputpointer = value.p_value
        if name == "t":
            self._t_inputpointer = value.p_value
        if name == "tn":
            self._tn_inputpointer = value.p_value
        if name == "epn":
            self._epn_inputpointer = value.p_value
@cython.final
cdef class FluxSequences:
    cdef public double tmean
    cdef public int _tmean_ndim
    cdef public int _tmean_length
    cdef public bint _tmean_diskflag
    cdef public str _tmean_path
    cdef FILE *_tmean_file
    cdef public bint _tmean_ramflag
    cdef public double[:] _tmean_array
    cdef public bint _tmean_outputflag
    cdef double *_tmean_outputpointer
    cdef public double[:] tc
    cdef public int _tc_ndim
    cdef public int _tc_length
    cdef public int _tc_length_0
    cdef public bint _tc_diskflag
    cdef public str _tc_path
    cdef FILE *_tc_file
    cdef public bint _tc_ramflag
    cdef public double[:,:] _tc_array
    cdef public bint _tc_outputflag
    cdef double *_tc_outputpointer
    cdef public double[:] fracrain
    cdef public int _fracrain_ndim
    cdef public int _fracrain_length
    cdef public int _fracrain_length_0
    cdef public bint _fracrain_diskflag
    cdef public str _fracrain_path
    cdef FILE *_fracrain_file
    cdef public bint _fracrain_ramflag
    cdef public double[:,:] _fracrain_array
    cdef public bint _fracrain_outputflag
    cdef double *_fracrain_outputpointer
    cdef public double[:] rfc
    cdef public int _rfc_ndim
    cdef public int _rfc_length
    cdef public int _rfc_length_0
    cdef public bint _rfc_diskflag
    cdef public str _rfc_path
    cdef FILE *_rfc_file
    cdef public bint _rfc_ramflag
    cdef public double[:,:] _rfc_array
    cdef public bint _rfc_outputflag
    cdef double *_rfc_outputpointer
    cdef public double[:] sfc
    cdef public int _sfc_ndim
    cdef public int _sfc_length
    cdef public int _sfc_length_0
    cdef public bint _sfc_diskflag
    cdef public str _sfc_path
    cdef FILE *_sfc_file
    cdef public bint _sfc_ramflag
    cdef public double[:,:] _sfc_array
    cdef public bint _sfc_outputflag
    cdef double *_sfc_outputpointer
    cdef public double[:] pc
    cdef public int _pc_ndim
    cdef public int _pc_length
    cdef public int _pc_length_0
    cdef public bint _pc_diskflag
    cdef public str _pc_path
    cdef FILE *_pc_file
    cdef public bint _pc_ramflag
    cdef public double[:,:] _pc_array
    cdef public bint _pc_outputflag
    cdef double *_pc_outputpointer
    cdef public double[:] ep
    cdef public int _ep_ndim
    cdef public int _ep_length
    cdef public int _ep_length_0
    cdef public bint _ep_diskflag
    cdef public str _ep_path
    cdef FILE *_ep_file
    cdef public bint _ep_ramflag
    cdef public double[:,:] _ep_array
    cdef public bint _ep_outputflag
    cdef double *_ep_outputpointer
    cdef public double[:] epc
    cdef public int _epc_ndim
    cdef public int _epc_length
    cdef public int _epc_length_0
    cdef public bint _epc_diskflag
    cdef public str _epc_path
    cdef FILE *_epc_file
    cdef public bint _epc_ramflag
    cdef public double[:,:] _epc_array
    cdef public bint _epc_outputflag
    cdef double *_epc_outputpointer
    cdef public double[:] ei
    cdef public int _ei_ndim
    cdef public int _ei_length
    cdef public int _ei_length_0
    cdef public bint _ei_diskflag
    cdef public str _ei_path
    cdef FILE *_ei_file
    cdef public bint _ei_ramflag
    cdef public double[:,:] _ei_array
    cdef public bint _ei_outputflag
    cdef double *_ei_outputpointer
    cdef public double[:] tf
    cdef public int _tf_ndim
    cdef public int _tf_length
    cdef public int _tf_length_0
    cdef public bint _tf_diskflag
    cdef public str _tf_path
    cdef FILE *_tf_file
    cdef public bint _tf_ramflag
    cdef public double[:,:] _tf_array
    cdef public bint _tf_outputflag
    cdef double *_tf_outputpointer
    cdef public double[:] glmelt
    cdef public int _glmelt_ndim
    cdef public int _glmelt_length
    cdef public int _glmelt_length_0
    cdef public bint _glmelt_diskflag
    cdef public str _glmelt_path
    cdef FILE *_glmelt_file
    cdef public bint _glmelt_ramflag
    cdef public double[:,:] _glmelt_array
    cdef public bint _glmelt_outputflag
    cdef double *_glmelt_outputpointer
    cdef public double[:] melt
    cdef public int _melt_ndim
    cdef public int _melt_length
    cdef public int _melt_length_0
    cdef public bint _melt_diskflag
    cdef public str _melt_path
    cdef FILE *_melt_file
    cdef public bint _melt_ramflag
    cdef public double[:,:] _melt_array
    cdef public bint _melt_outputflag
    cdef double *_melt_outputpointer
    cdef public double[:] refr
    cdef public int _refr_ndim
    cdef public int _refr_length
    cdef public int _refr_length_0
    cdef public bint _refr_diskflag
    cdef public str _refr_path
    cdef FILE *_refr_file
    cdef public bint _refr_ramflag
    cdef public double[:,:] _refr_array
    cdef public bint _refr_outputflag
    cdef double *_refr_outputpointer
    cdef public double[:] in_
    cdef public int _in__ndim
    cdef public int _in__length
    cdef public int _in__length_0
    cdef public bint _in__diskflag
    cdef public str _in__path
    cdef FILE *_in__file
    cdef public bint _in__ramflag
    cdef public double[:,:] _in__array
    cdef public bint _in__outputflag
    cdef double *_in__outputpointer
    cdef public double[:] r
    cdef public int _r_ndim
    cdef public int _r_length
    cdef public int _r_length_0
    cdef public bint _r_diskflag
    cdef public str _r_path
    cdef FILE *_r_file
    cdef public bint _r_ramflag
    cdef public double[:,:] _r_array
    cdef public bint _r_outputflag
    cdef double *_r_outputpointer
    cdef public double[:] ea
    cdef public int _ea_ndim
    cdef public int _ea_length
    cdef public int _ea_length_0
    cdef public bint _ea_diskflag
    cdef public str _ea_path
    cdef FILE *_ea_file
    cdef public bint _ea_ramflag
    cdef public double[:,:] _ea_array
    cdef public bint _ea_outputflag
    cdef double *_ea_outputpointer
    cdef public double[:] cf
    cdef public int _cf_ndim
    cdef public int _cf_length
    cdef public int _cf_length_0
    cdef public bint _cf_diskflag
    cdef public str _cf_path
    cdef FILE *_cf_file
    cdef public bint _cf_ramflag
    cdef public double[:,:] _cf_array
    cdef public bint _cf_outputflag
    cdef double *_cf_outputpointer
    cdef public double contriarea
    cdef public int _contriarea_ndim
    cdef public int _contriarea_length
    cdef public bint _contriarea_diskflag
    cdef public str _contriarea_path
    cdef FILE *_contriarea_file
    cdef public bint _contriarea_ramflag
    cdef public double[:] _contriarea_array
    cdef public bint _contriarea_outputflag
    cdef double *_contriarea_outputpointer
    cdef public double inuz
    cdef public int _inuz_ndim
    cdef public int _inuz_length
    cdef public bint _inuz_diskflag
    cdef public str _inuz_path
    cdef FILE *_inuz_file
    cdef public bint _inuz_ramflag
    cdef public double[:] _inuz_array
    cdef public bint _inuz_outputflag
    cdef double *_inuz_outputpointer
    cdef public double perc
    cdef public int _perc_ndim
    cdef public int _perc_length
    cdef public bint _perc_diskflag
    cdef public str _perc_path
    cdef FILE *_perc_file
    cdef public bint _perc_ramflag
    cdef public double[:] _perc_array
    cdef public bint _perc_outputflag
    cdef double *_perc_outputpointer
    cdef public double q0
    cdef public int _q0_ndim
    cdef public int _q0_length
    cdef public bint _q0_diskflag
    cdef public str _q0_path
    cdef FILE *_q0_file
    cdef public bint _q0_ramflag
    cdef public double[:] _q0_array
    cdef public bint _q0_outputflag
    cdef double *_q0_outputpointer
    cdef public double[:] el
    cdef public int _el_ndim
    cdef public int _el_length
    cdef public int _el_length_0
    cdef public bint _el_diskflag
    cdef public str _el_path
    cdef FILE *_el_file
    cdef public bint _el_ramflag
    cdef public double[:,:] _el_array
    cdef public bint _el_outputflag
    cdef double *_el_outputpointer
    cdef public double q1
    cdef public int _q1_ndim
    cdef public int _q1_length
    cdef public bint _q1_diskflag
    cdef public str _q1_path
    cdef FILE *_q1_file
    cdef public bint _q1_ramflag
    cdef public double[:] _q1_array
    cdef public bint _q1_outputflag
    cdef double *_q1_outputpointer
    cdef public double inuh
    cdef public int _inuh_ndim
    cdef public int _inuh_length
    cdef public bint _inuh_diskflag
    cdef public str _inuh_path
    cdef FILE *_inuh_file
    cdef public bint _inuh_ramflag
    cdef public double[:] _inuh_array
    cdef public bint _inuh_outputflag
    cdef double *_inuh_outputpointer
    cdef public double outuh
    cdef public int _outuh_ndim
    cdef public int _outuh_length
    cdef public bint _outuh_diskflag
    cdef public str _outuh_path
    cdef FILE *_outuh_file
    cdef public bint _outuh_ramflag
    cdef public double[:] _outuh_array
    cdef public bint _outuh_outputflag
    cdef double *_outuh_outputpointer
    cdef public double qt
    cdef public int _qt_ndim
    cdef public int _qt_length
    cdef public bint _qt_diskflag
    cdef public str _qt_path
    cdef FILE *_qt_file
    cdef public bint _qt_ramflag
    cdef public double[:] _qt_array
    cdef public bint _qt_outputflag
    cdef double *_qt_outputpointer
    cpdef open_files(self, int idx):
        if self._tmean_diskflag:
            self._tmean_file = fopen(str(self._tmean_path).encode(), "rb+")
            fseek(self._tmean_file, idx*8, SEEK_SET)
        if self._tc_diskflag:
            self._tc_file = fopen(str(self._tc_path).encode(), "rb+")
            fseek(self._tc_file, idx*self._tc_length*8, SEEK_SET)
        if self._fracrain_diskflag:
            self._fracrain_file = fopen(str(self._fracrain_path).encode(), "rb+")
            fseek(self._fracrain_file, idx*self._fracrain_length*8, SEEK_SET)
        if self._rfc_diskflag:
            self._rfc_file = fopen(str(self._rfc_path).encode(), "rb+")
            fseek(self._rfc_file, idx*self._rfc_length*8, SEEK_SET)
        if self._sfc_diskflag:
            self._sfc_file = fopen(str(self._sfc_path).encode(), "rb+")
            fseek(self._sfc_file, idx*self._sfc_length*8, SEEK_SET)
        if self._pc_diskflag:
            self._pc_file = fopen(str(self._pc_path).encode(), "rb+")
            fseek(self._pc_file, idx*self._pc_length*8, SEEK_SET)
        if self._ep_diskflag:
            self._ep_file = fopen(str(self._ep_path).encode(), "rb+")
            fseek(self._ep_file, idx*self._ep_length*8, SEEK_SET)
        if self._epc_diskflag:
            self._epc_file = fopen(str(self._epc_path).encode(), "rb+")
            fseek(self._epc_file, idx*self._epc_length*8, SEEK_SET)
        if self._ei_diskflag:
            self._ei_file = fopen(str(self._ei_path).encode(), "rb+")
            fseek(self._ei_file, idx*self._ei_length*8, SEEK_SET)
        if self._tf_diskflag:
            self._tf_file = fopen(str(self._tf_path).encode(), "rb+")
            fseek(self._tf_file, idx*self._tf_length*8, SEEK_SET)
        if self._glmelt_diskflag:
            self._glmelt_file = fopen(str(self._glmelt_path).encode(), "rb+")
            fseek(self._glmelt_file, idx*self._glmelt_length*8, SEEK_SET)
        if self._melt_diskflag:
            self._melt_file = fopen(str(self._melt_path).encode(), "rb+")
            fseek(self._melt_file, idx*self._melt_length*8, SEEK_SET)
        if self._refr_diskflag:
            self._refr_file = fopen(str(self._refr_path).encode(), "rb+")
            fseek(self._refr_file, idx*self._refr_length*8, SEEK_SET)
        if self._in__diskflag:
            self._in__file = fopen(str(self._in__path).encode(), "rb+")
            fseek(self._in__file, idx*self._in__length*8, SEEK_SET)
        if self._r_diskflag:
            self._r_file = fopen(str(self._r_path).encode(), "rb+")
            fseek(self._r_file, idx*self._r_length*8, SEEK_SET)
        if self._ea_diskflag:
            self._ea_file = fopen(str(self._ea_path).encode(), "rb+")
            fseek(self._ea_file, idx*self._ea_length*8, SEEK_SET)
        if self._cf_diskflag:
            self._cf_file = fopen(str(self._cf_path).encode(), "rb+")
            fseek(self._cf_file, idx*self._cf_length*8, SEEK_SET)
        if self._contriarea_diskflag:
            self._contriarea_file = fopen(str(self._contriarea_path).encode(), "rb+")
            fseek(self._contriarea_file, idx*8, SEEK_SET)
        if self._inuz_diskflag:
            self._inuz_file = fopen(str(self._inuz_path).encode(), "rb+")
            fseek(self._inuz_file, idx*8, SEEK_SET)
        if self._perc_diskflag:
            self._perc_file = fopen(str(self._perc_path).encode(), "rb+")
            fseek(self._perc_file, idx*8, SEEK_SET)
        if self._q0_diskflag:
            self._q0_file = fopen(str(self._q0_path).encode(), "rb+")
            fseek(self._q0_file, idx*8, SEEK_SET)
        if self._el_diskflag:
            self._el_file = fopen(str(self._el_path).encode(), "rb+")
            fseek(self._el_file, idx*self._el_length*8, SEEK_SET)
        if self._q1_diskflag:
            self._q1_file = fopen(str(self._q1_path).encode(), "rb+")
            fseek(self._q1_file, idx*8, SEEK_SET)
        if self._inuh_diskflag:
            self._inuh_file = fopen(str(self._inuh_path).encode(), "rb+")
            fseek(self._inuh_file, idx*8, SEEK_SET)
        if self._outuh_diskflag:
            self._outuh_file = fopen(str(self._outuh_path).encode(), "rb+")
            fseek(self._outuh_file, idx*8, SEEK_SET)
        if self._qt_diskflag:
            self._qt_file = fopen(str(self._qt_path).encode(), "rb+")
            fseek(self._qt_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._tmean_diskflag:
            fclose(self._tmean_file)
        if self._tc_diskflag:
            fclose(self._tc_file)
        if self._fracrain_diskflag:
            fclose(self._fracrain_file)
        if self._rfc_diskflag:
            fclose(self._rfc_file)
        if self._sfc_diskflag:
            fclose(self._sfc_file)
        if self._pc_diskflag:
            fclose(self._pc_file)
        if self._ep_diskflag:
            fclose(self._ep_file)
        if self._epc_diskflag:
            fclose(self._epc_file)
        if self._ei_diskflag:
            fclose(self._ei_file)
        if self._tf_diskflag:
            fclose(self._tf_file)
        if self._glmelt_diskflag:
            fclose(self._glmelt_file)
        if self._melt_diskflag:
            fclose(self._melt_file)
        if self._refr_diskflag:
            fclose(self._refr_file)
        if self._in__diskflag:
            fclose(self._in__file)
        if self._r_diskflag:
            fclose(self._r_file)
        if self._ea_diskflag:
            fclose(self._ea_file)
        if self._cf_diskflag:
            fclose(self._cf_file)
        if self._contriarea_diskflag:
            fclose(self._contriarea_file)
        if self._inuz_diskflag:
            fclose(self._inuz_file)
        if self._perc_diskflag:
            fclose(self._perc_file)
        if self._q0_diskflag:
            fclose(self._q0_file)
        if self._el_diskflag:
            fclose(self._el_file)
        if self._q1_diskflag:
            fclose(self._q1_file)
        if self._inuh_diskflag:
            fclose(self._inuh_file)
        if self._outuh_diskflag:
            fclose(self._outuh_file)
        if self._qt_diskflag:
            fclose(self._qt_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._tmean_diskflag:
            fread(&self.tmean, 8, 1, self._tmean_file)
        elif self._tmean_ramflag:
            self.tmean = self._tmean_array[idx]
        if self._tc_diskflag:
            fread(&self.tc[0], 8, self._tc_length, self._tc_file)
        elif self._tc_ramflag:
            for jdx0 in range(self._tc_length_0):
                self.tc[jdx0] = self._tc_array[idx, jdx0]
        if self._fracrain_diskflag:
            fread(&self.fracrain[0], 8, self._fracrain_length, self._fracrain_file)
        elif self._fracrain_ramflag:
            for jdx0 in range(self._fracrain_length_0):
                self.fracrain[jdx0] = self._fracrain_array[idx, jdx0]
        if self._rfc_diskflag:
            fread(&self.rfc[0], 8, self._rfc_length, self._rfc_file)
        elif self._rfc_ramflag:
            for jdx0 in range(self._rfc_length_0):
                self.rfc[jdx0] = self._rfc_array[idx, jdx0]
        if self._sfc_diskflag:
            fread(&self.sfc[0], 8, self._sfc_length, self._sfc_file)
        elif self._sfc_ramflag:
            for jdx0 in range(self._sfc_length_0):
                self.sfc[jdx0] = self._sfc_array[idx, jdx0]
        if self._pc_diskflag:
            fread(&self.pc[0], 8, self._pc_length, self._pc_file)
        elif self._pc_ramflag:
            for jdx0 in range(self._pc_length_0):
                self.pc[jdx0] = self._pc_array[idx, jdx0]
        if self._ep_diskflag:
            fread(&self.ep[0], 8, self._ep_length, self._ep_file)
        elif self._ep_ramflag:
            for jdx0 in range(self._ep_length_0):
                self.ep[jdx0] = self._ep_array[idx, jdx0]
        if self._epc_diskflag:
            fread(&self.epc[0], 8, self._epc_length, self._epc_file)
        elif self._epc_ramflag:
            for jdx0 in range(self._epc_length_0):
                self.epc[jdx0] = self._epc_array[idx, jdx0]
        if self._ei_diskflag:
            fread(&self.ei[0], 8, self._ei_length, self._ei_file)
        elif self._ei_ramflag:
            for jdx0 in range(self._ei_length_0):
                self.ei[jdx0] = self._ei_array[idx, jdx0]
        if self._tf_diskflag:
            fread(&self.tf[0], 8, self._tf_length, self._tf_file)
        elif self._tf_ramflag:
            for jdx0 in range(self._tf_length_0):
                self.tf[jdx0] = self._tf_array[idx, jdx0]
        if self._glmelt_diskflag:
            fread(&self.glmelt[0], 8, self._glmelt_length, self._glmelt_file)
        elif self._glmelt_ramflag:
            for jdx0 in range(self._glmelt_length_0):
                self.glmelt[jdx0] = self._glmelt_array[idx, jdx0]
        if self._melt_diskflag:
            fread(&self.melt[0], 8, self._melt_length, self._melt_file)
        elif self._melt_ramflag:
            for jdx0 in range(self._melt_length_0):
                self.melt[jdx0] = self._melt_array[idx, jdx0]
        if self._refr_diskflag:
            fread(&self.refr[0], 8, self._refr_length, self._refr_file)
        elif self._refr_ramflag:
            for jdx0 in range(self._refr_length_0):
                self.refr[jdx0] = self._refr_array[idx, jdx0]
        if self._in__diskflag:
            fread(&self.in_[0], 8, self._in__length, self._in__file)
        elif self._in__ramflag:
            for jdx0 in range(self._in__length_0):
                self.in_[jdx0] = self._in__array[idx, jdx0]
        if self._r_diskflag:
            fread(&self.r[0], 8, self._r_length, self._r_file)
        elif self._r_ramflag:
            for jdx0 in range(self._r_length_0):
                self.r[jdx0] = self._r_array[idx, jdx0]
        if self._ea_diskflag:
            fread(&self.ea[0], 8, self._ea_length, self._ea_file)
        elif self._ea_ramflag:
            for jdx0 in range(self._ea_length_0):
                self.ea[jdx0] = self._ea_array[idx, jdx0]
        if self._cf_diskflag:
            fread(&self.cf[0], 8, self._cf_length, self._cf_file)
        elif self._cf_ramflag:
            for jdx0 in range(self._cf_length_0):
                self.cf[jdx0] = self._cf_array[idx, jdx0]
        if self._contriarea_diskflag:
            fread(&self.contriarea, 8, 1, self._contriarea_file)
        elif self._contriarea_ramflag:
            self.contriarea = self._contriarea_array[idx]
        if self._inuz_diskflag:
            fread(&self.inuz, 8, 1, self._inuz_file)
        elif self._inuz_ramflag:
            self.inuz = self._inuz_array[idx]
        if self._perc_diskflag:
            fread(&self.perc, 8, 1, self._perc_file)
        elif self._perc_ramflag:
            self.perc = self._perc_array[idx]
        if self._q0_diskflag:
            fread(&self.q0, 8, 1, self._q0_file)
        elif self._q0_ramflag:
            self.q0 = self._q0_array[idx]
        if self._el_diskflag:
            fread(&self.el[0], 8, self._el_length, self._el_file)
        elif self._el_ramflag:
            for jdx0 in range(self._el_length_0):
                self.el[jdx0] = self._el_array[idx, jdx0]
        if self._q1_diskflag:
            fread(&self.q1, 8, 1, self._q1_file)
        elif self._q1_ramflag:
            self.q1 = self._q1_array[idx]
        if self._inuh_diskflag:
            fread(&self.inuh, 8, 1, self._inuh_file)
        elif self._inuh_ramflag:
            self.inuh = self._inuh_array[idx]
        if self._outuh_diskflag:
            fread(&self.outuh, 8, 1, self._outuh_file)
        elif self._outuh_ramflag:
            self.outuh = self._outuh_array[idx]
        if self._qt_diskflag:
            fread(&self.qt, 8, 1, self._qt_file)
        elif self._qt_ramflag:
            self.qt = self._qt_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._tmean_diskflag:
            fwrite(&self.tmean, 8, 1, self._tmean_file)
        elif self._tmean_ramflag:
            self._tmean_array[idx] = self.tmean
        if self._tc_diskflag:
            fwrite(&self.tc[0], 8, self._tc_length, self._tc_file)
        elif self._tc_ramflag:
            for jdx0 in range(self._tc_length_0):
                self._tc_array[idx, jdx0] = self.tc[jdx0]
        if self._fracrain_diskflag:
            fwrite(&self.fracrain[0], 8, self._fracrain_length, self._fracrain_file)
        elif self._fracrain_ramflag:
            for jdx0 in range(self._fracrain_length_0):
                self._fracrain_array[idx, jdx0] = self.fracrain[jdx0]
        if self._rfc_diskflag:
            fwrite(&self.rfc[0], 8, self._rfc_length, self._rfc_file)
        elif self._rfc_ramflag:
            for jdx0 in range(self._rfc_length_0):
                self._rfc_array[idx, jdx0] = self.rfc[jdx0]
        if self._sfc_diskflag:
            fwrite(&self.sfc[0], 8, self._sfc_length, self._sfc_file)
        elif self._sfc_ramflag:
            for jdx0 in range(self._sfc_length_0):
                self._sfc_array[idx, jdx0] = self.sfc[jdx0]
        if self._pc_diskflag:
            fwrite(&self.pc[0], 8, self._pc_length, self._pc_file)
        elif self._pc_ramflag:
            for jdx0 in range(self._pc_length_0):
                self._pc_array[idx, jdx0] = self.pc[jdx0]
        if self._ep_diskflag:
            fwrite(&self.ep[0], 8, self._ep_length, self._ep_file)
        elif self._ep_ramflag:
            for jdx0 in range(self._ep_length_0):
                self._ep_array[idx, jdx0] = self.ep[jdx0]
        if self._epc_diskflag:
            fwrite(&self.epc[0], 8, self._epc_length, self._epc_file)
        elif self._epc_ramflag:
            for jdx0 in range(self._epc_length_0):
                self._epc_array[idx, jdx0] = self.epc[jdx0]
        if self._ei_diskflag:
            fwrite(&self.ei[0], 8, self._ei_length, self._ei_file)
        elif self._ei_ramflag:
            for jdx0 in range(self._ei_length_0):
                self._ei_array[idx, jdx0] = self.ei[jdx0]
        if self._tf_diskflag:
            fwrite(&self.tf[0], 8, self._tf_length, self._tf_file)
        elif self._tf_ramflag:
            for jdx0 in range(self._tf_length_0):
                self._tf_array[idx, jdx0] = self.tf[jdx0]
        if self._glmelt_diskflag:
            fwrite(&self.glmelt[0], 8, self._glmelt_length, self._glmelt_file)
        elif self._glmelt_ramflag:
            for jdx0 in range(self._glmelt_length_0):
                self._glmelt_array[idx, jdx0] = self.glmelt[jdx0]
        if self._melt_diskflag:
            fwrite(&self.melt[0], 8, self._melt_length, self._melt_file)
        elif self._melt_ramflag:
            for jdx0 in range(self._melt_length_0):
                self._melt_array[idx, jdx0] = self.melt[jdx0]
        if self._refr_diskflag:
            fwrite(&self.refr[0], 8, self._refr_length, self._refr_file)
        elif self._refr_ramflag:
            for jdx0 in range(self._refr_length_0):
                self._refr_array[idx, jdx0] = self.refr[jdx0]
        if self._in__diskflag:
            fwrite(&self.in_[0], 8, self._in__length, self._in__file)
        elif self._in__ramflag:
            for jdx0 in range(self._in__length_0):
                self._in__array[idx, jdx0] = self.in_[jdx0]
        if self._r_diskflag:
            fwrite(&self.r[0], 8, self._r_length, self._r_file)
        elif self._r_ramflag:
            for jdx0 in range(self._r_length_0):
                self._r_array[idx, jdx0] = self.r[jdx0]
        if self._ea_diskflag:
            fwrite(&self.ea[0], 8, self._ea_length, self._ea_file)
        elif self._ea_ramflag:
            for jdx0 in range(self._ea_length_0):
                self._ea_array[idx, jdx0] = self.ea[jdx0]
        if self._cf_diskflag:
            fwrite(&self.cf[0], 8, self._cf_length, self._cf_file)
        elif self._cf_ramflag:
            for jdx0 in range(self._cf_length_0):
                self._cf_array[idx, jdx0] = self.cf[jdx0]
        if self._contriarea_diskflag:
            fwrite(&self.contriarea, 8, 1, self._contriarea_file)
        elif self._contriarea_ramflag:
            self._contriarea_array[idx] = self.contriarea
        if self._inuz_diskflag:
            fwrite(&self.inuz, 8, 1, self._inuz_file)
        elif self._inuz_ramflag:
            self._inuz_array[idx] = self.inuz
        if self._perc_diskflag:
            fwrite(&self.perc, 8, 1, self._perc_file)
        elif self._perc_ramflag:
            self._perc_array[idx] = self.perc
        if self._q0_diskflag:
            fwrite(&self.q0, 8, 1, self._q0_file)
        elif self._q0_ramflag:
            self._q0_array[idx] = self.q0
        if self._el_diskflag:
            fwrite(&self.el[0], 8, self._el_length, self._el_file)
        elif self._el_ramflag:
            for jdx0 in range(self._el_length_0):
                self._el_array[idx, jdx0] = self.el[jdx0]
        if self._q1_diskflag:
            fwrite(&self.q1, 8, 1, self._q1_file)
        elif self._q1_ramflag:
            self._q1_array[idx] = self.q1
        if self._inuh_diskflag:
            fwrite(&self.inuh, 8, 1, self._inuh_file)
        elif self._inuh_ramflag:
            self._inuh_array[idx] = self.inuh
        if self._outuh_diskflag:
            fwrite(&self.outuh, 8, 1, self._outuh_file)
        elif self._outuh_ramflag:
            self._outuh_array[idx] = self.outuh
        if self._qt_diskflag:
            fwrite(&self.qt, 8, 1, self._qt_file)
        elif self._qt_ramflag:
            self._qt_array[idx] = self.qt
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "tmean":
            self._tmean_outputpointer = value.p_value
        if name == "contriarea":
            self._contriarea_outputpointer = value.p_value
        if name == "inuz":
            self._inuz_outputpointer = value.p_value
        if name == "perc":
            self._perc_outputpointer = value.p_value
        if name == "q0":
            self._q0_outputpointer = value.p_value
        if name == "q1":
            self._q1_outputpointer = value.p_value
        if name == "inuh":
            self._inuh_outputpointer = value.p_value
        if name == "outuh":
            self._outuh_outputpointer = value.p_value
        if name == "qt":
            self._qt_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._tmean_outputflag:
            self._tmean_outputpointer[0] = self.tmean
        if self._contriarea_outputflag:
            self._contriarea_outputpointer[0] = self.contriarea
        if self._inuz_outputflag:
            self._inuz_outputpointer[0] = self.inuz
        if self._perc_outputflag:
            self._perc_outputpointer[0] = self.perc
        if self._q0_outputflag:
            self._q0_outputpointer[0] = self.q0
        if self._q1_outputflag:
            self._q1_outputpointer[0] = self.q1
        if self._inuh_outputflag:
            self._inuh_outputpointer[0] = self.inuh
        if self._outuh_outputflag:
            self._outuh_outputpointer[0] = self.outuh
        if self._qt_outputflag:
            self._qt_outputpointer[0] = self.qt
@cython.final
cdef class StateSequences:
    cdef public double[:] ic
    cdef public int _ic_ndim
    cdef public int _ic_length
    cdef public int _ic_length_0
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
    cdef public bint _sp_diskflag
    cdef public str _sp_path
    cdef FILE *_sp_file
    cdef public bint _sp_ramflag
    cdef public double[:,:] _sp_array
    cdef public bint _sp_outputflag
    cdef double *_sp_outputpointer
    cdef public double[:] wc
    cdef public int _wc_ndim
    cdef public int _wc_length
    cdef public int _wc_length_0
    cdef public bint _wc_diskflag
    cdef public str _wc_path
    cdef FILE *_wc_file
    cdef public bint _wc_ramflag
    cdef public double[:,:] _wc_array
    cdef public bint _wc_outputflag
    cdef double *_wc_outputpointer
    cdef public double[:] sm
    cdef public int _sm_ndim
    cdef public int _sm_length
    cdef public int _sm_length_0
    cdef public bint _sm_diskflag
    cdef public str _sm_path
    cdef FILE *_sm_file
    cdef public bint _sm_ramflag
    cdef public double[:,:] _sm_array
    cdef public bint _sm_outputflag
    cdef double *_sm_outputpointer
    cdef public double uz
    cdef public int _uz_ndim
    cdef public int _uz_length
    cdef public bint _uz_diskflag
    cdef public str _uz_path
    cdef FILE *_uz_file
    cdef public bint _uz_ramflag
    cdef public double[:] _uz_array
    cdef public bint _uz_outputflag
    cdef double *_uz_outputpointer
    cdef public double lz
    cdef public int _lz_ndim
    cdef public int _lz_length
    cdef public bint _lz_diskflag
    cdef public str _lz_path
    cdef FILE *_lz_file
    cdef public bint _lz_ramflag
    cdef public double[:] _lz_array
    cdef public bint _lz_outputflag
    cdef double *_lz_outputpointer
    cpdef open_files(self, int idx):
        if self._ic_diskflag:
            self._ic_file = fopen(str(self._ic_path).encode(), "rb+")
            fseek(self._ic_file, idx*self._ic_length*8, SEEK_SET)
        if self._sp_diskflag:
            self._sp_file = fopen(str(self._sp_path).encode(), "rb+")
            fseek(self._sp_file, idx*self._sp_length*8, SEEK_SET)
        if self._wc_diskflag:
            self._wc_file = fopen(str(self._wc_path).encode(), "rb+")
            fseek(self._wc_file, idx*self._wc_length*8, SEEK_SET)
        if self._sm_diskflag:
            self._sm_file = fopen(str(self._sm_path).encode(), "rb+")
            fseek(self._sm_file, idx*self._sm_length*8, SEEK_SET)
        if self._uz_diskflag:
            self._uz_file = fopen(str(self._uz_path).encode(), "rb+")
            fseek(self._uz_file, idx*8, SEEK_SET)
        if self._lz_diskflag:
            self._lz_file = fopen(str(self._lz_path).encode(), "rb+")
            fseek(self._lz_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._ic_diskflag:
            fclose(self._ic_file)
        if self._sp_diskflag:
            fclose(self._sp_file)
        if self._wc_diskflag:
            fclose(self._wc_file)
        if self._sm_diskflag:
            fclose(self._sm_file)
        if self._uz_diskflag:
            fclose(self._uz_file)
        if self._lz_diskflag:
            fclose(self._lz_file)
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
        if self._wc_diskflag:
            fread(&self.wc[0], 8, self._wc_length, self._wc_file)
        elif self._wc_ramflag:
            for jdx0 in range(self._wc_length_0):
                self.wc[jdx0] = self._wc_array[idx, jdx0]
        if self._sm_diskflag:
            fread(&self.sm[0], 8, self._sm_length, self._sm_file)
        elif self._sm_ramflag:
            for jdx0 in range(self._sm_length_0):
                self.sm[jdx0] = self._sm_array[idx, jdx0]
        if self._uz_diskflag:
            fread(&self.uz, 8, 1, self._uz_file)
        elif self._uz_ramflag:
            self.uz = self._uz_array[idx]
        if self._lz_diskflag:
            fread(&self.lz, 8, 1, self._lz_file)
        elif self._lz_ramflag:
            self.lz = self._lz_array[idx]
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
        if self._wc_diskflag:
            fwrite(&self.wc[0], 8, self._wc_length, self._wc_file)
        elif self._wc_ramflag:
            for jdx0 in range(self._wc_length_0):
                self._wc_array[idx, jdx0] = self.wc[jdx0]
        if self._sm_diskflag:
            fwrite(&self.sm[0], 8, self._sm_length, self._sm_file)
        elif self._sm_ramflag:
            for jdx0 in range(self._sm_length_0):
                self._sm_array[idx, jdx0] = self.sm[jdx0]
        if self._uz_diskflag:
            fwrite(&self.uz, 8, 1, self._uz_file)
        elif self._uz_ramflag:
            self._uz_array[idx] = self.uz
        if self._lz_diskflag:
            fwrite(&self.lz, 8, 1, self._lz_file)
        elif self._lz_ramflag:
            self._lz_array[idx] = self.lz
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "uz":
            self._uz_outputpointer = value.p_value
        if name == "lz":
            self._lz_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._uz_outputflag:
            self._uz_outputpointer[0] = self.uz
        if self._lz_outputflag:
            self._lz_outputpointer[0] = self.lz
@cython.final
cdef class LogSequences:
    cdef public double[:] quh
    cdef public int _quh_ndim
    cdef public int _quh_length
    cdef public int _quh_length_0
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
        self.load_data()
        self.run()
        self.new2old()
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
        for jdx0 in range(self.sequences.states._wc_length_0):
            self.sequences.old_states.wc[jdx0] = self.sequences.new_states.wc[jdx0]
        for jdx0 in range(self.sequences.states._sm_length_0):
            self.sequences.old_states.sm[jdx0] = self.sequences.new_states.sm[jdx0]
        self.sequences.old_states.uz = self.sequences.new_states.uz
        self.sequences.old_states.lz = self.sequences.new_states.lz
    cpdef inline void run(self) nogil:
        self.calc_tc_v1()
        self.calc_tmean_v1()
        self.calc_fracrain_v1()
        self.calc_rfc_sfc_v1()
        self.calc_pc_v1()
        self.calc_ep_v1()
        self.calc_epc_v1()
        self.calc_tf_ic_v1()
        self.calc_ei_ic_v1()
        self.calc_sp_wc_v1()
        self.calc_melt_sp_wc_v1()
        self.calc_refr_sp_wc_v1()
        self.calc_in_wc_v1()
        self.calc_glmelt_in_v1()
        self.calc_r_sm_v1()
        self.calc_cf_sm_v1()
        self.calc_ea_sm_v1()
        self.calc_inuz_v1()
        self.calc_contriarea_v1()
        self.calc_q0_perc_uz_v1()
        self.calc_lz_v1()
        self.calc_el_lz_v1()
        self.calc_q1_lz_v1()
        self.calc_inuh_v1()
        self.calc_outuh_quh_v1()
        self.calc_qt_v1()
    cpdef inline void update_inlets(self) nogil:
        pass
    cpdef inline void update_outlets(self) nogil:
        self.pass_q_v1()
    cpdef inline void update_receivers(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_senders(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_outputs(self) nogil:
        self.sequences.fluxes.update_outputs()
        self.sequences.states.update_outputs()

    cpdef inline void calc_tc_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.tc[k] = self.sequences.inputs.t - self.parameters.control.tcalt[k] * (self.parameters.control.zonez[k] - self.parameters.control.zrelt)
    cpdef inline void calc_tmean_v1(self)  nogil:
        cdef int k
        self.sequences.fluxes.tmean = 0.0
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.tmean = self.sequences.fluxes.tmean + (self.parameters.derived.relzonearea[k] * self.sequences.fluxes.tc[k])
    cpdef inline void calc_fracrain_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.sequences.fluxes.tc[k] >= (self.parameters.control.tt[k] + self.parameters.control.ttint[k] / 2.0):
                self.sequences.fluxes.fracrain[k] = 1.0
            elif self.sequences.fluxes.tc[k] <= (self.parameters.control.tt[k] - self.parameters.control.ttint[k] / 2.0):
                self.sequences.fluxes.fracrain[k] = 0.0
            else:
                self.sequences.fluxes.fracrain[k] = (                    self.sequences.fluxes.tc[k] - (self.parameters.control.tt[k] - self.parameters.control.ttint[k] / 2.0)                ) / self.parameters.control.ttint[k]
    cpdef inline void calc_rfc_sfc_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.rfc[k] = self.sequences.fluxes.fracrain[k] * self.parameters.control.rfcf[k]
            self.sequences.fluxes.sfc[k] = (1.0 - self.sequences.fluxes.fracrain[k]) * self.parameters.control.sfcf[k]
    cpdef inline void calc_pc_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.pc[k] = self.sequences.inputs.p * (1.0 + self.parameters.control.pcalt[k] * (self.parameters.control.zonez[k] - self.parameters.control.zrelp))
            if self.sequences.fluxes.pc[k] <= 0.0:
                self.sequences.fluxes.pc[k] = 0.0
            else:
                self.sequences.fluxes.pc[k] = self.sequences.fluxes.pc[k] * (self.parameters.control.pcorr[k] * (self.sequences.fluxes.rfc[k] + self.sequences.fluxes.sfc[k]))
    cpdef inline void calc_ep_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.ep[k] = self.sequences.inputs.epn * (1.0 + self.parameters.control.etf[k] * (self.sequences.fluxes.tmean - self.sequences.inputs.tn))
            self.sequences.fluxes.ep[k] = min(max(self.sequences.fluxes.ep[k], 0.0), 2.0 * self.sequences.inputs.epn)
    cpdef inline void calc_epc_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.epc[k] = (                self.sequences.fluxes.ep[k]                * self.parameters.control.ecorr[k]                * (1.0 - self.parameters.control.ecalt[k] * (self.parameters.control.zonez[k] - self.parameters.control.zrele))            )
            if self.sequences.fluxes.epc[k] <= 0.0:
                self.sequences.fluxes.epc[k] = 0.0
            else:
                self.sequences.fluxes.epc[k] = self.sequences.fluxes.epc[k] * (exp(-self.parameters.control.epf[k] * self.sequences.fluxes.pc[k]))
    cpdef inline void calc_tf_ic_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                self.sequences.fluxes.tf[k] = max(self.sequences.fluxes.pc[k] - (self.parameters.control.icmax[k] - self.sequences.states.ic[k]), 0.0)
                self.sequences.states.ic[k] = self.sequences.states.ic[k] + (self.sequences.fluxes.pc[k] - self.sequences.fluxes.tf[k])
            else:
                self.sequences.fluxes.tf[k] = self.sequences.fluxes.pc[k]
                self.sequences.states.ic[k] = 0.0
    cpdef inline void calc_ei_ic_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                self.sequences.fluxes.ei[k] = min(self.sequences.fluxes.epc[k], self.sequences.states.ic[k])
                self.sequences.states.ic[k] = self.sequences.states.ic[k] - (self.sequences.fluxes.ei[k])
            else:
                self.sequences.fluxes.ei[k] = 0.0
                self.sequences.states.ic[k] = 0.0
    cpdef inline void calc_sp_wc_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                if (self.sequences.fluxes.rfc[k] + self.sequences.fluxes.sfc[k]) > 0.0:
                    self.sequences.states.wc[k] = self.sequences.states.wc[k] + (self.sequences.fluxes.tf[k] * self.sequences.fluxes.rfc[k] / (self.sequences.fluxes.rfc[k] + self.sequences.fluxes.sfc[k]))
                    self.sequences.states.sp[k] = self.sequences.states.sp[k] + (self.sequences.fluxes.tf[k] * self.sequences.fluxes.sfc[k] / (self.sequences.fluxes.rfc[k] + self.sequences.fluxes.sfc[k]))
            else:
                self.sequences.states.wc[k] = 0.0
                self.sequences.states.sp[k] = 0.0
    cpdef inline void calc_melt_sp_wc_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                if self.sequences.fluxes.tc[k] > self.parameters.derived.ttm[k]:
                    self.sequences.fluxes.melt[k] = min(                        self.parameters.control.cfmax[k] * (self.sequences.fluxes.tc[k] - self.parameters.derived.ttm[k]), self.sequences.states.sp[k]                    )
                    self.sequences.states.sp[k] = self.sequences.states.sp[k] - (self.sequences.fluxes.melt[k])
                    self.sequences.states.wc[k] = self.sequences.states.wc[k] + (self.sequences.fluxes.melt[k])
                else:
                    self.sequences.fluxes.melt[k] = 0.0
            else:
                self.sequences.fluxes.melt[k] = 0.0
                self.sequences.states.wc[k] = 0.0
                self.sequences.states.sp[k] = 0.0
    cpdef inline void calc_refr_sp_wc_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                if self.sequences.fluxes.tc[k] < self.parameters.derived.ttm[k]:
                    self.sequences.fluxes.refr[k] = min(                        self.parameters.control.cfr[k] * self.parameters.control.cfmax[k] * (self.parameters.derived.ttm[k] - self.sequences.fluxes.tc[k]), self.sequences.states.wc[k]                    )
                    self.sequences.states.sp[k] = self.sequences.states.sp[k] + (self.sequences.fluxes.refr[k])
                    self.sequences.states.wc[k] = self.sequences.states.wc[k] - (self.sequences.fluxes.refr[k])
                else:
                    self.sequences.fluxes.refr[k] = 0.0
            else:
                self.sequences.fluxes.refr[k] = 0.0
                self.sequences.states.wc[k] = 0.0
                self.sequences.states.sp[k] = 0.0
    cpdef inline void calc_in_wc_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                self.sequences.fluxes.in_[k] = max(self.sequences.states.wc[k] - self.parameters.control.whc[k] * self.sequences.states.sp[k], 0.0)
                self.sequences.states.wc[k] = self.sequences.states.wc[k] - (self.sequences.fluxes.in_[k])
            else:
                self.sequences.fluxes.in_[k] = self.sequences.fluxes.tf[k]
                self.sequences.states.wc[k] = 0.0
    cpdef inline void calc_glmelt_in_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if (                (self.parameters.control.zonetype[k] == GLACIER)                and (self.sequences.states.sp[k] <= 0.0)                and (self.sequences.fluxes.tc[k] > self.parameters.derived.ttm[k])            ):
                self.sequences.fluxes.glmelt[k] = self.parameters.control.gmelt[k] * (self.sequences.fluxes.tc[k] - self.parameters.derived.ttm[k])
                self.sequences.fluxes.in_[k] = self.sequences.fluxes.in_[k] + (self.sequences.fluxes.glmelt[k])
            else:
                self.sequences.fluxes.glmelt[k] = 0.0
    cpdef inline void calc_r_sm_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                if self.parameters.control.fc[k] > 0.0:
                    self.sequences.fluxes.r[k] = self.sequences.fluxes.in_[k] * (self.sequences.states.sm[k] / self.parameters.control.fc[k]) ** self.parameters.control.beta[k]
                    self.sequences.fluxes.r[k] = max(self.sequences.fluxes.r[k], self.sequences.states.sm[k] + self.sequences.fluxes.in_[k] - self.parameters.control.fc[k])
                else:
                    self.sequences.fluxes.r[k] = self.sequences.fluxes.in_[k]
                self.sequences.states.sm[k] = self.sequences.states.sm[k] + (self.sequences.fluxes.in_[k] - self.sequences.fluxes.r[k])
            else:
                self.sequences.fluxes.r[k] = self.sequences.fluxes.in_[k]
                self.sequences.states.sm[k] = 0.0
    cpdef inline void calc_cf_sm_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                if self.parameters.control.fc[k] > 0.0:
                    self.sequences.fluxes.cf[k] = self.parameters.control.cflux[k] * (1.0 - self.sequences.states.sm[k] / self.parameters.control.fc[k])
                    self.sequences.fluxes.cf[k] = min(self.sequences.fluxes.cf[k], self.sequences.states.uz + self.sequences.fluxes.r[k])
                    self.sequences.fluxes.cf[k] = min(self.sequences.fluxes.cf[k], self.parameters.control.fc[k] - self.sequences.states.sm[k])
                else:
                    self.sequences.fluxes.cf[k] = 0.0
                self.sequences.states.sm[k] = self.sequences.states.sm[k] + (self.sequences.fluxes.cf[k])
            else:
                self.sequences.fluxes.cf[k] = 0.0
                self.sequences.states.sm[k] = 0.0
    cpdef inline void calc_ea_sm_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                if self.sequences.states.sp[k] <= 0.0:
                    if (self.parameters.control.lp[k] * self.parameters.control.fc[k]) > 0.0:
                        self.sequences.fluxes.ea[k] = self.sequences.fluxes.epc[k] * self.sequences.states.sm[k] / (self.parameters.control.lp[k] * self.parameters.control.fc[k])
                        self.sequences.fluxes.ea[k] = min(self.sequences.fluxes.ea[k], self.sequences.fluxes.epc[k])
                    else:
                        self.sequences.fluxes.ea[k] = self.sequences.fluxes.epc[k]
                    self.sequences.fluxes.ea[k] = self.sequences.fluxes.ea[k] - (max(                        self.parameters.control.ered[k] * (self.sequences.fluxes.ea[k] + self.sequences.fluxes.ei[k] - self.sequences.fluxes.epc[k]), 0.0                    ))
                    self.sequences.fluxes.ea[k] = min(self.sequences.fluxes.ea[k], self.sequences.states.sm[k])
                else:
                    self.sequences.fluxes.ea[k] = 0.0
                self.sequences.states.sm[k] = self.sequences.states.sm[k] - (self.sequences.fluxes.ea[k])
            else:
                self.sequences.fluxes.ea[k] = 0.0
                self.sequences.states.sm[k] = 0.0
    cpdef inline void calc_inuz_v1(self)  nogil:
        cdef int k
        self.sequences.fluxes.inuz = 0.0
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                self.sequences.fluxes.inuz = self.sequences.fluxes.inuz + (self.parameters.derived.rellandzonearea[k] * (self.sequences.fluxes.r[k] - self.sequences.fluxes.cf[k]))
    cpdef inline void calc_contriarea_v1(self)  nogil:
        cdef int k
        self.sequences.fluxes.contriarea = 1.0
        if self.parameters.control.resparea and (self.parameters.derived.relsoilarea > 0.0):
            for k in range(self.parameters.control.nmbzones):
                if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                    if self.parameters.control.fc[k] > 0.0:
                        self.sequences.fluxes.contriarea = self.sequences.fluxes.contriarea * ((                            self.sequences.states.sm[k] / self.parameters.control.fc[k]                        ) ** self.parameters.derived.relsoilzonearea[k])
            self.sequences.fluxes.contriarea = self.sequences.fluxes.contriarea ** (self.parameters.control.beta[k])
    cpdef inline void calc_q0_perc_uz_v1(self)  nogil:
        cdef double d_q0
        cdef double d_perc
        cdef int dummy
        self.sequences.fluxes.perc = 0.0
        self.sequences.fluxes.q0 = 0.0
        for dummy in range(self.parameters.control.recstep):
            self.sequences.states.uz = self.sequences.states.uz + (self.parameters.derived.dt * self.sequences.fluxes.inuz)
            d_perc = min(self.parameters.derived.dt * self.parameters.control.percmax * self.sequences.fluxes.contriarea, self.sequences.states.uz)
            self.sequences.states.uz = self.sequences.states.uz - (d_perc)
            self.sequences.fluxes.perc = self.sequences.fluxes.perc + (d_perc)
            if self.sequences.states.uz > 0.0:
                if self.sequences.fluxes.contriarea > 0.0:
                    d_q0 = (                        self.parameters.derived.dt * self.parameters.control.k * (self.sequences.states.uz / self.sequences.fluxes.contriarea) ** (1.0 + self.parameters.control.alpha)                    )
                    d_q0 = min(d_q0, self.sequences.states.uz)
                else:
                    d_q0 = self.sequences.states.uz
                self.sequences.states.uz = self.sequences.states.uz - (d_q0)
                self.sequences.fluxes.q0 = self.sequences.fluxes.q0 + (d_q0)
    cpdef inline void calc_lz_v1(self)  nogil:
        cdef int k
        self.sequences.states.lz = self.sequences.states.lz + (self.parameters.derived.rellandarea * self.sequences.fluxes.perc)
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] == ILAKE:
                self.sequences.states.lz = self.sequences.states.lz + (self.parameters.derived.relzonearea[k] * self.sequences.fluxes.pc[k])
    cpdef inline void calc_el_lz_v1(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if (self.parameters.control.zonetype[k] == ILAKE) and (self.sequences.fluxes.tc[k] > self.parameters.control.ttice[k]):
                self.sequences.fluxes.el[k] = self.sequences.fluxes.epc[k]
                self.sequences.states.lz = self.sequences.states.lz - (self.parameters.derived.relzonearea[k] * self.sequences.fluxes.el[k])
            else:
                self.sequences.fluxes.el[k] = 0.0
    cpdef inline void calc_q1_lz_v1(self)  nogil:
        if self.sequences.states.lz > 0.0:
            self.sequences.fluxes.q1 = self.parameters.control.k4 * self.sequences.states.lz ** (1.0 + self.parameters.control.gamma)
        else:
            self.sequences.fluxes.q1 = 0.0
        self.sequences.states.lz = self.sequences.states.lz - (self.sequences.fluxes.q1)
    cpdef inline void calc_inuh_v1(self)  nogil:
        self.sequences.fluxes.inuh = self.parameters.derived.rellandarea * self.sequences.fluxes.q0 + self.sequences.fluxes.q1
    cpdef inline void calc_outuh_quh_v1(self)  nogil:
        cdef int jdx
        self.sequences.fluxes.outuh = self.parameters.derived.uh[0] * self.sequences.fluxes.inuh + self.sequences.logs.quh[0]
        for jdx in range(1, len(self.parameters.derived.uh)):
            self.sequences.logs.quh[jdx - 1] = self.parameters.derived.uh[jdx] * self.sequences.fluxes.inuh + self.sequences.logs.quh[jdx]
    cpdef inline void calc_qt_v1(self)  nogil:
        self.sequences.fluxes.qt = max(self.parameters.derived.qfactor * self.sequences.fluxes.outuh - self.parameters.control.abstr, 0.0)
    cpdef inline void calc_tc(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.tc[k] = self.sequences.inputs.t - self.parameters.control.tcalt[k] * (self.parameters.control.zonez[k] - self.parameters.control.zrelt)
    cpdef inline void calc_tmean(self)  nogil:
        cdef int k
        self.sequences.fluxes.tmean = 0.0
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.tmean = self.sequences.fluxes.tmean + (self.parameters.derived.relzonearea[k] * self.sequences.fluxes.tc[k])
    cpdef inline void calc_fracrain(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.sequences.fluxes.tc[k] >= (self.parameters.control.tt[k] + self.parameters.control.ttint[k] / 2.0):
                self.sequences.fluxes.fracrain[k] = 1.0
            elif self.sequences.fluxes.tc[k] <= (self.parameters.control.tt[k] - self.parameters.control.ttint[k] / 2.0):
                self.sequences.fluxes.fracrain[k] = 0.0
            else:
                self.sequences.fluxes.fracrain[k] = (                    self.sequences.fluxes.tc[k] - (self.parameters.control.tt[k] - self.parameters.control.ttint[k] / 2.0)                ) / self.parameters.control.ttint[k]
    cpdef inline void calc_rfc_sfc(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.rfc[k] = self.sequences.fluxes.fracrain[k] * self.parameters.control.rfcf[k]
            self.sequences.fluxes.sfc[k] = (1.0 - self.sequences.fluxes.fracrain[k]) * self.parameters.control.sfcf[k]
    cpdef inline void calc_pc(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.pc[k] = self.sequences.inputs.p * (1.0 + self.parameters.control.pcalt[k] * (self.parameters.control.zonez[k] - self.parameters.control.zrelp))
            if self.sequences.fluxes.pc[k] <= 0.0:
                self.sequences.fluxes.pc[k] = 0.0
            else:
                self.sequences.fluxes.pc[k] = self.sequences.fluxes.pc[k] * (self.parameters.control.pcorr[k] * (self.sequences.fluxes.rfc[k] + self.sequences.fluxes.sfc[k]))
    cpdef inline void calc_ep(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.ep[k] = self.sequences.inputs.epn * (1.0 + self.parameters.control.etf[k] * (self.sequences.fluxes.tmean - self.sequences.inputs.tn))
            self.sequences.fluxes.ep[k] = min(max(self.sequences.fluxes.ep[k], 0.0), 2.0 * self.sequences.inputs.epn)
    cpdef inline void calc_epc(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            self.sequences.fluxes.epc[k] = (                self.sequences.fluxes.ep[k]                * self.parameters.control.ecorr[k]                * (1.0 - self.parameters.control.ecalt[k] * (self.parameters.control.zonez[k] - self.parameters.control.zrele))            )
            if self.sequences.fluxes.epc[k] <= 0.0:
                self.sequences.fluxes.epc[k] = 0.0
            else:
                self.sequences.fluxes.epc[k] = self.sequences.fluxes.epc[k] * (exp(-self.parameters.control.epf[k] * self.sequences.fluxes.pc[k]))
    cpdef inline void calc_tf_ic(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                self.sequences.fluxes.tf[k] = max(self.sequences.fluxes.pc[k] - (self.parameters.control.icmax[k] - self.sequences.states.ic[k]), 0.0)
                self.sequences.states.ic[k] = self.sequences.states.ic[k] + (self.sequences.fluxes.pc[k] - self.sequences.fluxes.tf[k])
            else:
                self.sequences.fluxes.tf[k] = self.sequences.fluxes.pc[k]
                self.sequences.states.ic[k] = 0.0
    cpdef inline void calc_ei_ic(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                self.sequences.fluxes.ei[k] = min(self.sequences.fluxes.epc[k], self.sequences.states.ic[k])
                self.sequences.states.ic[k] = self.sequences.states.ic[k] - (self.sequences.fluxes.ei[k])
            else:
                self.sequences.fluxes.ei[k] = 0.0
                self.sequences.states.ic[k] = 0.0
    cpdef inline void calc_sp_wc(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                if (self.sequences.fluxes.rfc[k] + self.sequences.fluxes.sfc[k]) > 0.0:
                    self.sequences.states.wc[k] = self.sequences.states.wc[k] + (self.sequences.fluxes.tf[k] * self.sequences.fluxes.rfc[k] / (self.sequences.fluxes.rfc[k] + self.sequences.fluxes.sfc[k]))
                    self.sequences.states.sp[k] = self.sequences.states.sp[k] + (self.sequences.fluxes.tf[k] * self.sequences.fluxes.sfc[k] / (self.sequences.fluxes.rfc[k] + self.sequences.fluxes.sfc[k]))
            else:
                self.sequences.states.wc[k] = 0.0
                self.sequences.states.sp[k] = 0.0
    cpdef inline void calc_melt_sp_wc(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                if self.sequences.fluxes.tc[k] > self.parameters.derived.ttm[k]:
                    self.sequences.fluxes.melt[k] = min(                        self.parameters.control.cfmax[k] * (self.sequences.fluxes.tc[k] - self.parameters.derived.ttm[k]), self.sequences.states.sp[k]                    )
                    self.sequences.states.sp[k] = self.sequences.states.sp[k] - (self.sequences.fluxes.melt[k])
                    self.sequences.states.wc[k] = self.sequences.states.wc[k] + (self.sequences.fluxes.melt[k])
                else:
                    self.sequences.fluxes.melt[k] = 0.0
            else:
                self.sequences.fluxes.melt[k] = 0.0
                self.sequences.states.wc[k] = 0.0
                self.sequences.states.sp[k] = 0.0
    cpdef inline void calc_refr_sp_wc(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                if self.sequences.fluxes.tc[k] < self.parameters.derived.ttm[k]:
                    self.sequences.fluxes.refr[k] = min(                        self.parameters.control.cfr[k] * self.parameters.control.cfmax[k] * (self.parameters.derived.ttm[k] - self.sequences.fluxes.tc[k]), self.sequences.states.wc[k]                    )
                    self.sequences.states.sp[k] = self.sequences.states.sp[k] + (self.sequences.fluxes.refr[k])
                    self.sequences.states.wc[k] = self.sequences.states.wc[k] - (self.sequences.fluxes.refr[k])
                else:
                    self.sequences.fluxes.refr[k] = 0.0
            else:
                self.sequences.fluxes.refr[k] = 0.0
                self.sequences.states.wc[k] = 0.0
                self.sequences.states.sp[k] = 0.0
    cpdef inline void calc_in_wc(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                self.sequences.fluxes.in_[k] = max(self.sequences.states.wc[k] - self.parameters.control.whc[k] * self.sequences.states.sp[k], 0.0)
                self.sequences.states.wc[k] = self.sequences.states.wc[k] - (self.sequences.fluxes.in_[k])
            else:
                self.sequences.fluxes.in_[k] = self.sequences.fluxes.tf[k]
                self.sequences.states.wc[k] = 0.0
    cpdef inline void calc_glmelt_in(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if (                (self.parameters.control.zonetype[k] == GLACIER)                and (self.sequences.states.sp[k] <= 0.0)                and (self.sequences.fluxes.tc[k] > self.parameters.derived.ttm[k])            ):
                self.sequences.fluxes.glmelt[k] = self.parameters.control.gmelt[k] * (self.sequences.fluxes.tc[k] - self.parameters.derived.ttm[k])
                self.sequences.fluxes.in_[k] = self.sequences.fluxes.in_[k] + (self.sequences.fluxes.glmelt[k])
            else:
                self.sequences.fluxes.glmelt[k] = 0.0
    cpdef inline void calc_r_sm(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                if self.parameters.control.fc[k] > 0.0:
                    self.sequences.fluxes.r[k] = self.sequences.fluxes.in_[k] * (self.sequences.states.sm[k] / self.parameters.control.fc[k]) ** self.parameters.control.beta[k]
                    self.sequences.fluxes.r[k] = max(self.sequences.fluxes.r[k], self.sequences.states.sm[k] + self.sequences.fluxes.in_[k] - self.parameters.control.fc[k])
                else:
                    self.sequences.fluxes.r[k] = self.sequences.fluxes.in_[k]
                self.sequences.states.sm[k] = self.sequences.states.sm[k] + (self.sequences.fluxes.in_[k] - self.sequences.fluxes.r[k])
            else:
                self.sequences.fluxes.r[k] = self.sequences.fluxes.in_[k]
                self.sequences.states.sm[k] = 0.0
    cpdef inline void calc_cf_sm(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                if self.parameters.control.fc[k] > 0.0:
                    self.sequences.fluxes.cf[k] = self.parameters.control.cflux[k] * (1.0 - self.sequences.states.sm[k] / self.parameters.control.fc[k])
                    self.sequences.fluxes.cf[k] = min(self.sequences.fluxes.cf[k], self.sequences.states.uz + self.sequences.fluxes.r[k])
                    self.sequences.fluxes.cf[k] = min(self.sequences.fluxes.cf[k], self.parameters.control.fc[k] - self.sequences.states.sm[k])
                else:
                    self.sequences.fluxes.cf[k] = 0.0
                self.sequences.states.sm[k] = self.sequences.states.sm[k] + (self.sequences.fluxes.cf[k])
            else:
                self.sequences.fluxes.cf[k] = 0.0
                self.sequences.states.sm[k] = 0.0
    cpdef inline void calc_ea_sm(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                if self.sequences.states.sp[k] <= 0.0:
                    if (self.parameters.control.lp[k] * self.parameters.control.fc[k]) > 0.0:
                        self.sequences.fluxes.ea[k] = self.sequences.fluxes.epc[k] * self.sequences.states.sm[k] / (self.parameters.control.lp[k] * self.parameters.control.fc[k])
                        self.sequences.fluxes.ea[k] = min(self.sequences.fluxes.ea[k], self.sequences.fluxes.epc[k])
                    else:
                        self.sequences.fluxes.ea[k] = self.sequences.fluxes.epc[k]
                    self.sequences.fluxes.ea[k] = self.sequences.fluxes.ea[k] - (max(                        self.parameters.control.ered[k] * (self.sequences.fluxes.ea[k] + self.sequences.fluxes.ei[k] - self.sequences.fluxes.epc[k]), 0.0                    ))
                    self.sequences.fluxes.ea[k] = min(self.sequences.fluxes.ea[k], self.sequences.states.sm[k])
                else:
                    self.sequences.fluxes.ea[k] = 0.0
                self.sequences.states.sm[k] = self.sequences.states.sm[k] - (self.sequences.fluxes.ea[k])
            else:
                self.sequences.fluxes.ea[k] = 0.0
                self.sequences.states.sm[k] = 0.0
    cpdef inline void calc_inuz(self)  nogil:
        cdef int k
        self.sequences.fluxes.inuz = 0.0
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] != ILAKE:
                self.sequences.fluxes.inuz = self.sequences.fluxes.inuz + (self.parameters.derived.rellandzonearea[k] * (self.sequences.fluxes.r[k] - self.sequences.fluxes.cf[k]))
    cpdef inline void calc_contriarea(self)  nogil:
        cdef int k
        self.sequences.fluxes.contriarea = 1.0
        if self.parameters.control.resparea and (self.parameters.derived.relsoilarea > 0.0):
            for k in range(self.parameters.control.nmbzones):
                if self.parameters.control.zonetype[k] in (FIELD, FOREST):
                    if self.parameters.control.fc[k] > 0.0:
                        self.sequences.fluxes.contriarea = self.sequences.fluxes.contriarea * ((                            self.sequences.states.sm[k] / self.parameters.control.fc[k]                        ) ** self.parameters.derived.relsoilzonearea[k])
            self.sequences.fluxes.contriarea = self.sequences.fluxes.contriarea ** (self.parameters.control.beta[k])
    cpdef inline void calc_q0_perc_uz(self)  nogil:
        cdef double d_q0
        cdef double d_perc
        cdef int dummy
        self.sequences.fluxes.perc = 0.0
        self.sequences.fluxes.q0 = 0.0
        for dummy in range(self.parameters.control.recstep):
            self.sequences.states.uz = self.sequences.states.uz + (self.parameters.derived.dt * self.sequences.fluxes.inuz)
            d_perc = min(self.parameters.derived.dt * self.parameters.control.percmax * self.sequences.fluxes.contriarea, self.sequences.states.uz)
            self.sequences.states.uz = self.sequences.states.uz - (d_perc)
            self.sequences.fluxes.perc = self.sequences.fluxes.perc + (d_perc)
            if self.sequences.states.uz > 0.0:
                if self.sequences.fluxes.contriarea > 0.0:
                    d_q0 = (                        self.parameters.derived.dt * self.parameters.control.k * (self.sequences.states.uz / self.sequences.fluxes.contriarea) ** (1.0 + self.parameters.control.alpha)                    )
                    d_q0 = min(d_q0, self.sequences.states.uz)
                else:
                    d_q0 = self.sequences.states.uz
                self.sequences.states.uz = self.sequences.states.uz - (d_q0)
                self.sequences.fluxes.q0 = self.sequences.fluxes.q0 + (d_q0)
    cpdef inline void calc_lz(self)  nogil:
        cdef int k
        self.sequences.states.lz = self.sequences.states.lz + (self.parameters.derived.rellandarea * self.sequences.fluxes.perc)
        for k in range(self.parameters.control.nmbzones):
            if self.parameters.control.zonetype[k] == ILAKE:
                self.sequences.states.lz = self.sequences.states.lz + (self.parameters.derived.relzonearea[k] * self.sequences.fluxes.pc[k])
    cpdef inline void calc_el_lz(self)  nogil:
        cdef int k
        for k in range(self.parameters.control.nmbzones):
            if (self.parameters.control.zonetype[k] == ILAKE) and (self.sequences.fluxes.tc[k] > self.parameters.control.ttice[k]):
                self.sequences.fluxes.el[k] = self.sequences.fluxes.epc[k]
                self.sequences.states.lz = self.sequences.states.lz - (self.parameters.derived.relzonearea[k] * self.sequences.fluxes.el[k])
            else:
                self.sequences.fluxes.el[k] = 0.0
    cpdef inline void calc_q1_lz(self)  nogil:
        if self.sequences.states.lz > 0.0:
            self.sequences.fluxes.q1 = self.parameters.control.k4 * self.sequences.states.lz ** (1.0 + self.parameters.control.gamma)
        else:
            self.sequences.fluxes.q1 = 0.0
        self.sequences.states.lz = self.sequences.states.lz - (self.sequences.fluxes.q1)
    cpdef inline void calc_inuh(self)  nogil:
        self.sequences.fluxes.inuh = self.parameters.derived.rellandarea * self.sequences.fluxes.q0 + self.sequences.fluxes.q1
    cpdef inline void calc_outuh_quh(self)  nogil:
        cdef int jdx
        self.sequences.fluxes.outuh = self.parameters.derived.uh[0] * self.sequences.fluxes.inuh + self.sequences.logs.quh[0]
        for jdx in range(1, len(self.parameters.derived.uh)):
            self.sequences.logs.quh[jdx - 1] = self.parameters.derived.uh[jdx] * self.sequences.fluxes.inuh + self.sequences.logs.quh[jdx]
    cpdef inline void calc_qt(self)  nogil:
        self.sequences.fluxes.qt = max(self.parameters.derived.qfactor * self.sequences.fluxes.outuh - self.parameters.control.abstr, 0.0)
    cpdef inline void pass_q_v1(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.qt)
    cpdef inline void pass_q(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.qt)
