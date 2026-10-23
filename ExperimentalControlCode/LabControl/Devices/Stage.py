from LabControl.DeviceDrivers.DeviceFactory import DeviceFactory



class Stage:

	def __init__(self):
		self.DEVICE_CONFIG = {
				"delay_stage": {
					"type": "zaber",
					"port_name": None,
					"device_index": 0,
					"passes": 2
					}
				}

		self.devices

	def connect(self, port_name: str) -> None:
		self.devices = DeviceFactory.create_devices(self.DEVICE_CONFIG)
		self.devices.delay_stage.connect(port_name)

	def get_position(self) -> float:
		pos = self.devices.delay_stage.get_position();
		return pos

	def move(self, move: str) -> None:
		if not self.devices.delay_stage.is_busy():
			if move[0] == "+":
				target = float(move[1:])
				self.devices.delay_stage.move_relative_mm(taget)
			elif move[0] == "-":
				target = float(move[1:]) * -1
				self.devices.delay_stage.move_relative_mm(target)
			elif move[0] == "=":
				target = float(move[1:])
				self.devices.delay_stage.move_absolute_mm(target)

	def stop(self) -> None:
		self.devices.delay_stage.stop()

	def home(self) -> None:
		self.devices.delay_stage.stop()
		self.devices.delay_stage.home()

	def disconnect(self) -> None:
		self.devices.delay_stage.disconnect()
