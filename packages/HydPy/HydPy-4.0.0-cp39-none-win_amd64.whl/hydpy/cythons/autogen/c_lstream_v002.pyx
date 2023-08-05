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
    cdef public numpy.int32_t gts
    cdef public annutils.ANN vg2qg
@cython.final
cdef class DerivedParameters:
    cdef public double sek
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
    cdef public double qza
    cdef public int _qza_ndim
    cdef public int _qza_length
    cdef public double[:] _qza_points
    cdef public double[:] _qza_results
    cdef public double[:] _qza_integrals
    cdef public double _qza_sum
    cdef public bint _qza_diskflag
    cdef public str _qza_path
    cdef FILE *_qza_file
    cdef public bint _qza_ramflag
    cdef public double[:] _qza_array
    cdef public bint _qza_outputflag
    cdef double *_qza_outputpointer
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
    cpdef open_files(self, int idx):
        if self._qz_diskflag:
            self._qz_file = fopen(str(self._qz_path).encode(), "rb+")
            fseek(self._qz_file, idx*8, SEEK_SET)
        if self._qza_diskflag:
            self._qza_file = fopen(str(self._qza_path).encode(), "rb+")
            fseek(self._qza_file, idx*8, SEEK_SET)
        if self._qg_diskflag:
            self._qg_file = fopen(str(self._qg_path).encode(), "rb+")
            fseek(self._qg_file, idx*self._qg_length*8, SEEK_SET)
        if self._qa_diskflag:
            self._qa_file = fopen(str(self._qa_path).encode(), "rb+")
            fseek(self._qa_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._qz_diskflag:
            fclose(self._qz_file)
        if self._qza_diskflag:
            fclose(self._qza_file)
        if self._qg_diskflag:
            fclose(self._qg_file)
        if self._qa_diskflag:
            fclose(self._qa_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._qz_diskflag:
            fread(&self.qz, 8, 1, self._qz_file)
        elif self._qz_ramflag:
            self.qz = self._qz_array[idx]
        if self._qza_diskflag:
            fread(&self.qza, 8, 1, self._qza_file)
        elif self._qza_ramflag:
            self.qza = self._qza_array[idx]
        if self._qg_diskflag:
            fread(&self.qg[0], 8, self._qg_length, self._qg_file)
        elif self._qg_ramflag:
            for jdx0 in range(self._qg_length_0):
                self.qg[jdx0] = self._qg_array[idx, jdx0]
        if self._qa_diskflag:
            fread(&self.qa, 8, 1, self._qa_file)
        elif self._qa_ramflag:
            self.qa = self._qa_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._qz_diskflag:
            fwrite(&self.qz, 8, 1, self._qz_file)
        elif self._qz_ramflag:
            self._qz_array[idx] = self.qz
        if self._qza_diskflag:
            fwrite(&self.qza, 8, 1, self._qza_file)
        elif self._qza_ramflag:
            self._qza_array[idx] = self.qza
        if self._qg_diskflag:
            fwrite(&self.qg[0], 8, self._qg_length, self._qg_file)
        elif self._qg_ramflag:
            for jdx0 in range(self._qg_length_0):
                self._qg_array[idx, jdx0] = self.qg[jdx0]
        if self._qa_diskflag:
            fwrite(&self.qa, 8, 1, self._qa_file)
        elif self._qa_ramflag:
            self._qa_array[idx] = self.qa
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "qz":
            self._qz_outputpointer = value.p_value
        if name == "qza":
            self._qza_outputpointer = value.p_value
        if name == "qa":
            self._qa_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._qz_outputflag:
            self._qz_outputpointer[0] = self.qz
        if self._qza_outputflag:
            self._qza_outputpointer[0] = self.qza
        if self._qa_outputflag:
            self._qa_outputpointer[0] = self.qa
@cython.final
cdef class StateSequences:
    cdef public double[:] vg
    cdef public int _vg_ndim
    cdef public int _vg_length
    cdef public int _vg_length_0
    cdef public double[:,:] _vg_points
    cdef public double[:,:] _vg_results
    cdef public bint _vg_diskflag
    cdef public str _vg_path
    cdef FILE *_vg_file
    cdef public bint _vg_ramflag
    cdef public double[:,:] _vg_array
    cdef public bint _vg_outputflag
    cdef double *_vg_outputpointer
    cpdef open_files(self, int idx):
        if self._vg_diskflag:
            self._vg_file = fopen(str(self._vg_path).encode(), "rb+")
            fseek(self._vg_file, idx*self._vg_length*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._vg_diskflag:
            fclose(self._vg_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._vg_diskflag:
            fread(&self.vg[0], 8, self._vg_length, self._vg_file)
        elif self._vg_ramflag:
            for jdx0 in range(self._vg_length_0):
                self.vg[jdx0] = self._vg_array[idx, jdx0]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._vg_diskflag:
            fwrite(&self.vg[0], 8, self._vg_length, self._vg_file)
        elif self._vg_ramflag:
            for jdx0 in range(self._vg_length_0):
                self._vg_array[idx, jdx0] = self.vg[jdx0]
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
        for jdx0 in range(self.sequences.states._vg_length_0):
            self.sequences.old_states.vg[jdx0] = self.sequences.new_states.vg[jdx0]
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
        self.calc_qza_v1()
        self.calc_qg_v2()
        self.calc_qa_v1()
    cpdef inline void calculate_full_terms(self) nogil:
        self.update_vg_v1()
    cpdef inline void get_point_states(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.states._vg_length):
            self.sequences.states.vg[idx0] = self.sequences.states._vg_points[self.numvars.idx_stage][idx0]
    cpdef inline void set_point_states(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.states._vg_length):
            self.sequences.states._vg_points[self.numvars.idx_stage][idx0] = self.sequences.states.vg[idx0]
    cpdef inline void set_result_states(self) nogil:
        cdef int idx0
        for idx0 in range(self.sequences.states._vg_length):
            self.sequences.states._vg_results[self.numvars.idx_method][idx0] = self.sequences.states.vg[idx0]
    cpdef inline void get_sum_fluxes(self) nogil:
        cdef int idx0
        self.sequences.fluxes.qza = self.sequences.fluxes._qza_sum
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes.qg[idx0] = self.sequences.fluxes._qg_sum[idx0]
        self.sequences.fluxes.qa = self.sequences.fluxes._qa_sum
    cpdef inline void set_point_fluxes(self) nogil:
        cdef int idx0
        self.sequences.fluxes._qza_points[self.numvars.idx_stage] = self.sequences.fluxes.qza
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes._qg_points[self.numvars.idx_stage][idx0] = self.sequences.fluxes.qg[idx0]
        self.sequences.fluxes._qa_points[self.numvars.idx_stage] = self.sequences.fluxes.qa
    cpdef inline void set_result_fluxes(self) nogil:
        cdef int idx0
        self.sequences.fluxes._qza_results[self.numvars.idx_method] = self.sequences.fluxes.qza
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes._qg_results[self.numvars.idx_method][idx0] = self.sequences.fluxes.qg[idx0]
        self.sequences.fluxes._qa_results[self.numvars.idx_method] = self.sequences.fluxes.qa
    cpdef inline void integrate_fluxes(self) nogil:
        cdef int jdx, idx0
        self.sequences.fluxes.qza = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.qza = self.sequences.fluxes.qza +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._qza_points[jdx]
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes.qg[idx0] = 0.
            for jdx in range(self.numvars.idx_method):
                self.sequences.fluxes.qg[idx0] = self.sequences.fluxes.qg[idx0] + self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._qg_points[jdx, idx0]
        self.sequences.fluxes.qa = 0.
        for jdx in range(self.numvars.idx_method):
            self.sequences.fluxes.qa = self.sequences.fluxes.qa +self.numvars.dt * self.numconsts.a_coefs[self.numvars.idx_method-1, self.numvars.idx_stage, jdx]*self.sequences.fluxes._qa_points[jdx]
    cpdef inline void reset_sum_fluxes(self) nogil:
        cdef int idx0
        self.sequences.fluxes._qza_sum = 0.
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes._qg_sum[idx0] = 0.
        self.sequences.fluxes._qa_sum = 0.
    cpdef inline void addup_fluxes(self) nogil:
        cdef int idx0
        self.sequences.fluxes._qza_sum = self.sequences.fluxes._qza_sum + self.sequences.fluxes.qza
        for idx0 in range(self.sequences.fluxes._qg_length):
            self.sequences.fluxes._qg_sum[idx0] = self.sequences.fluxes._qg_sum[idx0] + self.sequences.fluxes.qg[idx0]
        self.sequences.fluxes._qa_sum = self.sequences.fluxes._qa_sum + self.sequences.fluxes.qa
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
    cpdef inline void calc_qza_v1(self)  nogil:
        self.sequences.fluxes.qza = self.sequences.fluxes.qz
    cpdef inline void calc_qg_v2(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.parameters.control.vg2qg.inputs[0] = self.sequences.states.vg[i]
            self.parameters.control.vg2qg.calculate_values()
            self.sequences.fluxes.qg[i] = self.parameters.control.vg2qg.outputs[0]
    cpdef inline void calc_qa_v1(self)  nogil:
        self.sequences.fluxes.qa = self.sequences.fluxes.qg[self.parameters.control.gts - 1]
    cpdef inline void calc_qza(self)  nogil:
        self.sequences.fluxes.qza = self.sequences.fluxes.qz
    cpdef inline void calc_qg(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            self.parameters.control.vg2qg.inputs[0] = self.sequences.states.vg[i]
            self.parameters.control.vg2qg.calculate_values()
            self.sequences.fluxes.qg[i] = self.parameters.control.vg2qg.outputs[0]
    cpdef inline void calc_qa(self)  nogil:
        self.sequences.fluxes.qa = self.sequences.fluxes.qg[self.parameters.control.gts - 1]
    cpdef inline void update_vg_v1(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            if i:
                self.sequences.new_states.vg[i] = self.sequences.old_states.vg[i] + self.parameters.derived.sek * (self.sequences.fluxes.qg[i - 1] - self.sequences.fluxes.qg[i]) / 1e6
            else:
                self.sequences.new_states.vg[i] = self.sequences.old_states.vg[i] + self.parameters.derived.sek * (self.sequences.fluxes.qza - self.sequences.fluxes.qg[i]) / 1e6
    cpdef inline void update_vg(self)  nogil:
        cdef int i
        for i in range(self.parameters.control.gts):
            if i:
                self.sequences.new_states.vg[i] = self.sequences.old_states.vg[i] + self.parameters.derived.sek * (self.sequences.fluxes.qg[i - 1] - self.sequences.fluxes.qg[i]) / 1e6
            else:
                self.sequences.new_states.vg[i] = self.sequences.old_states.vg[i] + self.parameters.derived.sek * (self.sequences.fluxes.qza - self.sequences.fluxes.qg[i]) / 1e6
    cpdef inline void pass_q_v1(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.qa)
    cpdef inline void pass_q(self)  nogil:
        self.sequences.outlets.q[0] = self.sequences.outlets.q[0] + (self.sequences.fluxes.qa)
