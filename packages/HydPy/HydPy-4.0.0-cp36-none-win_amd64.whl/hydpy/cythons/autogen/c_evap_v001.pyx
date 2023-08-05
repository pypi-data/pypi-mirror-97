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
    cdef public double latitude
    cdef public double longitude
    cdef public double measuringheightwindspeed
    cdef public double[:] angstromconstant
    cdef public double[:] angstromfactor
@cython.final
cdef class DerivedParameters:
    cdef public numpy.int32_t[:] doy
    cdef public numpy.int32_t[:] moy
    cdef public double seconds
    cdef public double[:] sct
    cdef public numpy.int32_t utclongitude
    cdef public numpy.int32_t nmblogentries
    cdef public double latituderad
@cython.final
cdef class Sequences:
    cdef public InputSequences inputs
    cdef public FluxSequences fluxes
    cdef public LogSequences logs
@cython.final
cdef class InputSequences:
    cdef public double airtemperature
    cdef public int _airtemperature_ndim
    cdef public int _airtemperature_length
    cdef public bint _airtemperature_diskflag
    cdef public str _airtemperature_path
    cdef FILE *_airtemperature_file
    cdef public bint _airtemperature_ramflag
    cdef public double[:] _airtemperature_array
    cdef public bint _airtemperature_inputflag
    cdef double *_airtemperature_inputpointer
    cdef public double relativehumidity
    cdef public int _relativehumidity_ndim
    cdef public int _relativehumidity_length
    cdef public bint _relativehumidity_diskflag
    cdef public str _relativehumidity_path
    cdef FILE *_relativehumidity_file
    cdef public bint _relativehumidity_ramflag
    cdef public double[:] _relativehumidity_array
    cdef public bint _relativehumidity_inputflag
    cdef double *_relativehumidity_inputpointer
    cdef public double windspeed
    cdef public int _windspeed_ndim
    cdef public int _windspeed_length
    cdef public bint _windspeed_diskflag
    cdef public str _windspeed_path
    cdef FILE *_windspeed_file
    cdef public bint _windspeed_ramflag
    cdef public double[:] _windspeed_array
    cdef public bint _windspeed_inputflag
    cdef double *_windspeed_inputpointer
    cdef public double sunshineduration
    cdef public int _sunshineduration_ndim
    cdef public int _sunshineduration_length
    cdef public bint _sunshineduration_diskflag
    cdef public str _sunshineduration_path
    cdef FILE *_sunshineduration_file
    cdef public bint _sunshineduration_ramflag
    cdef public double[:] _sunshineduration_array
    cdef public bint _sunshineduration_inputflag
    cdef double *_sunshineduration_inputpointer
    cdef public double atmosphericpressure
    cdef public int _atmosphericpressure_ndim
    cdef public int _atmosphericpressure_length
    cdef public bint _atmosphericpressure_diskflag
    cdef public str _atmosphericpressure_path
    cdef FILE *_atmosphericpressure_file
    cdef public bint _atmosphericpressure_ramflag
    cdef public double[:] _atmosphericpressure_array
    cdef public bint _atmosphericpressure_inputflag
    cdef double *_atmosphericpressure_inputpointer
    cpdef open_files(self, int idx):
        if self._airtemperature_diskflag:
            self._airtemperature_file = fopen(str(self._airtemperature_path).encode(), "rb+")
            fseek(self._airtemperature_file, idx*8, SEEK_SET)
        if self._relativehumidity_diskflag:
            self._relativehumidity_file = fopen(str(self._relativehumidity_path).encode(), "rb+")
            fseek(self._relativehumidity_file, idx*8, SEEK_SET)
        if self._windspeed_diskflag:
            self._windspeed_file = fopen(str(self._windspeed_path).encode(), "rb+")
            fseek(self._windspeed_file, idx*8, SEEK_SET)
        if self._sunshineduration_diskflag:
            self._sunshineduration_file = fopen(str(self._sunshineduration_path).encode(), "rb+")
            fseek(self._sunshineduration_file, idx*8, SEEK_SET)
        if self._atmosphericpressure_diskflag:
            self._atmosphericpressure_file = fopen(str(self._atmosphericpressure_path).encode(), "rb+")
            fseek(self._atmosphericpressure_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._airtemperature_diskflag:
            fclose(self._airtemperature_file)
        if self._relativehumidity_diskflag:
            fclose(self._relativehumidity_file)
        if self._windspeed_diskflag:
            fclose(self._windspeed_file)
        if self._sunshineduration_diskflag:
            fclose(self._sunshineduration_file)
        if self._atmosphericpressure_diskflag:
            fclose(self._atmosphericpressure_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._airtemperature_inputflag:
            self.airtemperature = self._airtemperature_inputpointer[0]
        elif self._airtemperature_diskflag:
            fread(&self.airtemperature, 8, 1, self._airtemperature_file)
        elif self._airtemperature_ramflag:
            self.airtemperature = self._airtemperature_array[idx]
        if self._relativehumidity_inputflag:
            self.relativehumidity = self._relativehumidity_inputpointer[0]
        elif self._relativehumidity_diskflag:
            fread(&self.relativehumidity, 8, 1, self._relativehumidity_file)
        elif self._relativehumidity_ramflag:
            self.relativehumidity = self._relativehumidity_array[idx]
        if self._windspeed_inputflag:
            self.windspeed = self._windspeed_inputpointer[0]
        elif self._windspeed_diskflag:
            fread(&self.windspeed, 8, 1, self._windspeed_file)
        elif self._windspeed_ramflag:
            self.windspeed = self._windspeed_array[idx]
        if self._sunshineduration_inputflag:
            self.sunshineduration = self._sunshineduration_inputpointer[0]
        elif self._sunshineduration_diskflag:
            fread(&self.sunshineduration, 8, 1, self._sunshineduration_file)
        elif self._sunshineduration_ramflag:
            self.sunshineduration = self._sunshineduration_array[idx]
        if self._atmosphericpressure_inputflag:
            self.atmosphericpressure = self._atmosphericpressure_inputpointer[0]
        elif self._atmosphericpressure_diskflag:
            fread(&self.atmosphericpressure, 8, 1, self._atmosphericpressure_file)
        elif self._atmosphericpressure_ramflag:
            self.atmosphericpressure = self._atmosphericpressure_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._airtemperature_inputflag:
            if self._airtemperature_diskflag:
                fwrite(&self.airtemperature, 8, 1, self._airtemperature_file)
            elif self._airtemperature_ramflag:
                self._airtemperature_array[idx] = self.airtemperature
        if self._relativehumidity_inputflag:
            if self._relativehumidity_diskflag:
                fwrite(&self.relativehumidity, 8, 1, self._relativehumidity_file)
            elif self._relativehumidity_ramflag:
                self._relativehumidity_array[idx] = self.relativehumidity
        if self._windspeed_inputflag:
            if self._windspeed_diskflag:
                fwrite(&self.windspeed, 8, 1, self._windspeed_file)
            elif self._windspeed_ramflag:
                self._windspeed_array[idx] = self.windspeed
        if self._sunshineduration_inputflag:
            if self._sunshineduration_diskflag:
                fwrite(&self.sunshineduration, 8, 1, self._sunshineduration_file)
            elif self._sunshineduration_ramflag:
                self._sunshineduration_array[idx] = self.sunshineduration
        if self._atmosphericpressure_inputflag:
            if self._atmosphericpressure_diskflag:
                fwrite(&self.atmosphericpressure, 8, 1, self._atmosphericpressure_file)
            elif self._atmosphericpressure_ramflag:
                self._atmosphericpressure_array[idx] = self.atmosphericpressure
    cpdef inline set_pointerinput(self, str name, pointerutils.PDouble value):
        if name == "airtemperature":
            self._airtemperature_inputpointer = value.p_value
        if name == "relativehumidity":
            self._relativehumidity_inputpointer = value.p_value
        if name == "windspeed":
            self._windspeed_inputpointer = value.p_value
        if name == "sunshineduration":
            self._sunshineduration_inputpointer = value.p_value
        if name == "atmosphericpressure":
            self._atmosphericpressure_inputpointer = value.p_value
@cython.final
cdef class FluxSequences:
    cdef public double adjustedwindspeed
    cdef public int _adjustedwindspeed_ndim
    cdef public int _adjustedwindspeed_length
    cdef public bint _adjustedwindspeed_diskflag
    cdef public str _adjustedwindspeed_path
    cdef FILE *_adjustedwindspeed_file
    cdef public bint _adjustedwindspeed_ramflag
    cdef public double[:] _adjustedwindspeed_array
    cdef public bint _adjustedwindspeed_outputflag
    cdef double *_adjustedwindspeed_outputpointer
    cdef public double saturationvapourpressure
    cdef public int _saturationvapourpressure_ndim
    cdef public int _saturationvapourpressure_length
    cdef public bint _saturationvapourpressure_diskflag
    cdef public str _saturationvapourpressure_path
    cdef FILE *_saturationvapourpressure_file
    cdef public bint _saturationvapourpressure_ramflag
    cdef public double[:] _saturationvapourpressure_array
    cdef public bint _saturationvapourpressure_outputflag
    cdef double *_saturationvapourpressure_outputpointer
    cdef public double saturationvapourpressureslope
    cdef public int _saturationvapourpressureslope_ndim
    cdef public int _saturationvapourpressureslope_length
    cdef public bint _saturationvapourpressureslope_diskflag
    cdef public str _saturationvapourpressureslope_path
    cdef FILE *_saturationvapourpressureslope_file
    cdef public bint _saturationvapourpressureslope_ramflag
    cdef public double[:] _saturationvapourpressureslope_array
    cdef public bint _saturationvapourpressureslope_outputflag
    cdef double *_saturationvapourpressureslope_outputpointer
    cdef public double actualvapourpressure
    cdef public int _actualvapourpressure_ndim
    cdef public int _actualvapourpressure_length
    cdef public bint _actualvapourpressure_diskflag
    cdef public str _actualvapourpressure_path
    cdef FILE *_actualvapourpressure_file
    cdef public bint _actualvapourpressure_ramflag
    cdef public double[:] _actualvapourpressure_array
    cdef public bint _actualvapourpressure_outputflag
    cdef double *_actualvapourpressure_outputpointer
    cdef public double earthsundistance
    cdef public int _earthsundistance_ndim
    cdef public int _earthsundistance_length
    cdef public bint _earthsundistance_diskflag
    cdef public str _earthsundistance_path
    cdef FILE *_earthsundistance_file
    cdef public bint _earthsundistance_ramflag
    cdef public double[:] _earthsundistance_array
    cdef public bint _earthsundistance_outputflag
    cdef double *_earthsundistance_outputpointer
    cdef public double solardeclination
    cdef public int _solardeclination_ndim
    cdef public int _solardeclination_length
    cdef public bint _solardeclination_diskflag
    cdef public str _solardeclination_path
    cdef FILE *_solardeclination_file
    cdef public bint _solardeclination_ramflag
    cdef public double[:] _solardeclination_array
    cdef public bint _solardeclination_outputflag
    cdef double *_solardeclination_outputpointer
    cdef public double sunsethourangle
    cdef public int _sunsethourangle_ndim
    cdef public int _sunsethourangle_length
    cdef public bint _sunsethourangle_diskflag
    cdef public str _sunsethourangle_path
    cdef FILE *_sunsethourangle_file
    cdef public bint _sunsethourangle_ramflag
    cdef public double[:] _sunsethourangle_array
    cdef public bint _sunsethourangle_outputflag
    cdef double *_sunsethourangle_outputpointer
    cdef public double solartimeangle
    cdef public int _solartimeangle_ndim
    cdef public int _solartimeangle_length
    cdef public bint _solartimeangle_diskflag
    cdef public str _solartimeangle_path
    cdef FILE *_solartimeangle_file
    cdef public bint _solartimeangle_ramflag
    cdef public double[:] _solartimeangle_array
    cdef public bint _solartimeangle_outputflag
    cdef double *_solartimeangle_outputpointer
    cdef public double extraterrestrialradiation
    cdef public int _extraterrestrialradiation_ndim
    cdef public int _extraterrestrialradiation_length
    cdef public bint _extraterrestrialradiation_diskflag
    cdef public str _extraterrestrialradiation_path
    cdef FILE *_extraterrestrialradiation_file
    cdef public bint _extraterrestrialradiation_ramflag
    cdef public double[:] _extraterrestrialradiation_array
    cdef public bint _extraterrestrialradiation_outputflag
    cdef double *_extraterrestrialradiation_outputpointer
    cdef public double possiblesunshineduration
    cdef public int _possiblesunshineduration_ndim
    cdef public int _possiblesunshineduration_length
    cdef public bint _possiblesunshineduration_diskflag
    cdef public str _possiblesunshineduration_path
    cdef FILE *_possiblesunshineduration_file
    cdef public bint _possiblesunshineduration_ramflag
    cdef public double[:] _possiblesunshineduration_array
    cdef public bint _possiblesunshineduration_outputflag
    cdef double *_possiblesunshineduration_outputpointer
    cdef public double clearskysolarradiation
    cdef public int _clearskysolarradiation_ndim
    cdef public int _clearskysolarradiation_length
    cdef public bint _clearskysolarradiation_diskflag
    cdef public str _clearskysolarradiation_path
    cdef FILE *_clearskysolarradiation_file
    cdef public bint _clearskysolarradiation_ramflag
    cdef public double[:] _clearskysolarradiation_array
    cdef public bint _clearskysolarradiation_outputflag
    cdef double *_clearskysolarradiation_outputpointer
    cdef public double globalradiation
    cdef public int _globalradiation_ndim
    cdef public int _globalradiation_length
    cdef public bint _globalradiation_diskflag
    cdef public str _globalradiation_path
    cdef FILE *_globalradiation_file
    cdef public bint _globalradiation_ramflag
    cdef public double[:] _globalradiation_array
    cdef public bint _globalradiation_outputflag
    cdef double *_globalradiation_outputpointer
    cdef public double netshortwaveradiation
    cdef public int _netshortwaveradiation_ndim
    cdef public int _netshortwaveradiation_length
    cdef public bint _netshortwaveradiation_diskflag
    cdef public str _netshortwaveradiation_path
    cdef FILE *_netshortwaveradiation_file
    cdef public bint _netshortwaveradiation_ramflag
    cdef public double[:] _netshortwaveradiation_array
    cdef public bint _netshortwaveradiation_outputflag
    cdef double *_netshortwaveradiation_outputpointer
    cdef public double netlongwaveradiation
    cdef public int _netlongwaveradiation_ndim
    cdef public int _netlongwaveradiation_length
    cdef public bint _netlongwaveradiation_diskflag
    cdef public str _netlongwaveradiation_path
    cdef FILE *_netlongwaveradiation_file
    cdef public bint _netlongwaveradiation_ramflag
    cdef public double[:] _netlongwaveradiation_array
    cdef public bint _netlongwaveradiation_outputflag
    cdef double *_netlongwaveradiation_outputpointer
    cdef public double netradiation
    cdef public int _netradiation_ndim
    cdef public int _netradiation_length
    cdef public bint _netradiation_diskflag
    cdef public str _netradiation_path
    cdef FILE *_netradiation_file
    cdef public bint _netradiation_ramflag
    cdef public double[:] _netradiation_array
    cdef public bint _netradiation_outputflag
    cdef double *_netradiation_outputpointer
    cdef public double soilheatflux
    cdef public int _soilheatflux_ndim
    cdef public int _soilheatflux_length
    cdef public bint _soilheatflux_diskflag
    cdef public str _soilheatflux_path
    cdef FILE *_soilheatflux_file
    cdef public bint _soilheatflux_ramflag
    cdef public double[:] _soilheatflux_array
    cdef public bint _soilheatflux_outputflag
    cdef double *_soilheatflux_outputpointer
    cdef public double psychrometricconstant
    cdef public int _psychrometricconstant_ndim
    cdef public int _psychrometricconstant_length
    cdef public bint _psychrometricconstant_diskflag
    cdef public str _psychrometricconstant_path
    cdef FILE *_psychrometricconstant_file
    cdef public bint _psychrometricconstant_ramflag
    cdef public double[:] _psychrometricconstant_array
    cdef public bint _psychrometricconstant_outputflag
    cdef double *_psychrometricconstant_outputpointer
    cdef public double referenceevapotranspiration
    cdef public int _referenceevapotranspiration_ndim
    cdef public int _referenceevapotranspiration_length
    cdef public bint _referenceevapotranspiration_diskflag
    cdef public str _referenceevapotranspiration_path
    cdef FILE *_referenceevapotranspiration_file
    cdef public bint _referenceevapotranspiration_ramflag
    cdef public double[:] _referenceevapotranspiration_array
    cdef public bint _referenceevapotranspiration_outputflag
    cdef double *_referenceevapotranspiration_outputpointer
    cpdef open_files(self, int idx):
        if self._adjustedwindspeed_diskflag:
            self._adjustedwindspeed_file = fopen(str(self._adjustedwindspeed_path).encode(), "rb+")
            fseek(self._adjustedwindspeed_file, idx*8, SEEK_SET)
        if self._saturationvapourpressure_diskflag:
            self._saturationvapourpressure_file = fopen(str(self._saturationvapourpressure_path).encode(), "rb+")
            fseek(self._saturationvapourpressure_file, idx*8, SEEK_SET)
        if self._saturationvapourpressureslope_diskflag:
            self._saturationvapourpressureslope_file = fopen(str(self._saturationvapourpressureslope_path).encode(), "rb+")
            fseek(self._saturationvapourpressureslope_file, idx*8, SEEK_SET)
        if self._actualvapourpressure_diskflag:
            self._actualvapourpressure_file = fopen(str(self._actualvapourpressure_path).encode(), "rb+")
            fseek(self._actualvapourpressure_file, idx*8, SEEK_SET)
        if self._earthsundistance_diskflag:
            self._earthsundistance_file = fopen(str(self._earthsundistance_path).encode(), "rb+")
            fseek(self._earthsundistance_file, idx*8, SEEK_SET)
        if self._solardeclination_diskflag:
            self._solardeclination_file = fopen(str(self._solardeclination_path).encode(), "rb+")
            fseek(self._solardeclination_file, idx*8, SEEK_SET)
        if self._sunsethourangle_diskflag:
            self._sunsethourangle_file = fopen(str(self._sunsethourangle_path).encode(), "rb+")
            fseek(self._sunsethourangle_file, idx*8, SEEK_SET)
        if self._solartimeangle_diskflag:
            self._solartimeangle_file = fopen(str(self._solartimeangle_path).encode(), "rb+")
            fseek(self._solartimeangle_file, idx*8, SEEK_SET)
        if self._extraterrestrialradiation_diskflag:
            self._extraterrestrialradiation_file = fopen(str(self._extraterrestrialradiation_path).encode(), "rb+")
            fseek(self._extraterrestrialradiation_file, idx*8, SEEK_SET)
        if self._possiblesunshineduration_diskflag:
            self._possiblesunshineduration_file = fopen(str(self._possiblesunshineduration_path).encode(), "rb+")
            fseek(self._possiblesunshineduration_file, idx*8, SEEK_SET)
        if self._clearskysolarradiation_diskflag:
            self._clearskysolarradiation_file = fopen(str(self._clearskysolarradiation_path).encode(), "rb+")
            fseek(self._clearskysolarradiation_file, idx*8, SEEK_SET)
        if self._globalradiation_diskflag:
            self._globalradiation_file = fopen(str(self._globalradiation_path).encode(), "rb+")
            fseek(self._globalradiation_file, idx*8, SEEK_SET)
        if self._netshortwaveradiation_diskflag:
            self._netshortwaveradiation_file = fopen(str(self._netshortwaveradiation_path).encode(), "rb+")
            fseek(self._netshortwaveradiation_file, idx*8, SEEK_SET)
        if self._netlongwaveradiation_diskflag:
            self._netlongwaveradiation_file = fopen(str(self._netlongwaveradiation_path).encode(), "rb+")
            fseek(self._netlongwaveradiation_file, idx*8, SEEK_SET)
        if self._netradiation_diskflag:
            self._netradiation_file = fopen(str(self._netradiation_path).encode(), "rb+")
            fseek(self._netradiation_file, idx*8, SEEK_SET)
        if self._soilheatflux_diskflag:
            self._soilheatflux_file = fopen(str(self._soilheatflux_path).encode(), "rb+")
            fseek(self._soilheatflux_file, idx*8, SEEK_SET)
        if self._psychrometricconstant_diskflag:
            self._psychrometricconstant_file = fopen(str(self._psychrometricconstant_path).encode(), "rb+")
            fseek(self._psychrometricconstant_file, idx*8, SEEK_SET)
        if self._referenceevapotranspiration_diskflag:
            self._referenceevapotranspiration_file = fopen(str(self._referenceevapotranspiration_path).encode(), "rb+")
            fseek(self._referenceevapotranspiration_file, idx*8, SEEK_SET)
    cpdef inline close_files(self):
        if self._adjustedwindspeed_diskflag:
            fclose(self._adjustedwindspeed_file)
        if self._saturationvapourpressure_diskflag:
            fclose(self._saturationvapourpressure_file)
        if self._saturationvapourpressureslope_diskflag:
            fclose(self._saturationvapourpressureslope_file)
        if self._actualvapourpressure_diskflag:
            fclose(self._actualvapourpressure_file)
        if self._earthsundistance_diskflag:
            fclose(self._earthsundistance_file)
        if self._solardeclination_diskflag:
            fclose(self._solardeclination_file)
        if self._sunsethourangle_diskflag:
            fclose(self._sunsethourangle_file)
        if self._solartimeangle_diskflag:
            fclose(self._solartimeangle_file)
        if self._extraterrestrialradiation_diskflag:
            fclose(self._extraterrestrialradiation_file)
        if self._possiblesunshineduration_diskflag:
            fclose(self._possiblesunshineduration_file)
        if self._clearskysolarradiation_diskflag:
            fclose(self._clearskysolarradiation_file)
        if self._globalradiation_diskflag:
            fclose(self._globalradiation_file)
        if self._netshortwaveradiation_diskflag:
            fclose(self._netshortwaveradiation_file)
        if self._netlongwaveradiation_diskflag:
            fclose(self._netlongwaveradiation_file)
        if self._netradiation_diskflag:
            fclose(self._netradiation_file)
        if self._soilheatflux_diskflag:
            fclose(self._soilheatflux_file)
        if self._psychrometricconstant_diskflag:
            fclose(self._psychrometricconstant_file)
        if self._referenceevapotranspiration_diskflag:
            fclose(self._referenceevapotranspiration_file)
    cpdef inline void load_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._adjustedwindspeed_diskflag:
            fread(&self.adjustedwindspeed, 8, 1, self._adjustedwindspeed_file)
        elif self._adjustedwindspeed_ramflag:
            self.adjustedwindspeed = self._adjustedwindspeed_array[idx]
        if self._saturationvapourpressure_diskflag:
            fread(&self.saturationvapourpressure, 8, 1, self._saturationvapourpressure_file)
        elif self._saturationvapourpressure_ramflag:
            self.saturationvapourpressure = self._saturationvapourpressure_array[idx]
        if self._saturationvapourpressureslope_diskflag:
            fread(&self.saturationvapourpressureslope, 8, 1, self._saturationvapourpressureslope_file)
        elif self._saturationvapourpressureslope_ramflag:
            self.saturationvapourpressureslope = self._saturationvapourpressureslope_array[idx]
        if self._actualvapourpressure_diskflag:
            fread(&self.actualvapourpressure, 8, 1, self._actualvapourpressure_file)
        elif self._actualvapourpressure_ramflag:
            self.actualvapourpressure = self._actualvapourpressure_array[idx]
        if self._earthsundistance_diskflag:
            fread(&self.earthsundistance, 8, 1, self._earthsundistance_file)
        elif self._earthsundistance_ramflag:
            self.earthsundistance = self._earthsundistance_array[idx]
        if self._solardeclination_diskflag:
            fread(&self.solardeclination, 8, 1, self._solardeclination_file)
        elif self._solardeclination_ramflag:
            self.solardeclination = self._solardeclination_array[idx]
        if self._sunsethourangle_diskflag:
            fread(&self.sunsethourangle, 8, 1, self._sunsethourangle_file)
        elif self._sunsethourangle_ramflag:
            self.sunsethourangle = self._sunsethourangle_array[idx]
        if self._solartimeangle_diskflag:
            fread(&self.solartimeangle, 8, 1, self._solartimeangle_file)
        elif self._solartimeangle_ramflag:
            self.solartimeangle = self._solartimeangle_array[idx]
        if self._extraterrestrialradiation_diskflag:
            fread(&self.extraterrestrialradiation, 8, 1, self._extraterrestrialradiation_file)
        elif self._extraterrestrialradiation_ramflag:
            self.extraterrestrialradiation = self._extraterrestrialradiation_array[idx]
        if self._possiblesunshineduration_diskflag:
            fread(&self.possiblesunshineduration, 8, 1, self._possiblesunshineduration_file)
        elif self._possiblesunshineduration_ramflag:
            self.possiblesunshineduration = self._possiblesunshineduration_array[idx]
        if self._clearskysolarradiation_diskflag:
            fread(&self.clearskysolarradiation, 8, 1, self._clearskysolarradiation_file)
        elif self._clearskysolarradiation_ramflag:
            self.clearskysolarradiation = self._clearskysolarradiation_array[idx]
        if self._globalradiation_diskflag:
            fread(&self.globalradiation, 8, 1, self._globalradiation_file)
        elif self._globalradiation_ramflag:
            self.globalradiation = self._globalradiation_array[idx]
        if self._netshortwaveradiation_diskflag:
            fread(&self.netshortwaveradiation, 8, 1, self._netshortwaveradiation_file)
        elif self._netshortwaveradiation_ramflag:
            self.netshortwaveradiation = self._netshortwaveradiation_array[idx]
        if self._netlongwaveradiation_diskflag:
            fread(&self.netlongwaveradiation, 8, 1, self._netlongwaveradiation_file)
        elif self._netlongwaveradiation_ramflag:
            self.netlongwaveradiation = self._netlongwaveradiation_array[idx]
        if self._netradiation_diskflag:
            fread(&self.netradiation, 8, 1, self._netradiation_file)
        elif self._netradiation_ramflag:
            self.netradiation = self._netradiation_array[idx]
        if self._soilheatflux_diskflag:
            fread(&self.soilheatflux, 8, 1, self._soilheatflux_file)
        elif self._soilheatflux_ramflag:
            self.soilheatflux = self._soilheatflux_array[idx]
        if self._psychrometricconstant_diskflag:
            fread(&self.psychrometricconstant, 8, 1, self._psychrometricconstant_file)
        elif self._psychrometricconstant_ramflag:
            self.psychrometricconstant = self._psychrometricconstant_array[idx]
        if self._referenceevapotranspiration_diskflag:
            fread(&self.referenceevapotranspiration, 8, 1, self._referenceevapotranspiration_file)
        elif self._referenceevapotranspiration_ramflag:
            self.referenceevapotranspiration = self._referenceevapotranspiration_array[idx]
    cpdef inline void save_data(self, int idx)  nogil:
        cdef int jdx0, jdx1, jdx2, jdx3, jdx4, jdx5
        if self._adjustedwindspeed_diskflag:
            fwrite(&self.adjustedwindspeed, 8, 1, self._adjustedwindspeed_file)
        elif self._adjustedwindspeed_ramflag:
            self._adjustedwindspeed_array[idx] = self.adjustedwindspeed
        if self._saturationvapourpressure_diskflag:
            fwrite(&self.saturationvapourpressure, 8, 1, self._saturationvapourpressure_file)
        elif self._saturationvapourpressure_ramflag:
            self._saturationvapourpressure_array[idx] = self.saturationvapourpressure
        if self._saturationvapourpressureslope_diskflag:
            fwrite(&self.saturationvapourpressureslope, 8, 1, self._saturationvapourpressureslope_file)
        elif self._saturationvapourpressureslope_ramflag:
            self._saturationvapourpressureslope_array[idx] = self.saturationvapourpressureslope
        if self._actualvapourpressure_diskflag:
            fwrite(&self.actualvapourpressure, 8, 1, self._actualvapourpressure_file)
        elif self._actualvapourpressure_ramflag:
            self._actualvapourpressure_array[idx] = self.actualvapourpressure
        if self._earthsundistance_diskflag:
            fwrite(&self.earthsundistance, 8, 1, self._earthsundistance_file)
        elif self._earthsundistance_ramflag:
            self._earthsundistance_array[idx] = self.earthsundistance
        if self._solardeclination_diskflag:
            fwrite(&self.solardeclination, 8, 1, self._solardeclination_file)
        elif self._solardeclination_ramflag:
            self._solardeclination_array[idx] = self.solardeclination
        if self._sunsethourangle_diskflag:
            fwrite(&self.sunsethourangle, 8, 1, self._sunsethourangle_file)
        elif self._sunsethourangle_ramflag:
            self._sunsethourangle_array[idx] = self.sunsethourangle
        if self._solartimeangle_diskflag:
            fwrite(&self.solartimeangle, 8, 1, self._solartimeangle_file)
        elif self._solartimeangle_ramflag:
            self._solartimeangle_array[idx] = self.solartimeangle
        if self._extraterrestrialradiation_diskflag:
            fwrite(&self.extraterrestrialradiation, 8, 1, self._extraterrestrialradiation_file)
        elif self._extraterrestrialradiation_ramflag:
            self._extraterrestrialradiation_array[idx] = self.extraterrestrialradiation
        if self._possiblesunshineduration_diskflag:
            fwrite(&self.possiblesunshineduration, 8, 1, self._possiblesunshineduration_file)
        elif self._possiblesunshineduration_ramflag:
            self._possiblesunshineduration_array[idx] = self.possiblesunshineduration
        if self._clearskysolarradiation_diskflag:
            fwrite(&self.clearskysolarradiation, 8, 1, self._clearskysolarradiation_file)
        elif self._clearskysolarradiation_ramflag:
            self._clearskysolarradiation_array[idx] = self.clearskysolarradiation
        if self._globalradiation_diskflag:
            fwrite(&self.globalradiation, 8, 1, self._globalradiation_file)
        elif self._globalradiation_ramflag:
            self._globalradiation_array[idx] = self.globalradiation
        if self._netshortwaveradiation_diskflag:
            fwrite(&self.netshortwaveradiation, 8, 1, self._netshortwaveradiation_file)
        elif self._netshortwaveradiation_ramflag:
            self._netshortwaveradiation_array[idx] = self.netshortwaveradiation
        if self._netlongwaveradiation_diskflag:
            fwrite(&self.netlongwaveradiation, 8, 1, self._netlongwaveradiation_file)
        elif self._netlongwaveradiation_ramflag:
            self._netlongwaveradiation_array[idx] = self.netlongwaveradiation
        if self._netradiation_diskflag:
            fwrite(&self.netradiation, 8, 1, self._netradiation_file)
        elif self._netradiation_ramflag:
            self._netradiation_array[idx] = self.netradiation
        if self._soilheatflux_diskflag:
            fwrite(&self.soilheatflux, 8, 1, self._soilheatflux_file)
        elif self._soilheatflux_ramflag:
            self._soilheatflux_array[idx] = self.soilheatflux
        if self._psychrometricconstant_diskflag:
            fwrite(&self.psychrometricconstant, 8, 1, self._psychrometricconstant_file)
        elif self._psychrometricconstant_ramflag:
            self._psychrometricconstant_array[idx] = self.psychrometricconstant
        if self._referenceevapotranspiration_diskflag:
            fwrite(&self.referenceevapotranspiration, 8, 1, self._referenceevapotranspiration_file)
        elif self._referenceevapotranspiration_ramflag:
            self._referenceevapotranspiration_array[idx] = self.referenceevapotranspiration
    cpdef inline set_pointeroutput(self, str name, pointerutils.PDouble value):
        if name == "adjustedwindspeed":
            self._adjustedwindspeed_outputpointer = value.p_value
        if name == "saturationvapourpressure":
            self._saturationvapourpressure_outputpointer = value.p_value
        if name == "saturationvapourpressureslope":
            self._saturationvapourpressureslope_outputpointer = value.p_value
        if name == "actualvapourpressure":
            self._actualvapourpressure_outputpointer = value.p_value
        if name == "earthsundistance":
            self._earthsundistance_outputpointer = value.p_value
        if name == "solardeclination":
            self._solardeclination_outputpointer = value.p_value
        if name == "sunsethourangle":
            self._sunsethourangle_outputpointer = value.p_value
        if name == "solartimeangle":
            self._solartimeangle_outputpointer = value.p_value
        if name == "extraterrestrialradiation":
            self._extraterrestrialradiation_outputpointer = value.p_value
        if name == "possiblesunshineduration":
            self._possiblesunshineduration_outputpointer = value.p_value
        if name == "clearskysolarradiation":
            self._clearskysolarradiation_outputpointer = value.p_value
        if name == "globalradiation":
            self._globalradiation_outputpointer = value.p_value
        if name == "netshortwaveradiation":
            self._netshortwaveradiation_outputpointer = value.p_value
        if name == "netlongwaveradiation":
            self._netlongwaveradiation_outputpointer = value.p_value
        if name == "netradiation":
            self._netradiation_outputpointer = value.p_value
        if name == "soilheatflux":
            self._soilheatflux_outputpointer = value.p_value
        if name == "psychrometricconstant":
            self._psychrometricconstant_outputpointer = value.p_value
        if name == "referenceevapotranspiration":
            self._referenceevapotranspiration_outputpointer = value.p_value
    cpdef inline void update_outputs(self) nogil:
        if self._adjustedwindspeed_outputflag:
            self._adjustedwindspeed_outputpointer[0] = self.adjustedwindspeed
        if self._saturationvapourpressure_outputflag:
            self._saturationvapourpressure_outputpointer[0] = self.saturationvapourpressure
        if self._saturationvapourpressureslope_outputflag:
            self._saturationvapourpressureslope_outputpointer[0] = self.saturationvapourpressureslope
        if self._actualvapourpressure_outputflag:
            self._actualvapourpressure_outputpointer[0] = self.actualvapourpressure
        if self._earthsundistance_outputflag:
            self._earthsundistance_outputpointer[0] = self.earthsundistance
        if self._solardeclination_outputflag:
            self._solardeclination_outputpointer[0] = self.solardeclination
        if self._sunsethourangle_outputflag:
            self._sunsethourangle_outputpointer[0] = self.sunsethourangle
        if self._solartimeangle_outputflag:
            self._solartimeangle_outputpointer[0] = self.solartimeangle
        if self._extraterrestrialradiation_outputflag:
            self._extraterrestrialradiation_outputpointer[0] = self.extraterrestrialradiation
        if self._possiblesunshineduration_outputflag:
            self._possiblesunshineduration_outputpointer[0] = self.possiblesunshineduration
        if self._clearskysolarradiation_outputflag:
            self._clearskysolarradiation_outputpointer[0] = self.clearskysolarradiation
        if self._globalradiation_outputflag:
            self._globalradiation_outputpointer[0] = self.globalradiation
        if self._netshortwaveradiation_outputflag:
            self._netshortwaveradiation_outputpointer[0] = self.netshortwaveradiation
        if self._netlongwaveradiation_outputflag:
            self._netlongwaveradiation_outputpointer[0] = self.netlongwaveradiation
        if self._netradiation_outputflag:
            self._netradiation_outputpointer[0] = self.netradiation
        if self._soilheatflux_outputflag:
            self._soilheatflux_outputpointer[0] = self.soilheatflux
        if self._psychrometricconstant_outputflag:
            self._psychrometricconstant_outputpointer[0] = self.psychrometricconstant
        if self._referenceevapotranspiration_outputflag:
            self._referenceevapotranspiration_outputpointer[0] = self.referenceevapotranspiration
@cython.final
cdef class LogSequences:
    cdef public double[:] loggedglobalradiation
    cdef public int _loggedglobalradiation_ndim
    cdef public int _loggedglobalradiation_length
    cdef public int _loggedglobalradiation_length_0
    cdef public double[:] loggedclearskysolarradiation
    cdef public int _loggedclearskysolarradiation_ndim
    cdef public int _loggedclearskysolarradiation_length
    cdef public int _loggedclearskysolarradiation_length_0


@cython.final
cdef class Model:
    cdef public int idx_sim
    cdef public Parameters parameters
    cdef public Sequences sequences
    cpdef inline void simulate(self, int idx)  nogil:
        self.idx_sim = idx
        self.load_data()
        self.run()
        self.update_outputs()
    cpdef inline void open_files(self):
        self.sequences.inputs.open_files(self.idx_sim)
        self.sequences.fluxes.open_files(self.idx_sim)
    cpdef inline void close_files(self):
        self.sequences.inputs.close_files()
        self.sequences.fluxes.close_files()
    cpdef inline void load_data(self) nogil:
        self.sequences.inputs.load_data(self.idx_sim)
    cpdef inline void save_data(self, int idx) nogil:
        self.sequences.inputs.save_data(self.idx_sim)
        self.sequences.fluxes.save_data(self.idx_sim)
    cpdef inline void run(self) nogil:
        self.calc_adjustedwindspeed_v1()
        self.calc_saturationvapourpressure_v1()
        self.calc_saturationvapourpressureslope_v1()
        self.calc_actualvapourpressure_v1()
        self.calc_earthsundistance_v1()
        self.calc_solardeclination_v1()
        self.calc_sunsethourangle_v1()
        self.calc_solartimeangle_v1()
        self.calc_extraterrestrialradiation_v1()
        self.calc_possiblesunshineduration_v1()
        self.calc_clearskysolarradiation_v1()
        self.update_loggedclearskysolarradiation_v1()
        self.calc_globalradiation_v1()
        self.update_loggedglobalradiation_v1()
        self.calc_netshortwaveradiation_v1()
        self.calc_netlongwaveradiation_v1()
        self.calc_netradiation_v1()
        self.calc_soilheatflux_v1()
        self.calc_psychrometricconstant_v1()
        self.calc_referenceevapotranspiration_v1()
    cpdef inline void update_inlets(self) nogil:
        pass
    cpdef inline void update_outlets(self) nogil:
        pass
    cpdef inline void update_receivers(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_senders(self, int idx) nogil:
        self.idx_sim = idx
        pass
    cpdef inline void update_outputs(self) nogil:
        self.sequences.fluxes.update_outputs()

    cpdef inline void calc_adjustedwindspeed_v1(self)  nogil:
        cdef double d_z0
        cdef double d_d
        d_d = 2.0 / 3.0 * 0.12
        d_z0 = 0.123 * 0.12
        self.sequences.fluxes.adjustedwindspeed = self.sequences.inputs.windspeed * (            log((2.0 - d_d) / d_z0)            / log((self.parameters.control.measuringheightwindspeed - d_d) / d_z0)        )
    cpdef inline void calc_saturationvapourpressure_v1(self)  nogil:
        self.sequences.fluxes.saturationvapourpressure = 0.6108 * exp(            17.27 * self.sequences.inputs.airtemperature / (self.sequences.inputs.airtemperature + 237.3)        )
    cpdef inline void calc_saturationvapourpressureslope_v1(self)  nogil:
        self.sequences.fluxes.saturationvapourpressureslope = (            4098.0 * self.sequences.fluxes.saturationvapourpressure / (self.sequences.inputs.airtemperature + 237.3) ** 2        )
    cpdef inline void calc_actualvapourpressure_v1(self)  nogil:
        self.sequences.fluxes.actualvapourpressure = (            self.sequences.fluxes.saturationvapourpressure * self.sequences.inputs.relativehumidity / 100.0        )
    cpdef inline void calc_earthsundistance_v1(self)  nogil:
        self.sequences.fluxes.earthsundistance = 1.0 + 0.033 * cos(            2 * 3.141592653589793 / 366.0 * (self.parameters.derived.doy[self.idx_sim] + 1)        )
    cpdef inline void calc_solardeclination_v1(self)  nogil:
        self.sequences.fluxes.solardeclination = 0.409 * sin(            2 * 3.141592653589793 / 366 * (self.parameters.derived.doy[self.idx_sim] + 1) - 1.39        )
    cpdef inline void calc_sunsethourangle_v1(self)  nogil:
        self.sequences.fluxes.sunsethourangle = acos(            -tan(self.parameters.derived.latituderad) * tan(self.sequences.fluxes.solardeclination)        )
    cpdef inline void calc_solartimeangle_v1(self)  nogil:
        cdef double d_sc
        cdef double d_b
        cdef double d_pi
        d_pi = 3.141592653589793
        d_b = 2.0 * d_pi * (self.parameters.derived.doy[self.idx_sim] - 80.0) / 365.0
        d_sc = (            0.1645 * sin(2.0 * d_b)            - 0.1255 * cos(d_b)            - 0.025 * sin(d_b)        )
        self.sequences.fluxes.solartimeangle = (            d_pi            / 12.0            * (                (                    self.parameters.derived.sct[self.idx_sim]                    + (self.parameters.control.longitude - self.parameters.derived.utclongitude) / 15.0                    + d_sc                )                - 12.0            )        )
    cpdef inline void calc_extraterrestrialradiation_v1(self)  nogil:
        cdef double d_omega2
        cdef double d_omega1
        cdef double d_delta
        cdef double d_pi
        d_pi = 3.141592653589793
        if self.parameters.derived.seconds < 60.0 * 60.0 * 24.0:
            d_delta = d_pi * self.parameters.derived.seconds / 60.0 / 60.0 / 24.0
            d_omega1 = self.sequences.fluxes.solartimeangle - d_delta
            d_omega2 = self.sequences.fluxes.solartimeangle + d_delta
            self.sequences.fluxes.extraterrestrialradiation = max(                12.0                * 4.92                / d_pi                * self.sequences.fluxes.earthsundistance                * (                    (                        (d_omega2 - d_omega1)                        * sin(self.parameters.derived.latituderad)                        * sin(self.sequences.fluxes.solardeclination)                    )                    + (                        cos(self.parameters.derived.latituderad)                        * cos(self.sequences.fluxes.solardeclination)                        * (sin(d_omega2) - sin(d_omega1))                    )                ),                0.0,            )
        else:
            self.sequences.fluxes.extraterrestrialradiation = (                self.parameters.derived.seconds                * 0.0820                / 60.0                / d_pi                * self.sequences.fluxes.earthsundistance                * (                    (                        self.sequences.fluxes.sunsethourangle                        * sin(self.parameters.derived.latituderad)                        * sin(self.sequences.fluxes.solardeclination)                    )                    + (                        cos(self.parameters.derived.latituderad)                        * cos(self.sequences.fluxes.solardeclination)                        * sin(self.sequences.fluxes.sunsethourangle)                    )                )            )
    cpdef inline void calc_possiblesunshineduration_v1(self)  nogil:
        cdef double d_thresh
        cdef double d_days
        cdef double d_hours
        cdef double d_pi
        d_pi = 3.141592653589793
        d_hours = self.parameters.derived.seconds / 60.0 / 60.0
        d_days = d_hours / 24.0
        if d_hours < 24.0:
            if self.sequences.fluxes.solartimeangle <= 0.0:
                d_thresh = -self.sequences.fluxes.solartimeangle - d_pi * d_days
            else:
                d_thresh = self.sequences.fluxes.solartimeangle - d_pi * d_days
            self.sequences.fluxes.possiblesunshineduration = min(                max(12.0 / d_pi * (self.sequences.fluxes.sunsethourangle - d_thresh), 0.0), d_hours            )
        else:
            self.sequences.fluxes.possiblesunshineduration = 24.0 / d_pi * self.sequences.fluxes.sunsethourangle
    cpdef inline void calc_clearskysolarradiation_v1(self)  nogil:
        cdef int idx
        idx = self.parameters.derived.moy[self.idx_sim]
        self.sequences.fluxes.clearskysolarradiation = self.sequences.fluxes.extraterrestrialradiation * (            self.parameters.control.angstromconstant[idx] + self.parameters.control.angstromfactor[idx]        )
    cpdef inline void update_loggedclearskysolarradiation_v1(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedclearskysolarradiation[idx] = self.sequences.logs.loggedclearskysolarradiation[                idx - 1            ]
        self.sequences.logs.loggedclearskysolarradiation[0] = self.sequences.fluxes.clearskysolarradiation
    cpdef inline void calc_globalradiation_v1(self)  nogil:
        cdef int idx
        if self.sequences.fluxes.possiblesunshineduration > 0.0:
            idx = self.parameters.derived.moy[self.idx_sim]
            self.sequences.fluxes.globalradiation = self.sequences.fluxes.extraterrestrialradiation * (                self.parameters.control.angstromconstant[idx]                + self.parameters.control.angstromfactor[idx]                * self.sequences.inputs.sunshineduration                / self.sequences.fluxes.possiblesunshineduration            )
        else:
            self.sequences.fluxes.globalradiation = 0.0
    cpdef inline void update_loggedglobalradiation_v1(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedglobalradiation[idx] = self.sequences.logs.loggedglobalradiation[idx - 1]
        self.sequences.logs.loggedglobalradiation[0] = self.sequences.fluxes.globalradiation
    cpdef inline void calc_netshortwaveradiation_v1(self)  nogil:
        self.sequences.fluxes.netshortwaveradiation = (1.0 - 0.23) * self.sequences.fluxes.globalradiation
    cpdef inline void calc_netlongwaveradiation_v1(self)  nogil:
        cdef int idx
        cdef double d_clearskysolarradiation
        cdef double d_globalradiation
        if self.sequences.fluxes.clearskysolarradiation > 0.0:
            d_globalradiation = self.sequences.fluxes.globalradiation
            d_clearskysolarradiation = self.sequences.fluxes.clearskysolarradiation
        else:
            d_globalradiation = 0.0
            d_clearskysolarradiation = 0.0
            for idx in range(self.parameters.derived.nmblogentries):
                d_clearskysolarradiation = d_clearskysolarradiation + (self.sequences.logs.loggedclearskysolarradiation[idx])
                d_globalradiation = d_globalradiation + (self.sequences.logs.loggedglobalradiation[idx])
        self.sequences.fluxes.netlongwaveradiation = (            4.903e-9            / 24.0            / 60.0            / 60.0            * self.parameters.derived.seconds            * (self.sequences.inputs.airtemperature + 273.16) ** 4            * (0.34 - 0.14 * self.sequences.fluxes.actualvapourpressure ** 0.5)            * (1.35 * d_globalradiation / d_clearskysolarradiation - 0.35)        )
    cpdef inline void calc_netradiation_v1(self)  nogil:
        self.sequences.fluxes.netradiation = self.sequences.fluxes.netshortwaveradiation - self.sequences.fluxes.netlongwaveradiation
    cpdef inline void calc_soilheatflux_v1(self)  nogil:
        if self.parameters.derived.seconds < 60.0 * 60.0 * 24.0:
            if self.sequences.fluxes.netradiation >= 0.0:
                self.sequences.fluxes.soilheatflux = 0.1 * self.sequences.fluxes.netradiation
            else:
                self.sequences.fluxes.soilheatflux = 0.5 * self.sequences.fluxes.netradiation
        else:
            self.sequences.fluxes.soilheatflux = 0.0
    cpdef inline void calc_psychrometricconstant_v1(self)  nogil:
        self.sequences.fluxes.psychrometricconstant = 6.65e-4 * self.sequences.inputs.atmosphericpressure
    cpdef inline void calc_referenceevapotranspiration_v1(self)  nogil:
        self.sequences.fluxes.referenceevapotranspiration = (            0.408            * self.sequences.fluxes.saturationvapourpressureslope            * (self.sequences.fluxes.netradiation - self.sequences.fluxes.soilheatflux)            + self.sequences.fluxes.psychrometricconstant            * (37.5 / 60.0 / 60.0 * self.parameters.derived.seconds)            / (self.sequences.inputs.airtemperature + 273.0)            * self.sequences.fluxes.adjustedwindspeed            * (self.sequences.fluxes.saturationvapourpressure - self.sequences.fluxes.actualvapourpressure)        ) / (            self.sequences.fluxes.saturationvapourpressureslope            + self.sequences.fluxes.psychrometricconstant * (1.0 + 0.34 * self.sequences.fluxes.adjustedwindspeed)        )
    cpdef inline void calc_adjustedwindspeed(self)  nogil:
        cdef double d_z0
        cdef double d_d
        d_d = 2.0 / 3.0 * 0.12
        d_z0 = 0.123 * 0.12
        self.sequences.fluxes.adjustedwindspeed = self.sequences.inputs.windspeed * (            log((2.0 - d_d) / d_z0)            / log((self.parameters.control.measuringheightwindspeed - d_d) / d_z0)        )
    cpdef inline void calc_saturationvapourpressure(self)  nogil:
        self.sequences.fluxes.saturationvapourpressure = 0.6108 * exp(            17.27 * self.sequences.inputs.airtemperature / (self.sequences.inputs.airtemperature + 237.3)        )
    cpdef inline void calc_saturationvapourpressureslope(self)  nogil:
        self.sequences.fluxes.saturationvapourpressureslope = (            4098.0 * self.sequences.fluxes.saturationvapourpressure / (self.sequences.inputs.airtemperature + 237.3) ** 2        )
    cpdef inline void calc_actualvapourpressure(self)  nogil:
        self.sequences.fluxes.actualvapourpressure = (            self.sequences.fluxes.saturationvapourpressure * self.sequences.inputs.relativehumidity / 100.0        )
    cpdef inline void calc_earthsundistance(self)  nogil:
        self.sequences.fluxes.earthsundistance = 1.0 + 0.033 * cos(            2 * 3.141592653589793 / 366.0 * (self.parameters.derived.doy[self.idx_sim] + 1)        )
    cpdef inline void calc_solardeclination(self)  nogil:
        self.sequences.fluxes.solardeclination = 0.409 * sin(            2 * 3.141592653589793 / 366 * (self.parameters.derived.doy[self.idx_sim] + 1) - 1.39        )
    cpdef inline void calc_sunsethourangle(self)  nogil:
        self.sequences.fluxes.sunsethourangle = acos(            -tan(self.parameters.derived.latituderad) * tan(self.sequences.fluxes.solardeclination)        )
    cpdef inline void calc_solartimeangle(self)  nogil:
        cdef double d_sc
        cdef double d_b
        cdef double d_pi
        d_pi = 3.141592653589793
        d_b = 2.0 * d_pi * (self.parameters.derived.doy[self.idx_sim] - 80.0) / 365.0
        d_sc = (            0.1645 * sin(2.0 * d_b)            - 0.1255 * cos(d_b)            - 0.025 * sin(d_b)        )
        self.sequences.fluxes.solartimeangle = (            d_pi            / 12.0            * (                (                    self.parameters.derived.sct[self.idx_sim]                    + (self.parameters.control.longitude - self.parameters.derived.utclongitude) / 15.0                    + d_sc                )                - 12.0            )        )
    cpdef inline void calc_extraterrestrialradiation(self)  nogil:
        cdef double d_omega2
        cdef double d_omega1
        cdef double d_delta
        cdef double d_pi
        d_pi = 3.141592653589793
        if self.parameters.derived.seconds < 60.0 * 60.0 * 24.0:
            d_delta = d_pi * self.parameters.derived.seconds / 60.0 / 60.0 / 24.0
            d_omega1 = self.sequences.fluxes.solartimeangle - d_delta
            d_omega2 = self.sequences.fluxes.solartimeangle + d_delta
            self.sequences.fluxes.extraterrestrialradiation = max(                12.0                * 4.92                / d_pi                * self.sequences.fluxes.earthsundistance                * (                    (                        (d_omega2 - d_omega1)                        * sin(self.parameters.derived.latituderad)                        * sin(self.sequences.fluxes.solardeclination)                    )                    + (                        cos(self.parameters.derived.latituderad)                        * cos(self.sequences.fluxes.solardeclination)                        * (sin(d_omega2) - sin(d_omega1))                    )                ),                0.0,            )
        else:
            self.sequences.fluxes.extraterrestrialradiation = (                self.parameters.derived.seconds                * 0.0820                / 60.0                / d_pi                * self.sequences.fluxes.earthsundistance                * (                    (                        self.sequences.fluxes.sunsethourangle                        * sin(self.parameters.derived.latituderad)                        * sin(self.sequences.fluxes.solardeclination)                    )                    + (                        cos(self.parameters.derived.latituderad)                        * cos(self.sequences.fluxes.solardeclination)                        * sin(self.sequences.fluxes.sunsethourangle)                    )                )            )
    cpdef inline void calc_possiblesunshineduration(self)  nogil:
        cdef double d_thresh
        cdef double d_days
        cdef double d_hours
        cdef double d_pi
        d_pi = 3.141592653589793
        d_hours = self.parameters.derived.seconds / 60.0 / 60.0
        d_days = d_hours / 24.0
        if d_hours < 24.0:
            if self.sequences.fluxes.solartimeangle <= 0.0:
                d_thresh = -self.sequences.fluxes.solartimeangle - d_pi * d_days
            else:
                d_thresh = self.sequences.fluxes.solartimeangle - d_pi * d_days
            self.sequences.fluxes.possiblesunshineduration = min(                max(12.0 / d_pi * (self.sequences.fluxes.sunsethourangle - d_thresh), 0.0), d_hours            )
        else:
            self.sequences.fluxes.possiblesunshineduration = 24.0 / d_pi * self.sequences.fluxes.sunsethourangle
    cpdef inline void calc_clearskysolarradiation(self)  nogil:
        cdef int idx
        idx = self.parameters.derived.moy[self.idx_sim]
        self.sequences.fluxes.clearskysolarradiation = self.sequences.fluxes.extraterrestrialradiation * (            self.parameters.control.angstromconstant[idx] + self.parameters.control.angstromfactor[idx]        )
    cpdef inline void update_loggedclearskysolarradiation(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedclearskysolarradiation[idx] = self.sequences.logs.loggedclearskysolarradiation[                idx - 1            ]
        self.sequences.logs.loggedclearskysolarradiation[0] = self.sequences.fluxes.clearskysolarradiation
    cpdef inline void calc_globalradiation(self)  nogil:
        cdef int idx
        if self.sequences.fluxes.possiblesunshineduration > 0.0:
            idx = self.parameters.derived.moy[self.idx_sim]
            self.sequences.fluxes.globalradiation = self.sequences.fluxes.extraterrestrialradiation * (                self.parameters.control.angstromconstant[idx]                + self.parameters.control.angstromfactor[idx]                * self.sequences.inputs.sunshineduration                / self.sequences.fluxes.possiblesunshineduration            )
        else:
            self.sequences.fluxes.globalradiation = 0.0
    cpdef inline void update_loggedglobalradiation(self)  nogil:
        cdef int idx
        for idx in range(self.parameters.derived.nmblogentries - 1, 0, -1):
            self.sequences.logs.loggedglobalradiation[idx] = self.sequences.logs.loggedglobalradiation[idx - 1]
        self.sequences.logs.loggedglobalradiation[0] = self.sequences.fluxes.globalradiation
    cpdef inline void calc_netshortwaveradiation(self)  nogil:
        self.sequences.fluxes.netshortwaveradiation = (1.0 - 0.23) * self.sequences.fluxes.globalradiation
    cpdef inline void calc_netlongwaveradiation(self)  nogil:
        cdef int idx
        cdef double d_clearskysolarradiation
        cdef double d_globalradiation
        if self.sequences.fluxes.clearskysolarradiation > 0.0:
            d_globalradiation = self.sequences.fluxes.globalradiation
            d_clearskysolarradiation = self.sequences.fluxes.clearskysolarradiation
        else:
            d_globalradiation = 0.0
            d_clearskysolarradiation = 0.0
            for idx in range(self.parameters.derived.nmblogentries):
                d_clearskysolarradiation = d_clearskysolarradiation + (self.sequences.logs.loggedclearskysolarradiation[idx])
                d_globalradiation = d_globalradiation + (self.sequences.logs.loggedglobalradiation[idx])
        self.sequences.fluxes.netlongwaveradiation = (            4.903e-9            / 24.0            / 60.0            / 60.0            * self.parameters.derived.seconds            * (self.sequences.inputs.airtemperature + 273.16) ** 4            * (0.34 - 0.14 * self.sequences.fluxes.actualvapourpressure ** 0.5)            * (1.35 * d_globalradiation / d_clearskysolarradiation - 0.35)        )
    cpdef inline void calc_netradiation(self)  nogil:
        self.sequences.fluxes.netradiation = self.sequences.fluxes.netshortwaveradiation - self.sequences.fluxes.netlongwaveradiation
    cpdef inline void calc_soilheatflux(self)  nogil:
        if self.parameters.derived.seconds < 60.0 * 60.0 * 24.0:
            if self.sequences.fluxes.netradiation >= 0.0:
                self.sequences.fluxes.soilheatflux = 0.1 * self.sequences.fluxes.netradiation
            else:
                self.sequences.fluxes.soilheatflux = 0.5 * self.sequences.fluxes.netradiation
        else:
            self.sequences.fluxes.soilheatflux = 0.0
    cpdef inline void calc_psychrometricconstant(self)  nogil:
        self.sequences.fluxes.psychrometricconstant = 6.65e-4 * self.sequences.inputs.atmosphericpressure
    cpdef inline void calc_referenceevapotranspiration(self)  nogil:
        self.sequences.fluxes.referenceevapotranspiration = (            0.408            * self.sequences.fluxes.saturationvapourpressureslope            * (self.sequences.fluxes.netradiation - self.sequences.fluxes.soilheatflux)            + self.sequences.fluxes.psychrometricconstant            * (37.5 / 60.0 / 60.0 * self.parameters.derived.seconds)            / (self.sequences.inputs.airtemperature + 273.0)            * self.sequences.fluxes.adjustedwindspeed            * (self.sequences.fluxes.saturationvapourpressure - self.sequences.fluxes.actualvapourpressure)        ) / (            self.sequences.fluxes.saturationvapourpressureslope            + self.sequences.fluxes.psychrometricconstant * (1.0 + 0.34 * self.sequences.fluxes.adjustedwindspeed)        )
