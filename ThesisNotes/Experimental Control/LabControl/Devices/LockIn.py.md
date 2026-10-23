The __lockIn__ module provides a high-level asynchronous wrapper class that encapsulates lock-in configuration parameters, registers an [[AsyncSR830.py]] instrument via [[DeviceFactory.py]] and exposes simplified measurement acquisition routines

# Overview & Key Capabilities
- __Factory-Driven Instantiation__: Wraps _DeviceFactory.create_devices()_ to configure and build the lock-in device under the hood.
- __Pre-Connection Confugutation__: Allows staging hardware parameters (baudrate, timeout, gain, time constant, reference frequency) before establishing a serial connection.
- __Asynchronous execution__: Natice _async/await_ interface for hardware configuration, automatic phase adjustment and data reading.
- __Unified Measurement API__: Provides single-channel acquisition (_Acquire()_) and multichannel hardware snapshot acquisition (_AcquireSnap()_).
# Class API Reference
```
class LockIn()
```


| Attribute       | Type                        | Description                                                                    |
| --------------- | --------------------------- | ------------------------------------------------------------------------------ |
| DEVICE_CONFIG   | Dict\[str, Dict\[str, Any]] | Configuration dictionary passed to _DeviceFactory_                             |
| DEVICE_SETTINGS | Dict\[str, Any]             | Dictionary storing instrument parameters (frequency, amplitude, gain, $\tau$). |
| devices         | SimpleNamespace \| None     | Namespace returned by _DeviceFactory_ containing the lockin driver instance    |

# Method reference
<b>set_baudrate(baudrate: int) -> None</b>:
	Sets the serial communication baud rate in _DEVICE_CONFIG_ (default: $9600$).

<b>set_timeout(timeout: float) -> None</b>:
	Sets the serial read timeout in seconds in _DEVICE_CONFIG_ (default $2.0$).

<b>register(port_name: str) -> bool</b>:
	Assings _port_name_ to _DEVICE_CONFIG_,  calls _DeviceFactory.create_devices()_, and connects to the SR830 lock-in amplifier.
- __Returns__: _True_ if connection succeeds, false otherwise

__set_reference(internal: bool) -> None__:
	Sets reference mode in _DEVICE_SETTINGS_. True for internal oscillator, False for external reference.

__set_frequency(freq: float) -> None__:
	Sets internal reference oscillator frequency in Hz in _DEVICE_SETTINGS_.

__set_amplitude(amplitude: float) -> None__:
	Sets internal reference sine output amplitude in Volts RMS in _DEVICE_SETTINGS_.

__set_gain(gain: int) -> None__:
	Sets input sensitivity index (0 to 26) in _DEVICE_SETTINGS_.

__set_tau(tau: int) -> None__:
	Sets low-pass filter time constant index (0 to 19) in _DEVICE_SETTINGS_.

__configure() -> None__:
	Sends stashed _DEVICE_SETTINGS_ to the hardware over serial and executes auto-phase adjustment (auto_gain()).

__acquire(attr: str) -> float__:
	Queries a single measurement parameter from the lock-in.
- __Parameters__: attr — string identifier ("X", "Y", "R", or "Theta").
- __Returns__: Float value representing the measurement.

__acquire_snap() -> Dict\[str, float]__:
	Triggers a hardware snapshot (SNAP? 1,2,3,4) and returns a dictionary with keys "X", "Y", "R", and "Theta".

__disconnect() -> None__:
	Safely closes the underlying serial connection to the lock-in amplifier.

# Usage example
```
import asyncio
from LabControl.Wrappers.LockIn import LockIn

async def run_lockin_measurement():
    # Instantiate wrapper
    lockin = LockIn()

    # Configure connection and settings
    lockin.set_baudrate(9600)
    lockin.set_reference(internal=True)
    lockin.set_frequency(1000.0)    # 1 kHz reference
    lockin.set_amplitude(1.0)       # 1 V RMS sine out
    lockin.set_gain(22)             # Sensitivity setting
    lockin.set_tau(10)              # 1 second time constant

    # Register serial port and connect
    if await lockin.register(port_name="/dev/ttyUSB0"):
        print("Connected to SR830 successfully.")

        # Push parameters and auto-phase
        await lockin.configure()

        # Acquire single channel value
        r_val = await lockin.acquire("R")
        print(f"Magnitude R: {r_val:.6f} V")

        # Acquire complete snapshot
        snap = await lockin.acquire_snap()
        print(f"Full Snapshot: X={snap['X']:.6f} V, Y={snap['Y']:.6f} V, Phase={snap['Theta']:.2f} deg")

        await lockin.disconnect()

asyncio.run(run_lockin_measurement())
```