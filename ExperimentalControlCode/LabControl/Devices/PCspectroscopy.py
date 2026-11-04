from LabControl.DeviceDrivers.DeviceFactory import DeviceFactory
from LabControl.Utils.delayTimeConversion import DelayTimeHelper
from LabControl.Utils.hdf5Helper import HDF5Helper
from typing import Any, Dict, Optional


class PCspectroscopy:

    def __init__(self, hdf5_path: str):
        # Instantiate HDF5 Helper instance
        self.HDF5 = HDF5Helper(hdf5_path)
        self.HDF5.add_group("Currents")
        self.HDF5.add_group("Stage")

        # Helpers & devices placeholder
        self.delay_timer: Optional[DelayTimeHelper] = None
        self.devices: Any = None

        # Number of cycles in measurement
        self.N_cycles: int = 1

        # Device configurations
        self.DEVICE_CONFIG: Dict[str, Dict[str, Any]] = {
            "lockin": {
                "type": "sr830",
                "port": None,
                "baudrate": 9600,
                "timeout": 20.0,
            },
            "delay_stage": {
                "type": "ZaberDelayStage",
                "port_name": None,
                "device_index": 0,
                "passes": 2,
            },
        }

        # Default device settings
        self.DEVICE_SETTINGS: Dict[str, Dict[str, Any]] = {
            "lockin": {
                "internal_ref": False,
                "time_constant": 1,
                "gain": 16,
            },
            "stage": {
                "time_zero_mm": 0,
            },
        }

    def connect_devices(self, lockin_port: str, stage_port: str) -> None:
        """Configure ports and initialize physical devices."""
        self.DEVICE_CONFIG["lockin"]["port"] = lockin_port
        self.DEVICE_CONFIG["delay_stage"]["port_name"] = stage_port
        self.devices = DeviceFactory.create_devices(self.DEVICE_CONFIG)
        self.devices.lockin.connect()
        self.devices.delay_stage.connect()

    def add_delay_steps(self, start: float, stop: float, step: float) -> None:
        """Configure delay trajectory steps."""
        if self.delay_timer is None:
            time_zero = self.DEVICE_SETTINGS["stage"]["time_zero_mm"]
            self.delay_timer = DelayTimeHelper(time_zero)
        self.delay_timer.add_steps(start, stop, step)

    def set_parameters(self, parameter_dict: dict) -> None:
        """Save attributes to HDF5 root and pass parameters to devices."""
        if "N_cycles" in parameter_dict:
            self.N_cycles = parameter_dict["N_cycles"]

        # 1. Use HDF5Helper's set_metadata for root-level attributes
        self.HDF5.set_metadata(parameter_dict)

        # 2. Update local nested settings if provided
        if "lockin" in parameter_dict:
            self.DEVICE_SETTINGS["lockin"].update(parameter_dict["lockin"])
        if "stage" in parameter_dict:
            self.DEVICE_SETTINGS["stage"].update(parameter_dict["stage"])

        # 3. Apply settings to hardware and helper
        time_zero = self.DEVICE_SETTINGS["stage"]["time_zero_mm"]
        self.delay_timer = DelayTimeHelper(time_zero)

        self.devices.lockin.set_ref(self.DEVICE_SETTINGS["lockin"]["internal_ref"])
        self.devices.lockin.set_time_constant(
            self.DEVICE_SETTINGS["lockin"]["time_constant"]
        )
        self.devices.lockin.set_gain(self.DEVICE_SETTINGS["lockin"]["gain"])

    def start_measurement(self) -> None:
        """Run the multi-cycle delay measurement loop."""
        if not self.delay_timer:
            raise RuntimeError("Delay timer not initialized. Call add_delay_steps() or set_parameters() first.")

        # Prepare hardware
        self.devices.delay_stage.home()
        self.devices.lockin.auto_phase()

        stage_target_positions = self.delay_timer.get_stage_positions()
        N_pos = len(stage_target_positions)

        forward = True

        for cycle in range(self.N_cycles):
            # Define dataset names for this cycle
            target_ds = f"Cycle_{cycle}_Target"
            actual_ds = f"Cycle_{cycle}_Actual"
            x_ds = f"Cycle_{cycle}_X"
            y_ds = f"Cycle_{cycle}_Y"
            r_ds = f"Cycle_{cycle}_R"
            theta_ds = f"Cycle_{cycle}_Theta"

            # Create 1D resizable datasets via HDF5Helper
            self.HDF5.create_dataset("Stage", target_ds, dtype="f8")
            self.HDF5.create_dataset("Stage", actual_ds, dtype="f8")
            self.HDF5.create_dataset("Currents", x_ds, dtype="f8")
            self.HDF5.create_dataset("Currents", y_ds, dtype="f8")
            self.HDF5.create_dataset("Currents", r_ds, dtype="f8")
            self.HDF5.create_dataset("Currents", theta_ds, dtype="f8")

            # Perform scan across delay positions
            for step in range(N_pos):
                idx = step if forward else (N_pos - 1 - step)

                target = stage_target_positions[idx]
                self.devices.delay_stage.move_absolute_mm(target)
                actual_pos = self.devices.delay_stage.get_position()
                result = self.devices.lockin.get_snapshot()

                # Stream measurements point-by-point into HDF5 datasets
                self.HDF5.append_data("Stage", target_ds, target)
                self.HDF5.append_data("Stage", actual_ds, actual_pos)
                self.HDF5.append_data("Currents", x_ds, result["X"])
                self.HDF5.append_data("Currents", y_ds, result["Y"])
                self.HDF5.append_data("Currents", r_ds, result["R"])
                self.HDF5.append_data("Currents", theta_ds, result["Theta"])

            forward = not forward

    def close(self) -> None:
        """Safely disconnect devices and close the HDF5 file."""
        if self.devices:
            self.devices.delay_stage.disconnect()
            self.devices.lockin.disconnect()
        self.HDF5.close_file()
