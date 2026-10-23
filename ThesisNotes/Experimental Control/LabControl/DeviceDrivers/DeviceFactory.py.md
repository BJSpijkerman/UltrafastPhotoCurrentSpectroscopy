The _DeviceFactory_ module provides a centralized creation interface for instantiating and configuring lab equipment. It abstracts parameter routing, normalizes connection parameters, and returns instantiated hardware objects stored as attributes on a _types.SimpleNamespace_.

# Overview & Key Capabilities
- <b>Unified Initialization</b>: Centralizes the creation of all lab devices from a single configuration structure (e.g. loaded from YAML, JSON, or Python dictionaries).
- <b>Dot-Notation Access</b>: Packs initialized devices into a _types.SimpleNamespace_, allowing access like _devices.lockin_ and _devices.delay_stage_.
- <b>Extensible Registration</b>: Supports runtime registration of new hardware driver classes via _register_driver()_.
- <b>Decoupled Architecture</b>: Keeps experiment scripts independent of individual device constructor signatures and import dependencies.

# Constants & Class Variables
__DeviceFactory.\_DRIVER\_MAP__
A class-level dictionary mapping lowercase string aliases to their corresponding driver class references.

| String Alias            | Driver Class    | Target Instrument                                      |
| ----------------------- | --------------- | ------------------------------------------------------ |
| "sr830" / "lockin"      | SR830           | Stanford Research instruments SR830 Lock-in Amplifier. |
| "zaber" / "delay_stage" | ZaberDelayStage | Zaber Motorized Optical Delay Stage.                   |

# Class API Reference
## Device Factory
```
class DeviceFactory
```

## Class Methods
<b>register_driver(name: str, driver_cls: Type) -> None</b>:
	Registers a new hardware driver class dynamically to expand the factory's driver registry at runtime
- <b>Parameters</b>:
	- <b>name (str)</b>: String identifier/ alias for the device driver (case-insensitive).
	- <b>driver_cls (Type)</b>: Class reference for the instrument driver.

<b>create_device(device_type: str, **kwargs) -> Any</b>:
	Instantiates a single device using its registered string identifier alias.
- <b>Parameters</b>:
	- <b>device_type (str)</b>: String alias matching a key in _\_DRIVER\_MAP_ (e.g. _"sr830"_, _"zaber"_).
	- <b>**kwargs</b>: Keyword arguments passed directly to the constructor of the underlying device driver class.
- <b>Returns</b>: An instantiated hardware driver oject.
- <b>Raises</b>: _ValueError_ if _device\_type_ is not found in the registered driver map.

<b>create_devices(config: Dict[str, Dict[str, Any]]) -> SimpleNamespace</b>:
	Instantiates multiple laboratory instruments defined in a nested dictionary configuration and returns them organized inside a _types.SimpleNamespace_.
- <b>Parameters</b>:
	- <b>config (Dict[str, Dict[str, Any]])</b>: Configuration dictionary where top-level keys define the attribute names on the returned namespace, and values are parameter dicts containing  a required _"type"_ key.
- <b>Returns</b>: A _types.SimpleNamespace_ object where each attribute holds an instantiated hardware driver.
- <b>Raises</b>: _ValueError_ if any device entry in _config_ lacks a required _"type"_ field or specifies an unregistered device type.

# Configuration Schema
When passing a dictionary to _create\_devices()_, use the following structure:
```
CONFIG_SCHEMA = {
    "<attribute_name>": {
        "type": "<registered_driver_alias>",
        # Additional key-value pairs forwarded to the driver __init__
        "param_1": value_1,
        "param_2": value_2,
    }
}
```

<b>Example of configuration dict</b>
```
DEVICE_CONFIG = {
    "lockin": {
        "type": "sr830",
        "port": "/dev/ttyUSB0",
        "baudrate": 9600,
        "timeout": 2.0
    },
    "delay_stage": {
        "type": "zaber",
        "port_name": "/dev/ttyUSB1",
        "device_index": 0,
        "passes": 2
    }
}
```

# Usage Examples
__Pattern A: Multi-Device setup via _SimpleNamespace__
```
import asyncio
from LabControl.DeviceDrivers.DeviceFactory import DeviceFactory

DEVICE_CONFIG = {
    "lockin": {
        "type": "sr830",
        "port": "/dev/ttyUSB0",
        "baudrate": 9600,
        "timeout": 2.0
    },
    "delay_stage": {
        "type": "zaber",
        "port_name": "/dev/ttyUSB1",
        "device_index": 0,
        "passes": 2
    }
}

async def run_experiment():
    # Instantiate all instruments into a SimpleNamespace
    devices = DeviceFactory.create_devices(DEVICE_CONFIG)

    # Access instances using dot-notation
    devices.delay_stage.connect()
    devices.delay_stage.home()

    if await devices.lockin.connect():
        # Move stage to 5 ps delay and take a measurement
        devices.delay_stage.move_absolute_delay_ps(5.0)
        snapshot = await devices.lockin.get_snapshot()

        print(f"Delay: {devices.delay_stage.get_delay_ps():.2f} ps")
        print(f"Lock-In Magnitude (R): {snapshot['R']:.6f} V")

        await devices.lockin.disconnect()

    devices.delay_stage.disconnect()

asyncio.run(run_experiment())
```

__Pattern B: Single Device Instantiation & Custom Driver Registration__
```
from LabControl.DeviceDrivers.DeviceFactory import DeviceFactory

# Custom user-defined device class
class CustomSpectrometer:
    def __init__(self, integration_time_ms: int = 100):
        self.integration_time = integration_time_ms

# 1. Register custom driver
DeviceFactory.register_driver("spectrometer", CustomSpectrometer)

# 2. Instantiate directly via create_device
spec = DeviceFactory.create_device("spectrometer", integration_time_ms=250)
print(f"Initialized Spectrometer with {spec.integration_time} ms integration time.")
```