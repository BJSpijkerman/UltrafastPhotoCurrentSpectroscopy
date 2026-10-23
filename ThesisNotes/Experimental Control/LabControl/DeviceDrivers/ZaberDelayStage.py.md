The _ZaberDelayStage_ module provides a synchronous high-level Python wrapper for controlling __Zaber optical delay sages__ via the official _zaber-motion_ SDK. It handles physical motorized translation stages and translates physical axis displacement ($\text{mm}$) into optical delay time ($\text{ps}$) based on optical pass configuration.

# Overview and Key Capabilities
- <b>SDK Integration</b>: Utilizes _zaber_motion.ascii.Connection_ to detect and interface with Zaber ASCII-protocol devices.
- <b>Physical-to-Optical Conversion</b>: Converts physical displacement ($\text{mm}$) to optical delay ($\text{ps}$) using the speed of light ($c\approx2.99\cdot10^8\,\text{m}/\text{s}$) and configurable optical passes (e.g., retroreflector 2-pass systems).
- <b>Context Manager Support</b>: Implements _\_\_enter\_\__ and _\_\_exit\_\__ for clean connection lifecycle management using standard _with_ blocks.
- <b>Dual Motion Interfaces</b>: Exposes movement commands both in physical distance ($\text{mm}$) and optical time delay ($\text{ps}$).

# Physics Equations
The conversion between optical delay $\Delta t$ (in picoseconds) and physical stage displacement $\Delta d$ (in millimeters) is governed by:
$$
\Delta t = \frac{\Delta d\cdot10^{-3}N}{c}\cdot10^{12}
$$
$$
\Delta d = \frac{\Delta t\cdot10^{-12}c}{N}10^3
$$
where:
- $c=2.99\,\text{m}/\text{s}$ (speed of light)
- $N$ number of optical passes through the stage (default: _passes = 2_ for a standard retroreflector setup).

# Class API Reference
## ZaberDelayStage
```
class ZaberDelayStage(port_name: str, 
                      device_index: int = 0, 
                      axis_number: int = 1, 
                      passes: int = 2, 
                      log_path: str = ...)
```


| Parameter    | Type | Default  | Description                                                                                   |
| ------------ | ---- | -------- | --------------------------------------------------------------------------------------------- |
| port_name    | str  | Required | Serial port identifier (e.g. _/dev/ttyUSB0_ or _COM3_).                                       |
| device_index | int  | 0        | Zero-based index of the target Zaber device on the serial chain.                              |
| axis_number  | int  | 1        | One-based axis index on the target device.                                                    |
| passes       | int  | 2        | Number of optical passes through the delay line (e.g. 2 for single retroreflector pass-back). |
| log_path     | str  | Unused   | Log path parameter declared in _\_\_init\_\__.                                                |

# Methods
<b>@property axis -> Axis</b>:
Returns the connected _zaber_motion.ascii.Axis_ object. Raises _RuntimeError_ if called prior to _connect()_.

<b>connect() -> None</b>:
	Opens serial communication on _port_name_, enables Zaber device database store (_Library.enable_device_db_store()_), detects connected hardware, and assigns the target device and axis.

<b>disconnect() -> None</b>:
	Safely closes the serial connection and releases underlying _\_connection_, _\_device_, and _\_axis_ references.

<b>delay_ps_to_distance_mm(delay_ps: float) -> float</b>:
	Converts a target optical delay in picoseconds ($\text{ps}$) to equivalent physical stage travel in millimeters ($\text{mm}$).

<b>distance_mm_to_delay_ps(distance_mm: float) -> float</b>:
	Converts a physical stage displacement in millimeters ($\text{mm}$) to equivalent optical delay in picoseconds ($\text{ps}$).

<b>home(force: bool = False) -> None</b>:
	Homes the axis if it is not already homed. If _force = True_, re-homes the stage regardless of prior status.

<b>stop() -> None</b>:
	Immediately halts motion on the active axis.

<b>is_busy() -> bool</b>
	Queries wheter the stage axis is currently executing a motion command.

<b>move_absolute_mm(position_mm: float, wait_until_idle: bool = True) -> None</b>:
	Moves the stage axis to an absolute position in millimeters.

<b>move_relative_mm(distance_mm: float, wait_until_idle: bool = True) -> None</b>:
	Moves the stage axis by a relative distance in millimeters.

<b>get_position() -> float</b>:
	Queries the current absolute position of the stage axis in millimeters.

<b>move_absolute_delay_ps(delay_ps: float, wait_until_idle: bool = True) -> None</b>:
	Converts _delay_ps_ to distance in millimeters

<b>move_relatice_delay_ps(delay_ps: float, wait_until_idle: bool = True) -> None</b>:
	Converts _delay_ps_ to distance millimeters and performs a relative motion move.

<b>get_delay_ps() -> float</b>:
	Queries current position in millimeters and calculates current optical delay in picoseconds.

# Usage Example
```
from ZaberDelayStage import ZaberDelayStage

# Using Context Manager for automatic connection and cleanup
with ZaberDelayStage(port_name="/dev/ttyUSB2", device_index=0, passes=2) as stage:
    # Home stage if needed
    stage.home()

    # Move to absolute 10 ps delay position
    stage.move_absolute_delay_ps(10.0)
    print(f"Current Position: {stage.get_position():.4f} mm")
    print(f"Current Delay: {stage.get_delay_ps():.2f} ps")

    # Step forward by 2.5 ps
    stage.move_relative_ps(2.5)
```