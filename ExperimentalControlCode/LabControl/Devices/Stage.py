from typing import Any, Dict
from LabControl.DeviceDrivers.DeviceFactory import DeviceFactory


class Stage:

    def __init__(self):
        self.devices: Any = None

        self.DEVICE_CONFIG: Dict[str, Dict[str, Any]] = {
            "delay_stage": {
                "type": "zaber",
                "port_name": None,
                "device_index": 0,
                "passes": 2,
            }
        }

    def connect(self, port_name: str) -> None:
        """Configure port and connect to the stage device."""
        self.DEVICE_CONFIG["delay_stage"]["port_name"] = port_name
        self.devices = DeviceFactory.create_devices(self.DEVICE_CONFIG)
        self.devices.delay_stage.connect()

    def get_position(self) -> float:
        """Return the current absolute position in mm."""
        if not self.devices or not hasattr(self.devices, "delay_stage"):
            return 0.0
        return float(self.devices.delay_stage.get_position())

    def move(self, move_cmd: str) -> None:
        """Move stage based on relative or absolute string commands.
        
        Examples: '+5.0' (move +5 mm), '-2.5' (move -2.5 mm), '=10.0' (move to 10 mm absolute).
        """
        if not self.devices or self.devices.delay_stage.is_busy():
            return

        prefix = move_cmd[0]
        value = float(move_cmd[1:])

        if prefix == "+":
            self.devices.delay_stage.move_relative_mm(value)
        elif prefix == "-":
            self.devices.delay_stage.move_relative_mm(-value)
        elif prefix == "=":
            self.devices.delay_stage.move_absolute_mm(value)

    def stop(self) -> None:
        """Emergency stop stage movement."""
        if self.devices and hasattr(self.devices, "delay_stage"):
            self.devices.delay_stage.stop()

    def home(self) -> None:
        """Home the delay stage."""
        if self.devices and hasattr(self.devices, "delay_stage"):
            self.devices.delay_stage.stop()
            self.devices.delay_stage.home()

    def disconnect(self) -> None:
        """Safely disconnect the delay stage."""
        if self.devices and hasattr(self.devices, "delay_stage"):
            self.devices.delay_stage.disconnect()
