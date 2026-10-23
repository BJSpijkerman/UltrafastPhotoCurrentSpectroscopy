import math
from typing import Optional
from zaber_motion import Library, Units
from zaber_motion.ascii import Connection, Device, Axis


SPEED_OF_LIGHT = 299_792_458.0


class ZaberDelayStage:

	def __init__(self, port_name: str,
			  device_index: int=0,
			  axis_number: int=1,
			  passes: int=2,
				):

		self.port_name = port_name
		self.device_index = device_index
		self.axis_number = axis_number
		self.passes = passes

		self._connection: Optional[Connection] = None
		self._device: Optional[Device] = None
		self._axis: Optional[Axis] = None

		Library.enable_device_db_store()

	def connect(self) -> None:
		if self._connection is None:
			self._connection = Connection.open_serial_port(self.port_name)
			devices = self._connection.detect_devices()

			if not devices or len(devices) <= self.device_index:
				self.disconnect()
				raise RuntimeError(
						f"No Zaber device found at index {self.device_index} on {self.port_name}."
						)

			self._device = devices[self.device_index]
			self._axis = self._device.get_axis(self.axis_number)

	def disconnect(self) -> None:
		if self._connection is not None:
			self._connection.close()
			self._connection = None
			self._device = None
			self._axis = None

	def __enter__(self):
		self.connect()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.disconnect()

	@property
	def axis(self) -> Axis:
		if self._axis is None:
			raise RuntimeError("Stage is not connected. Call .connect() first.")
		return self._axis

	def delay_ps_to_distance_mm(self, delay_ps: float) -> float:
		delay_seconds = delay_ps * 1e-12
		distance_meters = (delay_seconds * SPEED_OF_LIGHT) / self.passes
		return distance_meters * 1000.0

	def distance_mm_to_delay_ps(self, distance_mm: float) -> float:
		distance_meters = distance_mm / 1000.0
		delay_seconds = (distance_meters * self.passes) / SPEED_OF_LIGHT
		return delay_seconds * 1e12

	def home(self, force: bool=False) -> None:
		if force or not self.axis.is_homed():
			self.axis.home()

	def stop(self) -> None:
		self.axis.stop()

	def is_busy(self) -> bool:
		return self.axis.is_busy()

	def move_absolute_mm(self, position_mm: float, wait_until_idle: bool=True) -> None:
		self.axis.move_absolute(position_mm, Units.LENGTH_MILLIMETRES, wait_until_idle=wait_until_idle)

	def move_relative_mm(self, distance_mm: float, wait_until_idle: bool=True) -> None:
		self.axis.move_relative(distance_mm, Units.LENGTH_MILLIMETRES, wait_until_idle=wait_until_idle)

	def get_position(self) -> float:
		return self.axis.get_position(Units.LENGTH_MILLIMETRES)

	def move_absolute_delay_ps(self, delay_ps: float, wait_until_idle: bool=True) -> None:
		target_mm = self.delay_ps_to_distance_mm(delay_ps)
		self.move_absolute_mm(target_mm, wait_until_idle=wait_until_idle)

	def move_relative_ps(self, delay_ps: float, wait_until_idle: bool=True) -> None:
		distance_mm = self.delay_ps_to_distance_mm(delay_ps)
		self.move_relative_mm(distance_mm, wait_until_idle=wait_until_idle)

	def get_delay_ps(self) -> float:
		current_mm = self.get_position()
		return self.distance_mm_to_delay_ps(current_mm)
