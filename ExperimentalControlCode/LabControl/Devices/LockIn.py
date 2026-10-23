from LabControl.DeviceDrivers.DeviceFactory import DeviceFactory


class LockIn:

	ATTR_MAP = {
			"X": 1,
			"Y": 2,
			"R": 3,
			"Theta": 4
			}


	def __init__(self):
		self.DEVICE_CONFIG = {
				"lockin": {
					"type": "sr830",
					"port": None,
					"baudrate": 9600,
					"timeout": 2.0
					}
				}

		self.DEVICE_SETTINGS = {
				"ref_internal": True,
				"ref_freq": 500.0,
				"ref_amplitude": 1.0,
				"gain": 26,
				"tau": 4
				}


	def set_boudrate(self, baudrate: int) -> None:
		self.DEVICE_CONFIG["lockin"]["baudrate"] = baudrate

	def set_timeout(self, timeout: float) -> None:
		self.DEVICE_CONFIG["lockin"]["timeout"] = timeout

	def register(self, port_name: str) -> bool:
		self.DEVICE_CONFIG["lockin"]["port"] = port_name
		self.devices = DeviceFactory.createDevices(DEVICE_CONFIG)

		if await self.devices.lockin.connect():
			return True
		else:
			return False


	def set_reference(self, internal: bool) -> None:
		self.DEVICE_SETTINGS["ref_internal"] = internal

	def set_frequency(self, freq: float) -> None:
		self.DEVICE_SETTINGS["ref_freq"]

	def set_amplitude(self, amplitude: float) -> None:
		self.DEVICE_SETTINGS["ref_amplitude"]

	def set_gain(self, gain: int) -> None:
		self.DEVICE_SETTINGS["gain"] = gain

	def set_tau(self, tau: int) -> None:
		self.DEVICE_SETTINGS["tau"] = tau


	def Configure(self) -> None:
		self.devices.lockin.set_ref_source(self.DEVICE_SETTINGS["ref_internal"])
		if self.DEVICE_SETTINGS["ref_internal"]:
			self.devices.lockin.set_frequency(self.DEVICE_SETTINGS["ref_freq"])
			self.devices.lockin.set_amplitude(self.DEVICE_SETTINGS["ref_amplitude"])

		self.devices.lockin.set_gain(self.DEVICE_SETTINGS["gain"])
		self.devices.lockin.set_time_constant(self.DEVICE_SETTINGS["tau"])
		self.devices.auto_phase()


	def Aquire(self, attr: str) -> float:
		if attr in ATT_MAP:
			if attr == "X":
				return await self.devices.lockin.read_ch1()
			elif attr == "Y":
				return await self.devices.lockin.read_ch2()
			elif attr == "R":
				return await self.devices.lockin.read_magniture()
			else:
				raise KeyError("Chosen key not available.")

	def AquireSnap(self) -> float:
		return await self.devices.lockin.get_snapshot()

	def disconnect(self) -> None:
		await self.devices.lockin.disconnect()
