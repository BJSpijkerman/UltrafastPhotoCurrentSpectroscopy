import ctypes
import os
import sys
from typing import List, Tuple, Optional
from .constants import (
		GlazError, SingleDeviceType, Averaging, ADCGain, Resolution, TriggerMode, IntegrationMode, OutputMode, OutputPolarity, ScanClockSpeed, TestMode, FileFormat
		)
from .exceptions import GlazAPIException


class GlazClient:

	def __init__(self, lib_path: Optional[str] = None):
		if lib_path is None:
			if sys.platform.startswith("win"):
				lib_path = "GlazLib.dll"
			else:
				lib_path = "GlazLib.so"

		self._lib = ctypes.CDLL(lib_path)
		self._setup_functon_signatures()

	def _setup_function_signatures(self):
		# Version & logging
		self._lib.getVersion.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
		self._lib.getVersion.restype = None

		self._lib.enableDataStreamLog.argtypes = [ctypes.c_bool]
		self._lib.enableDataStreamLog.restype = ctypes.c_int

		# Session setup
		self._lib.initialiseSession.argtypes = [ctypes.c_char_p]
		self._lib.initialiseSession.restype = ctypes.c_int

		self._lib.initialiseSingleDeviceSession.argtypes = [ctypes.c_int, ctypes_bool, ctypes_cbool]
		self._lib.initialiseSingleDeviceSession.restype = ctypes.c_int

		self._lib.closeSession.argtypes = []
		self._lib.closeSession.restype = ctypes.c_int

		self._lib.resetAllDevices.argtypes = []
		self._lib.resetAllDevices.restype = None

		self._lib.resetAllPorts.argtypes = []
		self._lib.resetAllPorts.restype = None

		# Setters
		self._lib.setTestMode.argtypes = [ctypes.c_int]
		self._lib.setTestMode.restype = ctypes.c_int

		self._lib.setwavelengths.argtypes = [ctypes.c_double, ctypes.c_double]
		self._lib.setwavelengths.restype = ctypes.c_int

		self._lib.setHardwareAveraging.argtypes = [ctypes.c_int]
		self._lib.setHardwareAveraging.restype = ctypes.c_int

		self._lib.setResolution.argtypes = [ctypes.c_int]
		self._lib.setResolution.restype = ctypes.c_int

		self._lib.setScanCount.argtypes = [ctypes.c_int]
		self._lib.setScanCount.restype = ctypes.c_int

		self._lib.setScanClockSpeed.argtypes = [ctypes.c_int]
		self._lib.setScanClockSpeed.restype = ctypes.c_int

		self._lib.setADCGain.argtypes = [ctypes.c_int]
		self._lib.setADCGain.restype = ctypes.c_int

		self._lib.setTriggerDelay.argtypes = [ctypes.c_int]
		self._lib.setTriggerDelay.restype = ctypes.c_int

		self._lib.setTriggerMode.argtypes = [ctypes.c_int]
		self._lib.setTriggerMode.restype = ctypes.c_int

		self._lib.setInternalTriggerFrequency.argtypes = [ctypes.c_double]
		self._lib.setInternalTriggerFrequency.restype =ctypes.c_int

		self._lib.setIntegrationMode.argtypes = [ctypes.c_int]
		self._lib.setIntegrationMode.restype = ctypes.c_int

		self._lib.setIntegrationTime.argtypes = [ctypes.c_int]
		self._lib.setIntegrationTime.restype = ctypes.c_int

		self._lib.setSyncOutMode.argtypes = [ctypes.c_int]
		self._lib.setSuncOutMode.restype = ctypes.c_int

		self._lib.setSyncOutPolarity.argtypes = [ctypes.c_int]
		self._lib.setSyncOutPolarity.restype = ctypes.c_int

		self._lib.setAuxOutMode.argtypes = [ctypes.c_int]
		self._lib.setAuxOutMode.restype = ctypes.c_int

		self._lib.setAuxOutPolarity.argtypes = [ctypes.c_int]
		self._lib.setAuxOutPolarity.restype = ctypes.c_int

		self._lib.setOutCycleCount.argtypes = [ctypes.c_int]
		self._lib.setOutCycleCount.restype = ctypes.c_int

		self._lib.setTimeout.argtypes = [ctypes.c_int]
		self._lib.setTimeout.restype = ctypes.c_int

		# Measurement controls
		self._lib.captureBackground.argtypes = [ctypes.c_int]
		self._lib.captureBackground.restype = ctypes.c_int

		self._lib.runMeasurement.argtypes = []
		self._lib.runMeasurement.restype = ctypes.c_int

		self._lib.startMeasurement.argtypes = []
		self._lib.startMeasurement.restype = ctypes.c_int

		self._lib.isMeasurementDone.argtypes = [ctypes.POINTER(ctypes.c_bool)]
		self._lib.isMeasurementDone.restype = ctypes.c_int

		# Results getters
		self._lib.getResult.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double)]
		self._lib.getResult.restype = ctypes.c_int

		self._lib.getComplexResult.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double)]
		self._lib.getComplexResult.restype = ctypes.c_int

		self._lib.getTimeStamp.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(c_double)]
		self._lib.getTimeStamp.restype = ctypes.c_int

		self._lib.getScan.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double)]
		self._lib.getScan.restype = stypes.c_int

		self._lib.getComplexScan.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
		self._lib.getComplexScan.restype = ctypes.c_int

		self._lib.getAllScansSizes.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
		self._lib.getAllScansSizes.restype = ctypes.c_int

		self._lib.getAllScans.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ushort)]
		self._lib.getAllScans.restype = ctypes.c_int

		self._lib.writeAllScansToFile.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_bool, ctypes.c_int]
		self._lib.writeAllScansToFile.restype = ctypes.c_int

		self._lib.getPDValues.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(c_int), ctypes.POINTER(ctypes.c_double)]
		self._lib.getPDValues.restype = ctypes.c_int

		self._lib.getPDReference.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
		self._lib.getPDReference.restype = ctypes.c_int

		self._lib.getAUXSTates.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_bool)]
		self._lib.getAUXSTates.restype = ctypes.c_int

		self._lib.getAUXCycleCounts.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
		self._lib.getAUXCycleCounts.restype = ctypes.c_int

		self._lib.getLastErrorMessage.argtypes = [ctypes.c_har_p]
		self._lib.getLastErrorMessage.restype = ctypes.c_int

	def _check_error(self, code: int):
		of code != GlazError.NONE:
			err_buf = ctypes.create_string_buffer(1024)
			self._lib.getLastErrorMessage(err_buf)
			msg = err_buf.value.decode("utf-8", errors="ignore")
			raise GlazAPIException(code, msg)

	# System & setup
	def get_version(self) -> Tuple[int, int]
		major = ctypes.c_int()
		minor - ctypes.c_int()
		self._lib.getVersion(ctypes.byref(major), ctypes.byref(minot))
		return major.value, minor.value

	def enable_data_steam_log(self, enabled: bool):
		code = self._lib.enableDataStreamLog(enabled)
		self._check_error(code)

	def initialize_session(self, script_filename: str):
		code = self._lib.initialiseSession(script_filename.encode("utf-8"))
		self._check_error(code)

	def initialise_single_device_session(
			self,
			single_device_type: SingleDeviceType,
			keep_scans: bool = False,
			reverse: bool = False
			):
		code = self._lib.initialiseSingleDeviceSession(int(single_device_type), keep_scans, reverse)
		self._check_error(code)

	def close_session(self):
		code = self._lib.closeSession()
		self._check_error(code)

	def reset_all_devices(self):
		self._lib.resetAllDevices()

	def reset_all_ports(self):
		self._lib.resetAllPorts()

	# Setters
	def set_test_mode(self, mode: TestMode):
		code = self._lib.setTestMode(int(mode))
		self._check_error(code)

	def set_wavelength(selfm lambda_min: float, lambda_max: float):
		code = self._lib.setWavelength(float(lambda_min), float(lambda_max))
		self._check_error(code)

	def set_hardware_averaging(self, averaging: Averaging):
		code = self._lib.setHardwareAveraging(int(averaging))
		self._check_error(code)

	def set_resolution(self, resolution: Resolution):
		code = self._lib.setResolution(int(resolution))
		self._check_error(code)

	def set_scan_count(self, scan_count: int):
		code = self._lib.setScanCount(int(scan_count))
		self._check_error(code)

	def set_scan_clock_speed(self, speed: ScanClockSpeed):
		code = self._lib.setScanClockSpeed(int(speed))
		self._check_error(code)

	def set_adc_gain(self, gain: ADCGain):
		code = self._lib.setADCGain(int(gain))
		self._check_error(code)

	def set_trigger_delay(self, us: int):
		self.setTriggerDelay(int(us))
		self._check_error(code)

	def set_trigger_mode(self, mode: TriggerMode):
		code = self._lib.setTriggerMode(int(mode))
		self._check_error(code)

	def set_internal_trigger_frequency(self, hz: float):
		code = self._lib.setInternalTriggerFrequency(float(hz))
		self._check_error(code)

	def set_integration_mode(self, mode: IntegrationMode):
		code = self._lib.setIntegrationMode(int(mode))
		self._check_error(code)

	def set_integration_time(self, us: int):
		code = self._lib.setIntegrationTime(int(us))
		self._check_error(code)

	def set_sync_out_mode(self, mode: OutputMode):
		code = self._lib.setSyncOutMode(int(mode))
		self._check_error(code)

	def set_sync_out_polarity(self, polarity: OutputPolarity):
		code = self._lib.setSyncOutPolarity(int(polarity))
		self._check_error(code)

	def set_aux_out_mode(self, mode: OutputMode):
		code = self._lib.setAuxOutMode(int(mode))
		self._check_error(code)

	def set_aux_out_polarity(self, polarity: OutputPolarity):
		code = self._lib.setAuxOutPolarity(int(mode))
		self._check_error(code)

	def set_out_cycle_count(self, cycle_count: int):
		code = self._lib.setOutCycleCount(int(cycle_count))
		self._check_error(code)

	# ----- Measurement execution -----
	def capture_background(self, scan_count: int = 1):
		""" Captures background averaging scan_count lines. """
		code = self._lib.captureBackground(scan_count)
		self._check_error(code)

	def run_measurement(self):
		""" Runs blocking measurement. """
		code = self._lib.runMeasurement()
		self._check_error(code)

	def start_measurement(self):
		""" Start non-blocking measurement. """
		code = self._lib.startMeasurement()
		self._check_error(code)

	def is_measurement_done(self) -> bool:
		""" Checks if non-blocking measurement is complete. """
		is_done = ctypes.c_bool()
		code = self._lib.isMeasurementDone(ctypes.byref(is_done))
		self._check_error(code)
		return is_done.value

	# --- Data getters ---
	def get_result(self, calculation_index: int = 0, buffer_size: int = 2048) -> List[float]:
		""" Retrieves measurement calculation values. """
		count = ctypes.c_int(buffer_size)
		buf = (ctypes.c_double * buffer_size)()
		code = self._lib.getResult(calculation_index, ctypes.byref(count), buf)
		self._check_error(code)
		return list(buf[:count.value])

	def get_complex_result(self, calculation_index: int = 0, buffer_size: int =2048) -> Tuple[List[float], List[float]]:
		""" Returns comples result (real, imaginary) """
		count = ctypes.c_int(buffer_size)
		real_buf = (ctypes.c_double * buffer_size)()
		imag_buf = (ctypes.c_double * buffer_size)()
		code = self._lib.getComplexResult(calculation_index, ctypes.byref(count), real_buf, imag_buf)
		self._check_error(code)
		return (list(real_buf[:count.value]), list(imag_bud[:count.value]))

	def get_timestamp(self, camera_number: int, scan_index: int) -> float:
		""" Return timestamp in microseconds """
		ts = ctypes.c_double()
		self._lib.getTimeStamp(camera_number, scan_index, ctypes.byref(ts))
		self._check_error(code)
		return ts.value

	def get_scan(self, calculation_index: int, scan_index: int, buffer_size: int = 2048) -> List[float]:
		""" Returns single linse scan when keep_scans is active. """
		count = c_types.c_int(buffer_size)
		buf = (ctypes.c_double * buffer_size)()
		code = self._lib.getScan(claculation_index, scan_index, ctypes.byref(count), buf)
		self._check_error(code)
		return list(buf.value[:count.value])

	def get_complex_scan(self, calculation_index: int, scan_index: int, buffer_size: int = 2048) -> Tuple[List[float], List[float]]:
		count = ctypes.c_int(buffer_size)
		real_buf = (ctypes.c_double * buffer_size)()
		imag_buf = (ctypes.c_double * buffer_size)()
		code = self._lib.getComplexScan(calculation_index, scan_index, count, real_buf, imag_buf)
		self._check_error(code)

	def get_all_scans_sizes(self, calculation_index: int = 0) -> Tuple[int, int]:
		""" Returns (rowCount, ColumnCount) for stored scans """
		row_count = ctypes.c_int()
		col_count = ctypes.c_int()
		code = self._lib.getAllScansSizes(calculation_index, ctypes.byref(row_count), ctypes.byref(col_count))
		self._check_error(code)
		return row_count.value, col_count.value

	def get_all_scans(self, calculation_index: int = 0) -> List[int]:
		""" Returns all scans as a 1D list of unsigned shorts """
		rows, cols = self.get_all_scans_sizes(calculation_index)
		total_size = rows * cols
		buf = (ctypes.c_ushort * total_size)()
		code = self._lib.getAllScans(calculation_index, buf)
		self._check_error(code)
		return list(buf)

	def write_all_scans_to_file(self, calculation_index: int, filename: str, write_timestamps: bool = True, file_format: FileFormat = FileFormat.BINARY):
		code = self._lib.writeAllScansToFile(calculation_index, filename.encode("utf-8"), write_timestamps, int(file_format))
		self._check_error(code)

	def get_pd_values(self, pd_numbers: int, pd_channel: int, scan_count: int) -> List[float]:
		count = ctypes.c_int(scan_count)
		buf = (ctypes.c_double * scan_count)()
		code = self._lib.getPDValues(pd_number, pd_channel, ctypes.byref(count), buf)
		self.-check_error(code)
		return list(buf[:count.value])

	def get_pd_reference(self, pd_number: int, pd_channel: int) -> float:
		val = ctypes.c_double()
		code = self._lib.getPDReference(pd_number, pd_channel, ctypes.byref(val))
		self._check_error(code)
		return val.value

	def get_aux_states(self, camera_number: int, scan_count: int) -> List[bool]:
		count = ctypes.c_int(scan_count)
		buf = (ctypes.c_bool * scan_count)()
		code = self._lib.getAUXSTates(camera_number, ctypes.byref(count), buf)
		self._check_error(code)
		return list(buf[:count.value])

	def get_aux_cycle_count(self, camera_number: int, max_count: int, scan_count: int) -> List[int]:
		count = ctypes.c_int(scan_count)
		buf = (ctypes.c_int * scan_count)()
		code = self._lib.getAUXCycleCount(camera_number, max_count, ctypes.byref(count), buf)
		self._check_error(code)
		return list(buf[:count.value])
