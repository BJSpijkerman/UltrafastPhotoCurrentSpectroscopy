from LabControl.devices.DeviceFactory import DeviceFactory
from LabControl.helpers.timeTimeConversion import DelayTimeHelper
from LabControl.helpers.hdf5Helper import HDF5Helper
from types import SimpleNamespace, Any


class PCspectroscopy:

	def __init__(self, hdf5_path: str):
		# Get time
		self.HDF5 = HDF5Helper
		# Declare helpers
		self.delay_timer: DelayTimeHelper

		# MAKE FILE
		self.HDF5.connect_to_file(hdf5_path)
		self.HDF5.add_group("Currents")
		self.HDF5.add_group("Stage")

		# Number of cycles in measurement
		self.N_cycles: int
		# Setup for device config
		self.DEVICE_CONFIG = {
				"lockin": {
					"type": "sr830",
					"port": None,
					"baudrate": 9600,
					"timeout": 20.0
					},
				"delay_stage": {
					"type": "ZaberDelayStage",
					"port_name": None,
					"device_index": 0,
					"passes": 2
					}
				}

		# Default device settings
		self.DEVICE_SETTINGS = {
				"lockin": {
					"internal_ref": False,
					"time_constant": 1,
					"gain": 16
					}
				"stage": {
					"time_zero_mm": 0,
					}
				}



	def connect_devices(self, lockin_port: str, stage_port: str) -> None:
		# Configure and connect to devices
		self.DEVICE_CONFIG["lockin"]["port"] = lockin_port
		self.DEVICE_CONFIG["delay_stage"]["port_name"] = stage_port
		self.devices = DeviceFactory.create_devices(self.DEVICE_CONFIG)
		self.devices.lockin.connect()
		self.devices.delay_stage.connect()


	def add_delay_steps(self, start: float, stop: float, step: float) -> None:
		# Add delay program
		self.delay_timer.add_steps(start, stop, step)


	def set_parameters(self, parameter_dict: dict) -> None:
		# Copy parameters
		self.N_cycles = parameter_dict["N_cycles"]
		for parameter in parameter_dict.keys():
			self.HDF5.arrts[parameter] = parameter_dict[parameter]

		for setting in self.DEVICE_SETTINGS.keys():
			self.DEVICE_SETTINGS[setting] = parameter_dict[setting]

		# Configure devices
		self.delay_timer = DelayTimeHelper(self.DEVICE_SETTINGS["time_zero_mm"])
		self.devices.lockin.set_ref(self.DEVICE_SETTINGS["internal_ref"])
		self.devices.lockin.set_time_constant(self.DEVICE_SETINGS["time_constant"])
		self.devices.lockin.set_gain(self.DEVICE_SETTINGS["gain"])


	def start_measurement() -> None:
		# Prepare devices for measurement
		self.devices.delay_stage.home()
		self.devices.lockin.auto_phase()
		stage_target_positions = self.delay_timer.get_stage_positions()
		N_pos = len(stage_target_positions)

		forward = True
		# Perform acquisition and stream data
		for cycle in range(self.N_cycles):
			# Build datasets

			# NOTE: Find out how to resize datasets and give column labels
			stage_dset = self.HDF5.create_dset("Stage", f"Cycle_{cycle}", maxshape(N_pos, 2))
			current_dset = self.HDF5.create_dset("Currents", f"Cycle_{cycle}", maxshape(N_pos, 4))

			for step in range(N_step):
				if not forward:
					step = N_step - step

				target = stage_target_positions[step]
				self.devices.delay_stage.move_absolute_mm(target)
				result = self.devices.lockin.get_snapshot()

				stage_target_dset[
				for key in result.keys():
				# NOTE: Do I have to resize here?
					# Save data
					stage_dset["target_position"][i] = target
					stage_dset["actual_position"][i] = self.devices.delay_stage.get_position()
					current_dset["X"][i] = result["X"]
					current_dset["Y"][i] = result["Y"]
					current_dset["R"][i] = result["R"]
					current_dset["Theta"][i] = result["Theta"]


			forward = not forward


	def close() -> None:
		self.devices.delay_stage.disconnect()
		self.devices.lockin.disconnect()


