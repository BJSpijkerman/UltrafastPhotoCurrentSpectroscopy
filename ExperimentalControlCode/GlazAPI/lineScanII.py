from typing import List, Tuple, Optional
from .wrapper import GlazClient
from .constants import (
		GlazError, SingleDeviceType, Averaging, ADCGain, Resolution, TriggerMode, IntegrationMode, OutputMode, OutputPolarity, ScanClockSpeed, TestMode, FileFormat
		)


class LineScanII(GlazClient):

	def __init__(self, lib_path=".linux64/GlazLib.so"):
		self.super().__init__(lib_path)

		self.initialise_single_device_session(
				single_device_type=SingleDeviceType.LINESCAN_II,
				keep_scans=True,
				reverse=False
				)

	def __delete__(self):
		self.close_session()

	def self.Acquire(self):
		self.run_measurement()
		return self.get_result(calculation_index=0)
