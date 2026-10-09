from LabControl.devices.SR830Control import SR830
from LabControl.devices.StageControl import PicoStage, ZaberStage
from types import SimpleNamespace


class DeviceFactory:

	def __init__(self):
		self.devices

	def createSR830(self, port: str, baudrate: int=9600, timeout: float=2.0):
		self.devices["LockIn"] = SR830(port, baudrate, timeout))

	def createPicoStage(self, port: str, log_path: str, baudrage: int=9600, timeout: float=2.0):
		self.devices["Stage"] = PicoStage("pico_stage", port, baudrate, log_path, stage_cfg)

	def createZaberStage(self, port: str, log_path: str):
		self.devices["Stage"] = ZaberStage(port, log_path)

	def getDevices(self):
		return SimpleNamespace(**self.devices)
