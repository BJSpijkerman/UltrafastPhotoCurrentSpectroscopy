The _DelayTimeHelper_ module provides utility functionality for planning optical pump-prove delay scans. It generates multi-region time grids in picoseconds ($\text{ps}$) and converts them into physical motor translation stage coordinates ($\text{mm}$) based on a reference time-zero position ($t_0$).

# Overview & Key Capabilities
- <b>Time-to-Position Conversion</b>: Translates target optical delay t ($\text{ps}$) into physical stage coordinates $d$ ($\text{mm}$) using the speed of light ($c\approx0.299792\,\text{mm}/\text{ps}$).
- <b>Multi-Region Scan Construction</b>: Supports building complex non-uniform time grids (e.g. fine step sizes around $t_0$, coarse step sizes for long decay times) via sequential _add\_steps()_ calls.
- <b>Program Tracking</b>: Maintains history lists (_time\_program_ and _position\_program_) recording start, stop, and step parameters across all scan segments.
# Mathematical equations
The absolute coordinate $d$ (in millimeters) corresponding to an optical delay $t$ (in picoseconds) relatice to $t_0$ is calculated as:
$$
d = d_0 + \frac{tc}{N},
$$
where:
- $d_0$ is the physical stage position in $\text{mm}$ corresponding to $0\,\text{ps}$ delay (_time\_zero\_mm_).
- $c=0.299792458\,\text{mm}/\text{ps}$ (speed of light in vacuum).
- $N$ is the number of optical passes through the translation stage (default $N=2$).

# Class API Reference
## DelayTimeHelper
```
class DelayTimeHelper(time_zero_mm: float, passes: int = 2)
```

| Parameter    | Type  | Default  | Description                                                                           |
| ------------ | ----- | -------- | ------------------------------------------------------------------------------------- |
| time_zero_mm | float | Required | Pysical stage coordinate ($\text{mm}$) corresponding to $0\,\text{ps}$ optical delay. |
| passes       | int   | 2        | Number of optical passes through the stage (e.g. 2 for retroreflector configuration). |

### Attributes

| Attribute        | Type                | Description                                                                   |
| ---------------- | ------------------- | ----------------------------------------------------------------------------- |
| stage_positions  | np.ndarray          | Concentrated array of calculated physical stage positions ($\text{mm}$).      |
| delay_times      | np.ndarray          | Concentrated array of target optical delay values ($\text{ps}$).              |
| time_program     | list\[list\[float]] | List of added time scan parameters \[\[start_ps, stop_ps, step_ps], ...].     |
| position_program | list\[list\[float]] | List of added position scan parameters \[\[start_mm, stop_mm, step_mm], ...]. |

# Methods
<b>add_steps(start_ps: float, stop_ps: float, step_ps: float) -> None</b>:
	Appends linear sequence of time steps in picoseconds to the scan program and computes corresponding physical stage positions.
- <b>Parameters</b>:
	- <b>start_ps (float)</b>: Starting optical delay in picoseconds.
	- <b>stop_ps (float)</b>: Ending optical delay in picoseconds (exclusive, using _np.arrange_ rules).
	- <b>step_ps (float)</b>: Step interval in picoseconds.

<b>get_stage_positions() -> np.ndarray</b>:
	Returns complete array of absolute stage positions in millimeters.

<b>get_delay_times() -> np.ndarray</b>:
	Returns complete array of optical delays in picoseconds.

# Usage Example
```
import numpy as np
from LabControl.Utils.DelayTimeHelper import DelayTimeHelper

# Initialize helper with time-zero located at 50.0 mm stage position
helper = DelayTimeHelper(time_zero_mm=50.0)

# Region 1: Fine step scan around zero delay (-2 ps to +5 ps in 0.1 ps steps)
helper.add_steps(start_ps=-2.0, stop_ps=5.0, step_ps=0.1)

# Region 2: Coarse step scan for longer dynamics (+5 ps to +50 ps in 2.0 ps steps)
helper.add_steps(start_ps=5.0, stop_ps=50.0, step_ps=2.0)

# Extract arrays for experiment loop
delays = helper.get_delay_times()
positions = helper.get_stage_positions()

print(f"Total scan points: {len(positions)}")
print(f"First position: {positions[0]:.4f} mm ({delays[0]} ps)")
print(f"Time Zero position: {helper.delay_ps_to_position_mm(0.0):.4f} mm (0 ps)")
print(f"Last position: {positions[-1]:.4f} mm ({delays[-1]} ps)")
```