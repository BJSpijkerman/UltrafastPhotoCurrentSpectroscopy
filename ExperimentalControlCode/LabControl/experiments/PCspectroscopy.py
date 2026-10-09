from LabControl.devices.DeviceFactory import DeviceFactory
from LabControl.helpers.timeTimeConversion import DelayTimeHelper
from LabControl.helpers.hdf5Helper import HDF5Helper
from types import SimpleNamespace, Any


class PCspectroscopy:

	def __init__(self, hdf5_path: str):
		# Get time
		self.HDF5 = HDF5Helper
		self.HDF5.connect_to_file(hdf5_path)

		# Create good file name on tree
		self.log_path...
		self.file_path...

		# Set metadata

		# Declare helpers
		self.delay_timer: DelayTimeHelper
		self.device_factory = DeviceFactory

	def connectSR830(self, port: str):
		self.device_factory.createSR830(port)

	def connectPicoStage(self, port: str):
		self.device_factory.createPicoStage(port, self.log_path: str)

	def connectZaberStage(self, port: str):
		self.device_factory.createZaberStage(port, self.log_path)

	def setTimeZero(self, time_zero_pos):
		self.delay_timer(time_zero_pos)

	def addDelaySteps(self, start: float, stop: float, step: float):
		self.delay_timer.add_steps(start, stop, step)


	def startMeasurement():




	def __del__(
