import time
from typing import Any, Callable, Dict, Optional
from LabControl.DeviceDrivers.DeviceFactory import DeviceFactory
from LabControl.Utils.delayTimeConversion import DelayTimeHelper
from LabControl.Utils.hdf5Helper import HDF5Helper


class PCspectroscopy:

    def __init__(self, hdf5_path: str):
        self.HDF5 = HDF5Helper(hdf5_path)
        self.HDF5.add_group("Currents")
        self.HDF5.add_group("Stage")

        self.delay_timer: Optional[DelayTimeHelper] = None
        self.devices: Any = None
        self.N_cycles: int = 1

        self.DEVICE_CONFIG: Dict[str, Dict[str, Any]] = {
            "lockin": {
                "type": "sr830",
                "port": None,
                "baudrate": 9600,
                "timeout": 20.0,
            },
            "delay_stage": {
                "type": "zaber",
                "port_name": None,
                "device_index": 0,
                "passes": 2,
            },
        }

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
        self.DEVICE_CONFIG["lockin"]["port"] = lockin_port
        self.DEVICE_CONFIG["delay_stage"]["port_name"] = stage_port
        self.devices = DeviceFactory.create_devices(self.DEVICE_CONFIG)
        self.devices.lockin.connect()
        self.devices.delay_stage.connect()

    def add_delay_steps(self, start: float, stop: float, step: float) -> None:
        if self.delay_timer is None:
            time_zero = self.DEVICE_SETTINGS["stage"]["time_zero_mm"]
            self.delay_timer = DelayTimeHelper(time_zero)
        self.delay_timer.add_steps(start, stop, step)

    def set_parameters(self, parameter_dict: dict) -> None:
        if "N_cycles" in parameter_dict:
            self.N_cycles = parameter_dict["N_cycles"]

        self.HDF5.set_metadata(parameter_dict)

        if "lockin" in parameter_dict:
            self.DEVICE_SETTINGS["lockin"].update(parameter_dict["lockin"])
        if "stage" in parameter_dict:
            self.DEVICE_SETTINGS["stage"].update(parameter_dict["stage"])

        time_zero = self.DEVICE_SETTINGS["stage"]["time_zero_mm"]
        if self.delay_timer is None:
            self.delay_timer = DelayTimeHelper(time_zero)
        else:
            self.delay_timer.time_zero_mm = time_zero

        if self.devices:
            self.devices.lockin.set_ref_source(
                self.DEVICE_SETTINGS["lockin"]["internal_ref"]
            )
            self.devices.lockin.set_time_constant(
                self.DEVICE_SETTINGS["lockin"]["time_constant"]
            )
            self.devices.lockin.set_gain(
                self.DEVICE_SETTINGS["lockin"]["gain"]
            )

    def start_measurement(self, update_callback=None) -> None:
        """Run multi-cycle scan and trigger update_callback for live plotting."""
        if not self.delay_timer:
            raise RuntimeError("Delay timer not initialized. Call add_delay_steps() first.")

        stage_target_positions = self.delay_timer.get_stage_positions()
        N_pos = len(stage_target_positions)

        if N_pos == 0:
            raise RuntimeError("No delay positions generated.")

        # Calculate time constant filter settling delay (5 * tau)
        tau_idx = self.DEVICE_SETTINGS["lockin"]["time_constant"]
        tau_seconds = self.devices.lockin.OFLT_MAP.get(tau_idx, 0.1)
        settle_delay = 5.0 * tau_seconds

        total_steps = self.N_cycles * N_pos
        current_step_count = 0
        forward = True

        for cycle in range(self.N_cycles):
            target_ds = f"Cycle_{cycle}_Target"
            actual_ds = f"Cycle_{cycle}_Actual"
            x_ds = f"Cycle_{cycle}_X"
            y_ds = f"Cycle_{cycle}_Y"
            r_ds = f"Cycle_{cycle}_R"
            theta_ds = f"Cycle_{cycle}_Theta"

            self.HDF5.create_dataset("Stage", target_ds, dtype="f8")
            self.HDF5.create_dataset("Stage", actual_ds, dtype="f8")
            self.HDF5.create_dataset("Currents", x_ds, dtype="f8")
            self.HDF5.create_dataset("Currents", y_ds, dtype="f8")
            self.HDF5.create_dataset("Currents", r_ds, dtype="f8")
            self.HDF5.create_dataset("Currents", theta_ds, dtype="f8")

            for step in range(N_pos):
                idx = step if forward else (N_pos - 1 - step)
                target = stage_target_positions[idx]

                # Move stage to target position
                self.devices.delay_stage.move_absolute_mm(target)
                time.sleep(settle_delay)

                actual_pos = self.devices.delay_stage.get_position()
                result = self.devices.lockin.get_snapshot()

                # Stream to HDF5
                self.HDF5.append_data("Stage", target_ds, target)
                self.HDF5.append_data("Stage", actual_ds, actual_pos)
                self.HDF5.append_data("Currents", x_ds, result["X"])
                self.HDF5.append_data("Currents", y_ds, result["Y"])
                self.HDF5.append_data("Currents", r_ds, result["R"])
                self.HDF5.append_data("Currents", theta_ds, result["Theta"])

                # Trigger Live Graph Callback
                current_step_count += 1
                progress_pct = (current_step_count / total_steps) * 100

                if update_callback:
                    update_callback(actual_pos, result["X"], result["Y"], progress_pct)

            forward = not forward

    def close(self) -> None:
        if self.devices:
            try:
                self.devices.delay_stage.disconnect()
                self.devices.lockin.disconnect()
            except Exception as e:
                print(f"Error during disconnection: {e}")
        self.HDF5.close_file()
