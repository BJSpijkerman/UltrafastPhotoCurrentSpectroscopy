This module help generate a [[ZaberDelayStage.py]] instance using the [[DeviceFactory.py]] and exposes a simplified user interface, capable of homing, moving and requesting positions from the stage.

# Overview & Key Capabilities
- __Factory-Driven Instantiation__: Wraps _DeviceFactory.create_devices()_ to configure and build the delay stage under the hood.
- __Pre-Connection Confugutation__: Allows staging hardware parameters before establishing a serial connection.
- __Unified Movement API__: Provides functions to easily move the stage and request its position.

```
class Stage()
```

| Attribute       | Type                        | Description                                                                    |
| --------------- | --------------------------- | ------------------------------------------------------------------------------ |
| DEVICE_CONFIG   | Dict\[str, Dict\[str, Any]] | Configuration dictionary passed to _DeviceFactory_                             |
# Method reference
__connect() -> None__:
	Connects to available Zaber stage devices.

__get\_position() -> float__:
	Requests the stage position in $\text{mm}$ from the device.
- __Returns__: Current position of the Zaber delay stage in $\text{mm}$.

__move(move: str) -> None__:
	Sends a movement command to the Zaber delay stage, where "_+_" and "_-_" cause relative movement and "=" absolute movement.

__stop() -> None__:
	Stops execution of movement.

__home() -> None__:
	Homes the stage

__disconnect() -> None__:
	Disconnects from the stage.


# Usage example
```
from LabControl.Devices.Stage import Stage

stage = Stage()
stage.connect("/dev/ttyUSB0")

# Move 10 mm in positive direction
stage.move("+10")

# Move stage to 17 mm
stage.move("=17")

# Stops all movement
stage.stop()

# Print current position of stage
print(stage.get_position())

# Disconnect stage
stage.disconnect()
```