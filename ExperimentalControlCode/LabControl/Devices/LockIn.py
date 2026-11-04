from typing import Any, Dict
from LabControl.DeviceDrivers.DeviceFactory import DeviceFactory


class LockIn:

    ATTR_MAP = {
        "X": 1,
        "Y": 2,
        "R": 3,
        "Theta": 4,
    }

    def __init__(self):
        self.devices: Any = None

        self.DEVICE_CONFIG: Dict[str, Dict[str, Any]] = {
            "lockin": {
                "type": "sr830",
                "port": None,
                "baudrate": 9600,
                "timeout": 2.0,
            }
        }

        self.DEVICE_SETTINGS: Dict[str, Any] = {
            "ref_internal": True,
            "ref_freq": 500.0,
            "ref_amplitude": 1.0,
            "gain": 26,
            "tau": 4,
        }

    def set_baudrate(self, baudrate: int) -> None:
        """Set baud rate in device configuration."""
        self.DEVICE_CONFIG["lockin"]["baudrate"] = baudrate

    def set_timeout(self, timeout: float) -> None:
        """Set timeout in device configuration."""
        self.DEVICE_CONFIG["lockin"]["timeout"] = timeout

    def register(self, port_name: str) -> bool:
        """Register the port and connect synchronously to the lock-in device."""
        self.DEVICE_CONFIG["lockin"]["port"] = port_name
        self.devices = DeviceFactory.createDevices(self.DEVICE_CONFIG)

        if self.devices.lockin.connect():
            return True
        return False

    def set_reference(self, internal: bool) -> None:
        """Set internal vs external reference source."""
        self.DEVICE_SETTINGS["ref_internal"] = internal

    def set_frequency(self, freq: float) -> None:
        """Set reference frequency."""
        self.DEVICE_SETTINGS["ref_freq"] = freq

    def set_amplitude(self, amplitude: float) -> None:
        """Set reference amplitude."""
        self.DEVICE_SETTINGS["ref_amplitude"] = amplitude

    def set_gain(self, gain: int) -> None:
        """Set gain level."""
        self.DEVICE_SETTINGS["gain"] = gain

    def set_tau(self, tau: int) -> None:
        """Set time constant (tau)."""
        self.DEVICE_SETTINGS["tau"] = tau

    def configure(self) -> None:
        """Apply configured settings to the hardware device."""
        self.devices.lockin.set_ref_source(self.DEVICE_SETTINGS["ref_internal"])
        if self.DEVICE_SETTINGS["ref_internal"]:
            self.devices.lockin.set_frequency(self.DEVICE_SETTINGS["ref_freq"])
            self.devices.lockin.set_amplitude(self.DEVICE_SETTINGS["ref_amplitude"])

        self.devices.lockin.set_gain(self.DEVICE_SETTINGS["gain"])
        self.devices.lockin.set_time_constant(self.DEVICE_SETTINGS["tau"])
        self.devices.lockin.auto_phase()

    def acquire(self, attr: str) -> float:
        """Acquire a specific channel reading synchronously."""
        if attr in self.ATTR_MAP:
            if attr == "X":
                return self.devices.lockin.read_ch1()
            elif attr == "Y":
                return self.devices.lockin.read_ch2()
            elif attr == "R":
                return self.devices.lockin.read_magnitude()
            elif attr == "Theta":
                return self.devices.lockin.read_phase()

        raise KeyError(
            f"Chosen key '{attr}' not available. Must be one of {list(self.ATTR_MAP.keys())}"
        )

    def acquire_snap(self) -> Dict[str, float]:
        """Acquire a full snapshot reading synchronously."""
        return self.devices.lockin.get_snapshot()

    def disconnect(self) -> None:
        """Safely disconnect the lock-in device."""
        if self.devices and hasattr(self.devices, "lockin"):
            self.devices.lockin.disconnect()
