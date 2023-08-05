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
cdef public bint TYPE_CHECKING = False
@cython.final
cdef class Parameters:
    cdef public ControlParameters control
    cdef public DerivedParameters derived
    cdef public FixedParameters fixed
    cdef public SolverParameters solver
@cython.final
cdef class ControlParameters:
    cdef public double laen
    cdef public double gef
    cdef public numpy.int32_t gts
    cdef public double hm
    cdef public double bm
    cdef public double bnm
    cdef public double[:] bv
    cdef public double[:] bbv
    cdef public double[:] bnv
    cdef public double[:] bnvr
    cdef public double skm
    cdef public double[:] skv
    cdef public double ekm
    cdef public double[:] ekv
    cdef public double hr
@cython.final
cdef class DerivedParameters:
    cdef public double sek
    cdef public double[:] hv
    cdef public double mfm
    cdef public double[:] mfv
    cdef public double bnmf
    cdef public double[:] bnvf
    cdef public double[:] bnvrf
    cdef public double hrp
@cython.final
cdef class FixedParameters:
    cdef public double wbmin
    cdef public double wbreg
@cython.final
cdef class SolverParameters:
    cdef public double abserrormax
    cdef public double relerrormax
    cdef public double reldtmin
    cdef public double reldtmax
@cython.final
cdef class Sequences:
    cdef public InletSequences inlets
    cdef public FluxSequences fluxes
    cdef public StateSequences states
    cdef public AideSequences aides
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
cdef class FluxSequences:
    cdef public double qz
    cdef public int _qz_ndim
    cdef public int _qz_length
    cdef public bint _qz_diskflag
    cdef public str _qz_path
    cdef FILE *_qz_file
    cdef public bint _qz_ramflag
    cdef public double[:] _qz_array
    cdef public bint _qz_outputflag
    cdef double *_qz_outputpointer
    cdef public double[:] qg
    cdef public int _qg_ndim
    cdef public int _qg_length
    cdef public int _qg_length_0
    cdef public double[:,:] _qg_points
    cdef public double[:,:] _qg_results
    cdef public double[:,:] _qg_integrals
    cdef public double[:] _qg_sum
    cdef public bint _qg_diskflag
    cdef public str _qg_path
    cdef FILE *_qg_file
    cdef public bint _qg_ramflag
    cdef public double[:,:] _qg_array
    cdef public bint _qg_outputflag
    cdef double *_qg_outputpointer
    cdef public double qa
    cdef public int _qa_ndim
    cdef public int _qa_length
    cdef public double[:] _qa_points
    cdef public double[:] _qa_results
    cdef public double[:] _qa_integrals
    cdef public double _qa_sum
    cdef public bint _qa_diskflag
    cdef public str _qa_path
    cdef FILE *_qa_file
    cdef public bint _qa_ramflag
    cdef public double[:] _qa_array
    cdef public bint _qa_outputflag
    cdef double *_qa_outputpointer
    cdef public double[:] dh
    cdef public int _dh_ndim
    cdef public int _dh_length
    cdef public int _dh_length_0
    cdef public double[:,:] _dh_points
    cdef public double[:,:] _dh_results
    cdef public double[:,:] _dh_integrals
    cdef public double[:] _dh_sum
    cdef public bint _dh_diskflag
    cdef public str _dh_path
    cdef FILE *_dh_file
    cdef public bint _dh_ramflag
    cdef public double[:,:] _dh_array
    cdef public bint _dh_outputflag
    cdef double *_dh_outputpointer
    cpdef open_files(self, int idx):
        if self._qz_diskflag:
            self._qz_file = fopen(str(self._qz_path).encode(), "rb+")
            fseek(self._qz_file, idx*8, SEEK_SET)
        if self._qg_diskflag:
            self._qg_file = fopen(str(self._qg_path).encode(), "rb+")
            fseek(self._qg_file, idx*self._qg_length*8, SEEK_SET)
        if self._qa_diskflag:
            self._qa_file = fopen(str(self._qa_path).encode(), "rb+")
            fseek(self._qa_file, idx*8, SEEK_SET)
        if self._dh_diskflag:
            self._dh_file = fopen(str(self._dh_path).encode(), "rb+")
            fseek(self._dh_file, idx*self._dh_length*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._qz_diskflag:
            fclose(self._qz_file)
        if self._qg_diskflag:
            fclose(self._qg_file)
        if self._qa_diskflag:
            fclose(self._qa_file)
        if self._dh_diskflag:
            fclose(self._dh_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._qz_diskflag:
            fread(&self.qz, 8, 1, self._qz_file)
        elif self._qz_ramflag:
            self.qz = self._qz_array[idx]
        if self._qg_diskflag:
            fread(&self.qg[0], 8, self._qg_length, self._qg_file)
        elif self._qg_ramflag:
            for jdx0 in range(self._qg_length_0):
                self.qg[jdx0] = self._qg_array[idx, jdx0]
        if self._qa_diskflag:
            fread(&self.qa, 8, 1, self._qa_file)
        elif self._qa_ramflag:
            self.qa = self._qa_array[idx]
        if self._dh_diskflag:
            fread(&self.dh[0], 8, self._dh_length, self._dh_file)
        elif self._dh_ramflag:
            for jdx0 in range(self._dh_length_0):
                self.dh[jdx0] = self._dh_array[idx, jdx0]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._qz_diskflag:
            fwrite(&self.qz, 8, 1, self._qz_file)
        elif self._qz_ramflag:
            self._qz_array[idx] = self.qz
        if self._qg_diskflag:
            fwrite(&self.qg[0], 8, self._qg_length, self._qg_file)
        elif self._qg_ramflag:
            for jdx0 in range(self._qg_length_0):
                self._qg_array[idx, jdx0] = self.qg[jdx0]
        if self._qa_diskflag:
            fwrite(&self.qa, 8, 1, self._qa_file)
        elif self._qa_ramflag:
            self._qa_array[idx] = self.qa
        if self._dh_diskflag:
            fwrite(&self.dh[0], 8, self._dh_length, self._dh_file)
        elif self._dh_ramflag:
            for jdx0 in range(self._dh_length_0):
                self._dh_array[idx, jdx0] = self.dh[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "qz":
            self._qz_outputpointer = value.p_value
        if name == "qa":
            self._qa_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._qz_outputflag:
            self._qz_outputpointer[0] = self.qz
        if self._qa_outputflag:
            self._qa_outputpointer[0] = self.qa
@cython.final
cdef class StateSequences:
    cdef public double[:] h
    cdef public int _h_ndim
    cdef public int _h_length
    cdef public int _h_length_0
    cdef public double[:,:] _h_points
    cdef public double[:,:] _h_results
    cdef public bint _h_diskflag
    cdef public str _h_path
    cdef FILE *_h_file
    cdef public bint _h_ramflag
    cdef public double[:,:] _h_array
    cdef public bint _h_outputflag
    cdef double *_h_outputpointer
    cpdef open_files(self, int idx):
        if self._h_diskflag:
            self._h_file = fopen(str(self._h_path).encode(), "rb+")
            fseek(self._h_file, idx*self._h_length*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._h_diskflag:
            fclose(self._h_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._h_diskflag:
            fread(&self.h[0], 8, self._h_length, self._h_file)
        elif self._h_ramflag:
            for jdx0 in range(self._h_length_0):
                self.h[jdx0] = self._h_array[idx, jdx0]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._h_diskflag:
            fwrite(&self.h[0], 8, self._h_length, self._h_file)
        elif self._h_ramflag:
            for jdx0 in range(self._h_length_0):
                self._h_array[idx, jdx0] = self.h[jdx0]
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        pass
    cpdef inline void update_outputs(self) nogil:
        pass
@cython.final
cdef class AideSequences:
    cdef public double[:] wbm
    cdef public int _wbm_ndim
    cdef public int _wbm_length
    cdef public int _wbm_length_0
    cdef public double[:] wblv
    cdef public int _wblv_ndim
    cdef public int _wblv_length
    cdef public int _wblv_length_0
    cdef public double[:] wbrv
    cdef public int _wbrv_ndim
    cdef public int _wbrv_length
    cdef public int _wbrv_length_0
    cdef public double[:] wblvr
    cdef public int _wblvr_ndim
    cdef public int _wblvr_length
    cdef public int _wblvr_length_0
    cdef public double[:] wbrvr
    cdef public int _wbrvr_ndim
    cdef public int _wbrvr_length
    cdef public int _wbrvr_length_0
    cdef public double[:] wbg
    cdef public int _wbg_ndim
    cdef public int _wbg_length
    cdef public int _wbg_length_0
    cdef public double[:] am
    cdef public int _am_ndim
    cdef public int _am_length
    cdef public int _am_length_0
    cdef public double[:] alv
    cdef public int _alv_ndim
    cdef public int _alv_length
    cdef public int _alv_length_0
    cdef public double[:] arv
    cdef public int _arv_ndim
    cdef public int _arv_length
    cdef public int _arv_length_0
    cdef public double[:] alvr
    cdef public int _alvr_ndim
    cdef public int _alvr_length
    cdef public int _alvr_length_0
    cdef public double[:] arvr
    cdef public int _arvr_ndim
    cdef public int _arvr_length
    cdef public int _arvr_length_0
    cdef public double[:] ag
    cdef public int _ag_ndim
    cdef public int _ag_length
    cdef public int _ag_length_0
    cdef public double[:] um
    cdef public int _um_ndim
    cdef public int _um_length
    cdef public int _um_length_0
    cdef public double[:] ulv
    cdef public int _ulv_ndim
    cdef public int _ulv_length
    cdef public int _ulv_length_0
    cdef public double[:] urv
    cdef public int _urv_ndim
    cdef public int _urv_length
    cdef public int _urv_length_0
    cdef public double[:] ulvr
    cdef public int _ulvr_ndim
    cdef public int _ulvr_length
    cdef public int _ulvr_length_0
    cdef public double[:] urvr
    cdef public int _urvr_ndim
    cdef public int _urvr_length
    cdef public int _urvr_length_0
    cdef public double[:] qm
    cdef public int _qm_ndim
    cdef public int _qm_length
    cdef public int _qm_length_0
    cdef public double[:] qlv
    cdef public int _qlv_ndim
    cdef public int _qlv_length
    cdef public int _qlv_length_0
    cdef public double[:] qrv
    cdef public int _qrv_ndim
    cdef public int _qrv_length
    cdef public int _qrv_length_0
    cdef public double[:] qlvr
    cdef public int _qlvr_ndim
    cdef public int _qlvr_length
    cdef public int _qlvr_length_0
    cdef public double[:] qrvr
    cdef public int _qrvr_ndim
    cdef public int _qrvr_length
    cdef public int _qrvr_length_0
    cdef public double[:] rhm
    cdef public int _rhm_ndim
    cdef public int _rhm_length
    cdef public int _rhm_length_0
    cdef public double[:] rhmdh
    cdef public int _rhmdh_ndim
    cdef public int _rhmdh_length
    cdef public int _rhmdh_length_0
    cdef public double[:] rhv
    cdef public int _rhv_ndim
    cdef public int _rhv_length
    cdef public int _rhv_length_0
    cdef public double[:] rhvdh
    cdef public int _rhvdh_ndim
    cdef public int _rhvdh_length
    cdef public int _rhvdh_length_0
    cdef public double[:] rhlvr
    cdef public int _rhlvr_ndim
    cdef public int _rhlvr_length
    cdef public int _rhlvr_length_0
    cdef public double[:] rhlvrdh
    cdef public int _rhlvrdh_ndim
    cdef public int _rhlvrdh_length
    cdef public int _rhlvrdh_length_0
    cdef public double[:] rhrvr
    cdef public int _rhrvr_ndim
    cdef public int _rhrvr_length
    cdef public int _rhrvr_length_0
    cdef public double[:] rhrvrdh
    cdef public int _rhrvrdh_ndim
    cdef public int _rhrvrdh_length
    cdef public int _rhrvrdh_length_0
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
cdef class PegasusH(rootutils.PegasusBase):
    cpdef public Model model
    def __init__(self, Model model):
        self.model = model
    cpdef double apply_method0(self, double x) nogil:
        return self.model.return_qf_v1(x)
@cython.final
cdef class Model:
    cdef public int idx_sim
    cdef public Parameters parameters
    cdef public Sequences sequences
    cdef public PegasusH pegasush
    cdef public NumConsts numconsts
    cdef public NumVars numvars
    def __init__(self):
        self.pegasush = PegasusH(self)
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
        for jdx0 in range(self.sequences.states._h_length_0):
            self.sequences.old_states.h[jdx0] = self.sequences.new_states.h[jdx0]
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
        self.sequences.fluxes.update_outputs()
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
        self.calc_rhm_v1()
        self.calc_rhmdh_v1()
        self.calc_rhv_v1()
        self.calc_rhvdh_v1()
        self.calc_rhlvr_rhrvr_v1()
        self.calc_rhlvrdh_rhrvrdh_v1()
        self.calc_am_um_v1()
        self.calc_alv_arv_ulv_urv_v1()
        self.calc_alvr_arvr_ulvr_urvr_v1()
        self.calc_qm_v1()
        self.calc_qlv_qrv_v1()
        self.calc_qlvr_qrvr_v1()
        self.calc_ag_v1()
        self.calc_qg_v1()
        self.calc_qa_v1()
        self.calc_wbm_v1()
        self.calc_wblv_wbrv_v1()
        self.calc_wblvr_wbrvr_v1()
        self.calc_wbg_v1()
        self.calc_dh_v1()
    cpdef inline void calculate_full_terms(self) nogil:
        self.update_h_v1()
    cpdef inline void get_point_states(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.states._h_length):
            self.sequences.states.h[idx0] = self.sequences.states._h_points[self.numvars.idx_stage][idx0]
    cpdef inline void set_point_states(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.states._h_length):
            self.sequences.states._h_points[self.numvars.idx_stage][idx0] = self.sequences.states.h[idx0]
    cpdef inline void set_result_states(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.states._h_length):
            self.sequences.states._h_results[self.numvars.idx_method][idx0] = self.sequences.states.h[idx0]
    cpdef inline void get_sum_fluxes(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes.qg[idx0] = self.sequences.fluxes._qg_sum[idx0]
        self.sequences.fluxes.qa = self.sequences.fluxes._qa_sum
        for idx0 in range(self.sequences.fluxes._dh_length):
            self.sequences.fluxes.dh[idx0] = self.sequences.fluxes._dh_sum[idx0]
    cpdef inline void set_point_fluxes(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes._qg_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.qg[idx0]
        self.sequences.fluxes._qa_points[self.numvars.idx_stage] = self.sequences.fluxes.qa
        for idx0 in range(self.sequences.fluxes._dh_length):
            self.sequences.fluxes._dh_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.dh[idx0]
    cpdef inline void set_result_fluxes(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes._qg_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.qg[idx0]
        self.sequences.fluxes._qa_results[self.numvars.idx_method] = self.sequences.fluxes.qa
        for idx0 in range(self.sequences.fluxes._dh_length):
            self.sequences.fluxes._dh_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.dh[idx0]
    cpdef inline void integrate_fluxes(self) nogil:
        cdef int jdx, idx0
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes.qg[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.qg[idx0] = self.sequences.fluxes.qg[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._qg_points[jdx, idx0]
        self.sequences.fluxes.qa = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.qa = self.sequences.fluxes.qa +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._qa_points[jdx]
        for idx0 in range(self.sequences.fluxes._dh_length):
            self.sequences.fluxes.dh[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.dh[idx0] = self.sequences.fluxes.dh[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._dh_points[jdx, idx0]
    cpdef inline void reset_sum_fluxes(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes._qg_sum[idx0] = 0.
        self.sequences.fluxes._qa_sum = 0.
        for idx0 in range(self.sequences.fluxes._dh_length):
            self.sequences.fluxes._dh_sum[idx0] = 0.
    cpdef inline void addup_fluxes(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes._qg_sum[idx0] = self.sequences.fluxes._qg_sum[idx0] + self.sequences.fluxes.qg[idx0]
        self.sequences.fluxes._qa_sum = self.sequences.fluxes._qa_sum + self.sequences.fluxes.qa
        for idx0 in range(self.sequences.fluxes._dh_length):
            self.sequences.fluxes._dh_sum[idx0] = self.sequences.fluxes._dh_sum[idx0] + self.sequences.fluxes.dh[idx0]
    cpdef inline void calculate_error(self) nogil:
        cdef int idx0
        cdef double abserror
        self.numvars.abserror = 0.
        if self.numvars.use_relerror:
            self.numvars.relerror = 0.
        else:
            self.numvars.relerror = inf
        for idx0 in range(self.sequences.fluxes._qg_length):
            abserror = fabs(self.sequences.fluxes._qg_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._qg_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._qg_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._qg_results[self.numvars.idx_method, idx0]))
        for idx0 in range(self.sequences.fluxes._dh_length):
            abserror = fabs(self.sequences.fluxes._dh_results[self.numvars.idx_method, idx0]-self.sequences.fluxes._dh_results[self.numvars.idx_method-1, idx0])
            self.numvars.abserror = max(self.numvars.abserror, abserror)
            if self.numvars.use_relerror:
                if self.sequences.fluxes._dh_results[self.numvars.idx_method, idx0] == 0.:
                    self.numvars.relerror = inf
                else:
                    self.numvars.relerror = max(self.numvars.relerror, fabs(abserror/self.sequences.fluxes._dh_results[self.numvars.idx_method, idx0]))
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
    cpdef inline void pick_q_v1(self)  nogil:
        cdef int idx
        self.sequences.fluxes.qz = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.qz = self.sequences.fluxes.qz + (self.sequences.inlets.q[idx][0])
    cpdef inline void pick_q(self)  nogil:
        cdef int idx
        self.sequences.fluxes.qz = 0.0
        for idx in range(self.sequences.inlets.len_q):
            self.sequences.fluxes.qz = self.sequences.fluxes.qz + (self.sequences.inlets.q[idx][0])
    cpdef inline void calc_rhm_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhm[i] = smoothutils.smooth_logistic2(self.sequences.states.h[i], self.parameters.derived.hrp)
    cpdef inline void calc_rhmdh_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhmdh[i] = smoothutils.smooth_logistic2_derivative2(self.sequences.states.h[i], self.parameters.derived.hrp)
    cpdef inline void calc_rhv_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhv[i] = smoothutils.smooth_logistic2(self.sequences.states.h[i] - self.parameters.control.hm, self.parameters.derived.hrp)
    cpdef inline void calc_rhvdh_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhvdh[i] = smoothutils.smooth_logistic2_derivative2(                self.sequences.states.h[i] - self.parameters.control.hm, self.parameters.derived.hrp            )
    cpdef inline void calc_rhlvr_rhrvr_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhlvr[i] = smoothutils.smooth_logistic2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[0], self.parameters.derived.hrp            )
            self.sequences.aides.rhrvr[i] = smoothutils.smooth_logistic2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[1], self.parameters.derived.hrp            )
    cpdef inline void calc_rhlvrdh_rhrvrdh_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhlvrdh[i] = smoothutils.smooth_logistic2_derivative2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[0], self.parameters.derived.hrp            )
            self.sequences.aides.rhrvrdh[i] = smoothutils.smooth_logistic2_derivative2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[1], self.parameters.derived.hrp            )
    cpdef inline void calc_am_um_v1(self)  nogil:
        cdef double d_temp
        cdef int i
        for i in range(self.parameters.control.gts):
            d_temp = self.sequences.aides.rhm[i] - self.sequences.aides.rhv[i]
            self.sequences.aides.am[i] = d_temp * (self.parameters.control.bm + d_temp * self.parameters.control.bnm) + self.sequences.aides.rhv[i] * (                self.parameters.control.bm + 2.0 * d_temp * self.parameters.control.bnm            )
            self.sequences.aides.um[i] = self.parameters.control.bm + 2.0 * d_temp * self.parameters.derived.bnmf + 2.0 * self.sequences.aides.rhv[i]
    cpdef inline void calc_alv_arv_ulv_urv_v1(self)  nogil:
        cdef double d_temp
        cdef int i
        for i in range(self.parameters.control.gts):
            d_temp = self.sequences.aides.rhv[i] - self.sequences.aides.rhlvr[i]
            self.sequences.aides.alv[i] = d_temp * (self.parameters.control.bv[0] + (d_temp * self.parameters.control.bnv[0] / 2.0)) + self.sequences.aides.rhlvr[                i            ] * (self.parameters.control.bv[0] + d_temp * self.parameters.control.bnv[0])
            self.sequences.aides.ulv[i] = self.parameters.control.bv[0] + d_temp * self.parameters.derived.bnvf[0] + self.sequences.aides.rhlvr[i]
            d_temp = self.sequences.aides.rhv[i] - self.sequences.aides.rhrvr[i]
            self.sequences.aides.arv[i] = d_temp * (self.parameters.control.bv[1] + (d_temp * self.parameters.control.bnv[1] / 2.0)) + self.sequences.aides.rhrvr[                i            ] * (self.parameters.control.bv[1] + d_temp * self.parameters.control.bnv[1])
            self.sequences.aides.urv[i] = self.parameters.control.bv[1] + d_temp * self.parameters.derived.bnvf[1] + self.sequences.aides.rhrvr[i]
    cpdef inline void calc_alvr_arvr_ulvr_urvr_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.alvr[i] = self.sequences.aides.rhlvr[i] ** 2 * self.parameters.control.bnvr[0] / 2.0
            self.sequences.aides.ulvr[i] = self.sequences.aides.rhlvr[i] * self.parameters.derived.bnvrf[0]
            self.sequences.aides.arvr[i] = self.sequences.aides.rhrvr[i] ** 2 * self.parameters.control.bnvr[1] / 2.0
            self.sequences.aides.urvr[i] = self.sequences.aides.rhrvr[i] * self.parameters.derived.bnvrf[1]
    cpdef inline void calc_qm_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            if self.sequences.aides.um[i] > 0.0:
                self.sequences.aides.qm[i] = (                    self.parameters.derived.mfm * self.sequences.aides.am[i] ** (5.0 / 3.0) / self.sequences.aides.um[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qm[i] = 0.0
    cpdef inline void calc_qlv_qrv_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            if self.sequences.aides.ulv[i] > 0.0:
                self.sequences.aides.qlv[i] = (                    self.parameters.derived.mfv[0] * self.sequences.aides.alv[i] ** (5.0 / 3.0) / self.sequences.aides.ulv[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qlv[i] = 0.0
            if self.sequences.aides.urv[i] > 0:
                self.sequences.aides.qrv[i] = (                    self.parameters.derived.mfv[1] * self.sequences.aides.arv[i] ** (5.0 / 3.0) / self.sequences.aides.urv[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qrv[i] = 0.0
    cpdef inline void calc_qlvr_qrvr_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            if self.sequences.aides.ulvr[i] > 0.0:
                self.sequences.aides.qlvr[i] = (                    self.parameters.derived.mfv[0] * self.sequences.aides.alvr[i] ** (5.0 / 3.0) / self.sequences.aides.ulvr[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qlvr[i] = 0.0
            if self.sequences.aides.urvr[i] > 0.0:
                self.sequences.aides.qrvr[i] = (                    self.parameters.derived.mfv[1] * self.sequences.aides.arvr[i] ** (5.0 / 3.0) / self.sequences.aides.urvr[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qrvr[i] = 0.0
    cpdef inline void calc_ag_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.ag[i] = self.sequences.aides.am[i] + self.sequences.aides.alv[i] + self.sequences.aides.arv[i] + self.sequences.aides.alvr[i] + self.sequences.aides.arvr[i]
    cpdef inline void calc_qg_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.fluxes.qg[i] = self.sequences.aides.qm[i] + self.sequences.aides.qlv[i] + self.sequences.aides.qrv[i] + self.sequences.aides.qlvr[i] + self.sequences.aides.qrvr[i]
    cpdef inline void calc_qa_v1(self)  nogil:
        self.sequences.fluxes.qa = self.sequences.fluxes.qg[self.parameters.control.gts - 1]
    cpdef inline void calc_wbm_v1(self)  nogil:
        cdef double d_temp2
        cdef double d_temp1
        cdef int i
        for i in range(self.parameters.control.gts):
            d_temp1 = self.sequences.aides.rhm[i] - self.sequences.aides.rhv[i]
            d_temp2 = self.sequences.aides.rhmdh[i] - self.sequences.aides.rhvdh[i]
            self.sequences.aides.wbm[i] = (                self.parameters.control.bnm * d_temp1 * d_temp2                + self.parameters.control.bnm * 2.0 * d_temp2 * self.sequences.aides.rhv[i]                + (self.parameters.control.bm + self.parameters.control.bnm * d_temp1) * d_temp2                + (self.parameters.control.bm + self.parameters.control.bnm * 2.0 * d_temp1) * self.sequences.aides.rhvdh[i]            )
            self.sequences.aides.wbm[i] = smoothutils.smooth_max1(self.parameters.fixed.wbmin, self.sequences.aides.wbm[i], self.parameters.fixed.wbreg)
    cpdef inline void calc_wblv_wbrv_v1(self)  nogil:
        cdef double d_temp2
        cdef double d_temp1
        cdef int i
        for i in range(self.parameters.control.gts):
            d_temp1 = self.sequences.aides.rhv[i] - self.sequences.aides.rhlvr[i]
            d_temp2 = self.sequences.aides.rhvdh[i] - self.sequences.aides.rhlvrdh[i]
            self.sequences.aides.wblv[i] = (                self.parameters.control.bnv[0] * d_temp1 * d_temp2 / 2.0                + self.parameters.control.bnv[0] * d_temp2 * self.sequences.aides.rhlvr[i]                + (self.parameters.control.bnv[0] * d_temp1 / 2.0 + self.parameters.control.bv[0]) * d_temp2                + (self.parameters.control.bnv[0] * d_temp1 + self.parameters.control.bv[0]) * self.sequences.aides.rhlvrdh[i]            )
            d_temp1 = self.sequences.aides.rhv[i] - self.sequences.aides.rhrvr[i]
            d_temp2 = self.sequences.aides.rhvdh[i] - self.sequences.aides.rhrvrdh[i]
            self.sequences.aides.wbrv[i] = (                self.parameters.control.bnv[1] * d_temp1 * d_temp2 / 2.0                + self.parameters.control.bnv[1] * d_temp2 * self.sequences.aides.rhrvr[i]                + (self.parameters.control.bnv[1] * d_temp1 / 2.0 + self.parameters.control.bv[1]) * d_temp2                + (self.parameters.control.bnv[1] * d_temp1 + self.parameters.control.bv[1]) * self.sequences.aides.rhrvrdh[i]            )
    cpdef inline void calc_wblvr_wbrvr_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.wblvr[i] = self.parameters.control.bnvr[0] * self.sequences.aides.rhlvr[i] * self.sequences.aides.rhlvrdh[i]
            self.sequences.aides.wbrvr[i] = self.parameters.control.bnvr[1] * self.sequences.aides.rhrvr[i] * self.sequences.aides.rhrvrdh[i]
    cpdef inline void calc_wbg_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.wbg[i] = (                self.sequences.aides.wbm[i] + self.sequences.aides.wblv[i] + self.sequences.aides.wbrv[i] + self.sequences.aides.wblvr[i] + self.sequences.aides.wbrvr[i]            )
    cpdef inline void calc_dh_v1(self)  nogil:
        cdef double d_qz
        cdef int i
        for i in range(self.parameters.control.gts):
            if i:
                d_qz = self.sequences.fluxes.qg[i - 1]
            else:
                d_qz = self.sequences.fluxes.qz
            self.sequences.fluxes.dh[i] = (d_qz - self.sequences.fluxes.qg[i]) / (1000.0 * self.parameters.control.laen / self.parameters.control.gts * self.sequences.aides.wbg[i])
    cpdef inline void calc_rhm(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhm[i] = smoothutils.smooth_logistic2(self.sequences.states.h[i], self.parameters.derived.hrp)
    cpdef inline void calc_rhmdh(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhmdh[i] = smoothutils.smooth_logistic2_derivative2(self.sequences.states.h[i], self.parameters.derived.hrp)
    cpdef inline void calc_rhv(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhv[i] = smoothutils.smooth_logistic2(self.sequences.states.h[i] - self.parameters.control.hm, self.parameters.derived.hrp)
    cpdef inline void calc_rhvdh(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhvdh[i] = smoothutils.smooth_logistic2_derivative2(                self.sequences.states.h[i] - self.parameters.control.hm, self.parameters.derived.hrp            )
    cpdef inline void calc_rhlvr_rhrvr(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhlvr[i] = smoothutils.smooth_logistic2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[0], self.parameters.derived.hrp            )
            self.sequences.aides.rhrvr[i] = smoothutils.smooth_logistic2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[1], self.parameters.derived.hrp            )
    cpdef inline void calc_rhlvrdh_rhrvrdh(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.rhlvrdh[i] = smoothutils.smooth_logistic2_derivative2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[0], self.parameters.derived.hrp            )
            self.sequences.aides.rhrvrdh[i] = smoothutils.smooth_logistic2_derivative2(                self.sequences.states.h[i] - self.parameters.control.hm - self.parameters.derived.hv[1], self.parameters.derived.hrp            )
    cpdef inline void calc_am_um(self)  nogil:
        cdef double d_temp
        cdef int i
        for i in range(self.parameters.control.gts):
            d_temp = self.sequences.aides.rhm[i] - self.sequences.aides.rhv[i]
            self.sequences.aides.am[i] = d_temp * (self.parameters.control.bm + d_temp * self.parameters.control.bnm) + self.sequences.aides.rhv[i] * (                self.parameters.control.bm + 2.0 * d_temp * self.parameters.control.bnm            )
            self.sequences.aides.um[i] = self.parameters.control.bm + 2.0 * d_temp * self.parameters.derived.bnmf + 2.0 * self.sequences.aides.rhv[i]
    cpdef inline void calc_alv_arv_ulv_urv(self)  nogil:
        cdef double d_temp
        cdef int i
        for i in range(self.parameters.control.gts):
            d_temp = self.sequences.aides.rhv[i] - self.sequences.aides.rhlvr[i]
            self.sequences.aides.alv[i] = d_temp * (self.parameters.control.bv[0] + (d_temp * self.parameters.control.bnv[0] / 2.0)) + self.sequences.aides.rhlvr[                i            ] * (self.parameters.control.bv[0] + d_temp * self.parameters.control.bnv[0])
            self.sequences.aides.ulv[i] = self.parameters.control.bv[0] + d_temp * self.parameters.derived.bnvf[0] + self.sequences.aides.rhlvr[i]
            d_temp = self.sequences.aides.rhv[i] - self.sequences.aides.rhrvr[i]
            self.sequences.aides.arv[i] = d_temp * (self.parameters.control.bv[1] + (d_temp * self.parameters.control.bnv[1] / 2.0)) + self.sequences.aides.rhrvr[                i            ] * (self.parameters.control.bv[1] + d_temp * self.parameters.control.bnv[1])
            self.sequences.aides.urv[i] = self.parameters.control.bv[1] + d_temp * self.parameters.derived.bnvf[1] + self.sequences.aides.rhrvr[i]
    cpdef inline void calc_alvr_arvr_ulvr_urvr(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.alvr[i] = self.sequences.aides.rhlvr[i] ** 2 * self.parameters.control.bnvr[0] / 2.0
            self.sequences.aides.ulvr[i] = self.sequences.aides.rhlvr[i] * self.parameters.derived.bnvrf[0]
            self.sequences.aides.arvr[i] = self.sequences.aides.rhrvr[i] ** 2 * self.parameters.control.bnvr[1] / 2.0
            self.sequences.aides.urvr[i] = self.sequences.aides.rhrvr[i] * self.parameters.derived.bnvrf[1]
    cpdef inline void calc_qm(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            if self.sequences.aides.um[i] > 0.0:
                self.sequences.aides.qm[i] = (                    self.parameters.derived.mfm * self.sequences.aides.am[i] ** (5.0 / 3.0) / self.sequences.aides.um[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qm[i] = 0.0
    cpdef inline void calc_qlv_qrv(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            if self.sequences.aides.ulv[i] > 0.0:
                self.sequences.aides.qlv[i] = (                    self.parameters.derived.mfv[0] * self.sequences.aides.alv[i] ** (5.0 / 3.0) / self.sequences.aides.ulv[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qlv[i] = 0.0
            if self.sequences.aides.urv[i] > 0:
                self.sequences.aides.qrv[i] = (                    self.parameters.derived.mfv[1] * self.sequences.aides.arv[i] ** (5.0 / 3.0) / self.sequences.aides.urv[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qrv[i] = 0.0
    cpdef inline void calc_qlvr_qrvr(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            if self.sequences.aides.ulvr[i] > 0.0:
                self.sequences.aides.qlvr[i] = (                    self.parameters.derived.mfv[0] * self.sequences.aides.alvr[i] ** (5.0 / 3.0) / self.sequences.aides.ulvr[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qlvr[i] = 0.0
            if self.sequences.aides.urvr[i] > 0.0:
                self.sequences.aides.qrvr[i] = (                    self.parameters.derived.mfv[1] * self.sequences.aides.arvr[i] ** (5.0 / 3.0) / self.sequences.aides.urvr[i] ** (2.0 / 3.0)                )
            else:
                self.sequences.aides.qrvr[i] = 0.0
    cpdef inline void calc_ag(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.ag[i] = self.sequences.aides.am[i] + self.sequences.aides.alv[i] + self.sequences.aides.arv[i] + self.sequences.aides.alvr[i] + self.sequences.aides.arvr[i]
    cpdef inline void calc_qg(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.fluxes.qg[i] = self.sequences.aides.qm[i] + self.sequences.aides.qlv[i] + self.sequences.aides.qrv[i] + self.sequences.aides.qlvr[i] + self.sequences.aides.qrvr[i]
    cpdef inline void calc_qa(self)  nogil:
        self.sequences.fluxes.qa = self.sequences.fluxes.qg[self.parameters.control.gts - 1]
    cpdef inline void calc_wbm(self)  nogil:
        cdef double d_temp2
        cdef double d_temp1
        cdef int i
        for i in range(self.parameters.control.gts):
            d_temp1 = self.sequences.aides.rhm[i] - self.sequences.aides.rhv[i]
            d_temp2 = self.sequences.aides.rhmdh[i] - self.sequences.aides.rhvdh[i]
            self.sequences.aides.wbm[i] = (                self.parameters.control.bnm * d_temp1 * d_temp2                + self.parameters.control.bnm * 2.0 * d_temp2 * self.sequences.aides.rhv[i]                + (self.parameters.control.bm + self.parameters.control.bnm * d_temp1) * d_temp2                + (self.parameters.control.bm + self.parameters.control.bnm * 2.0 * d_temp1) * self.sequences.aides.rhvdh[i]            )
            self.sequences.aides.wbm[i] = smoothutils.smooth_max1(self.parameters.fixed.wbmin, self.sequences.aides.wbm[i], self.parameters.fixed.wbreg)
    cpdef inline void calc_wblv_wbrv(self)  nogil:
        cdef double d_temp2
        cdef double d_temp1
        cdef int i
        for i in range(self.parameters.control.gts):
            d_temp1 = self.sequences.aides.rhv[i] - self.sequences.aides.rhlvr[i]
            d_temp2 = self.sequences.aides.rhvdh[i] - self.sequences.aides.rhlvrdh[i]
            self.sequences.aides.wblv[i] = (                self.parameters.control.bnv[0] * d_temp1 * d_temp2 / 2.0                + self.parameters.control.bnv[0] * d_temp2 * self.sequences.aides.rhlvr[i]                + (self.parameters.control.bnv[0] * d_temp1 / 2.0 + self.parameters.control.bv[0]) * d_temp2                + (self.parameters.control.bnv[0] * d_temp1 + self.parameters.control.bv[0]) * self.sequences.aides.rhlvrdh[i]            )
            d_temp1 = self.sequences.aides.rhv[i] - self.sequences.aides.rhrvr[i]
            d_temp2 = self.sequences.aides.rhvdh[i] - self.sequences.aides.rhrvrdh[i]
            self.sequences.aides.wbrv[i] = (                self.parameters.control.bnv[1] * d_temp1 * d_temp2 / 2.0                + self.parameters.control.bnv[1] * d_temp2 * self.sequences.aides.rhrvr[i]                + (self.parameters.control.bnv[1] * d_temp1 / 2.0 + self.parameters.control.bv[1]) * d_temp2                + (self.parameters.control.bnv[1] * d_temp1 + self.parameters.control.bv[1]) * self.sequences.aides.rhrvrdh[i]            )
    cpdef inline void calc_wblvr_wbrvr(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.wblvr[i] = self.parameters.control.bnvr[0] * self.sequences.aides.rhlvr[i] * self.sequences.aides.rhlvrdh[i]
            self.sequences.aides.wbrvr[i] = self.parameters.control.bnvr[1] * self.sequences.aides.rhrvr[i] * self.sequences.aides.rhrvrdh[i]
    cpdef inline void calc_wbg(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.aides.wbg[i] = (                self.sequences.aides.wbm[i] + self.sequences.aides.wblv[i] + self.sequences.aides.wbrv[i] + self.sequences.aides.wblvr[i] + self.sequences.aides.wbrvr[i]            )
    cpdef inline void calc_dh(self)  nogil:
        cdef double d_qz
        cdef int i
        for i in range(self.parameters.control.gts):
            if i:
                d_qz = self.sequences.fluxes.qg[i - 1]
            else:
                d_qz = self.sequences.fluxes.qz
            self.sequences.fluxes.dh[i] = (d_qz - self.sequences.fluxes.qg[i]) / (1000.0 * self.parameters.control.laen / self.parameters.control.gts * self.sequences.aides.wbg[i])
    cpdef inline void update_h_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.new_states.h[i] = self.sequences.old_states.h[i] + self.parameters.derived.sek * self.sequences.fluxes.dh[i]
    cpdef inline void update_h(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.sequences.new_states.h[i] = self.sequences.old_states.h[i] + self.parameters.derived.sek * self.sequences.fluxes.dh[i]
    cpdef inline double return_qf_v1(self, double h)  nogil:
        cdef double d_error
        cdef double d_qg
        d_qg = self.sequences.fluxes.qg[0]
        self.sequences.states.h[0] = h
        self.calc_rhm_v1()
        self.calc_rhmdh_v1()
        self.calc_rhv_v1()
        self.calc_rhvdh_v1()
        self.calc_rhlvr_rhrvr_v1()
        self.calc_rhlvrdh_rhrvrdh_v1()
        self.calc_am_um_v1()
        self.calc_alv_arv_ulv_urv_v1()
        self.calc_alvr_arvr_ulvr_urvr_v1()
        self.calc_qm_v1()
        self.calc_qlv_qrv_v1()
        self.calc_qlvr_qrvr_v1()
        self.calc_ag_v1()
        self.calc_qg_v1()
        d_error = self.sequences.fluxes.qg[0] - d_qg
        self.sequences.fluxes.qg[0] = d_qg
        return d_error
    cpdef inline double return_h_v1(self)  nogil:
        return self.pegasush.find_x(0.0, 2.0 * self.parameters.control.hm, -10.0, 1000.0, 0.0, 1e-10, 1000)
    cpdef inline double return_qf(self, double h)  nogil:
        cdef double d_error
        cdef double d_qg
        d_qg = self.sequences.fluxes.qg[0]
        self.sequences.states.h[0] = h
        self.calc_rhm_v1()
        self.calc_rhmdh_v1()
        self.calc_rhv_v1()
        self.calc_rhvdh_v1()
        self.calc_rhlvr_rhrvr_v1()
        self.calc_rhlvrdh_rhrvrdh_v1()
        self.calc_am_um_v1()
        self.calc_alv_arv_ulv_urv_v1()
        self.calc_alvr_arvr_ulvr_urvr_v1()
        self.calc_qm_v1()
        self.calc_qlv_qrv_v1()
        self.calc_qlvr_qrvr_v1()
        self.calc_ag_v1()
        self.calc_qg_v1()
        d_error = self.sequences.fluxes.qg[0] - d_qg
        self.sequences.fluxes.qg[0] = d_qg
        return d_error
    cpdef inline double return_h(self)  nogil:
        return self.pegasush.find_x(0.0, 2.0 * self.parameters.control.hm, -10.0, 1000.0, 0.0, 1e-10, 1000)
    cpdef inline void pass_q_v1(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.qa)
    cpdef inline void pass_q(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.qa)
