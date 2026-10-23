The SR830Control module provides an asynchonous high-level Python driver for controlling the _Stanford Research Systems (SRS)_ SR830 Lock-in amplifier. It wraps instrument-specific SCPI/IEEE-488.2 serial commands using the [[AsyncRS232Client.py]] transport layer.

# Overview & Key Capabillities
- <b>Transport Integration</b>: Uses [[AsyncRS232Client.py]]  (from _LabControl.RS232Clients.AcynRS232Client_) to send RS-232 commands without blocking the asyncio event loop.
- <b>Automatic Output Port Setup</b>: Configures _OUTX 0_ upon connection to force responses back through the RS-232 interface.
- <b>Settling Time Automation</b>: Automatically calculated and waits fro filter settling delays based on the selected time constant (up to $5\tau$).
- <b>Status Polling</b>: Provides _wait_until_ready()_ to poll the Lock-in Status Byte (_LIAS? 1_) and deger actions until auto-phase or parameter operations complete.
- <b>Synchronous Snapshots</b>: Fetches concurrent $X$, $Y$, $R$, and $\theta$ readings using the hardware snapshot command (_SNAP?_).

# Constants & Class Variables

__SR830.OFLT_MAP__
A class-level dictionary mapping time constant index codes $0-19$ to their physical duration in seconds

| Index | Time Constant ($\tau$) | Index | Time Constant ($\tau$) |
| ----- | ---------------------- | ----- | ---------------------- |
| $0$   | $10\,\mu\text{s}$      | $10$  | $1\,\text{s}$          |
| $1$   | $30\,\mu\text{s}$      | $11$  | $3\,\text{s}$          |
| $2$   | $100\,\mu\text{s}$     | $12$  | $10\,\text{s}$         |
| $3$   | $300\,\mu\text{s}$     | $13$  | $30\,\text{s}$         |
| $4$   | $1\,\text{ms}$         | $14$  | $100\,\text{s}$        |
| $5$   | $3\,\text{ms}$         | $15$  | $300\,\text{s}$        |
| $6$   | $10\,\text{ms}$        | $16$  | $1\,\text{ks}$         |
| $7$   | $30\,\text{ms}$        | $17$  | $3\,\text{ks}$         |
| $8$   | $100\,\text{ms}$       | $18$  | $10\,\text{ks}$        |
| $9$   | $300\,\text{ms}$       | $19$  | $30\,\text{ks}$        |
__SR830.SENS_MAP__
A class-level dictionary mapping gain index codes $0-26$ to their physical voltage level.

| Index | Gain ($V$)                   | Index | Gain ($V$)                   |
| ----- | ---------------------------- | ----- | ---------------------------- |
| $0$   | $2\,\text{nV}/\text{fA}$     | $14$  | $100\,\mu\text{V}/\text{pV}$ |
| $1$   | $5\,\text{nV}/\text{fA}$     | $15$  | $200\,\mu\text{V}/\text{pV}$ |
| $2$   | $10\,\text{nV}/\text{fA}$    | $16$  | $500\,\mu\text{V}/\text{pV}$ |
| $3$   | $20\,\text{nV}/\text{fA}$    | $17$  | $1\,\text{mV}/\text{nA}$     |
| $4$   | $50\,\text{nV}/\text{fA}$    | $18$  | $2\,\text{mV}/\text{nA}$     |
| $5$   | $100\,\text{nV}/\text{fA}$   | $19$  | $5\,\text{mV}/\text{nA}$$    |
| $6$   | $200\,\text{nV}/\text{fA}$   | $20$  | $10\,\text{mV}/\text{nA}$    |
| $7$   | $500\,\text{nV}/\text{fA}$   | $21$  | $20\,\text{mV}/\text{nA}$    |
| $8$   | $1\,\mu\text{V}/\text{pV}$   | $22$  | $50\,\text{mV}/\text{nA}$$   |
| $9$   | $2\,\mu\text{V}/\text{pV}$   | $23$  | $100\,\text{mV}/\text{nA}$   |
| $10$  | $5\,\mu\text{V}/\text{pV}$   | $24$  | $200\,\text{mV}/\text{nA}$   |
| $11$  | $10\,\mu\text{V}/\text{pV}$$ | $25$  | $500\,\text{mV}/\text{nA}$   |
| $12$  | $20\,\mu\text{V}/\text{pV}$  | $26$  | $1\,\text{V}/\mu\text{A}$    |
| $13$  | $50\,\mu\text{V}/\text{pV}$  |       |                              |

# Class API Reference
## AsyncSR830
```
class AsyncSR830(port: str, baudrate: int = 9600, timeout: float = 2.0)
```

| Parameter | Type  | Default  | Description                                                                  |
| --------- | ----- | -------- | ---------------------------------------------------------------------------- |
| port      | str   | Required | Serial port path or COM port identifier (e.g. __/dev/ttyUSB0__ or __COM4__). |
| baudrate  | int   | 9600     | RS-232 baudrate.                                                             |
| timeout   | float | 2.0      | Read timeout threshold in seconds.                                           |
#### Internal helper methods
<b>_send_cmd(command: str) -> bool</b>:
	Appends _\r_ and transmits a command string to the client.

<b>_query(command: str) -> bool</b>:
	Transmits a query and returns the single-line string response. Returns "" if transmission or read fails.

#### Methods
<b>connect() -> bool</b>:
	Opens the serial connection and transmits _OUTX 0_ to direct the output responses to the RS-232 port rather than GPIB.
- <b>Returns</b>: _True_ if connection and initialized successfully, _False_ otherwise.

<b>disconnect() -> None</b>:
	Closes the underlying [[AsyncRS232Client.py]] connection cleanly.

<b>wait_until_ready(poll_interval: float = 0.2, max_timeout: float = 15.0) -> bool</b>:
	Polls bit $1$ of the Lock-in Status Byte (_LIAS? 1_).
- <b>Returns</b>: _True_ when parameter update flag clears or _False_ if max_timeout expires.

<b>get_id() -> str</b>:
	Queries the hardware identification string using standards IEEE-488 command _*IDN?_.
- <b>Returns</b>: Device id string.

<b>set_ref_source(internal: bool = True) -> None</b>:
	Sets reference source mode (_FMOD_).
- <b>internal = True</b> $\rightarrow$ Internal reference (_FMOD 1_).
- <b>internal = False</b> $\rightarrow$ External reference (_FMOD 0_).

<b>set_frequency(freq_hz: float) -> None</b>:
	Sets the internal reference oscillator frequency in $\text{Hz}$ (_FREQ <freq_hz>_).

<b>get_frequency() -> float</b>:
	Queries current internal reference frequency (_FREQ?_).
- <b>Returns</b>: internal reference frequency _float_.

<b>set_amplitude(volts_rms: float) -> None</b>:
	Sets reference sine output amplitude in Volts RMS (_SLVL <volts_rms>_)

<b>set_phase(phase_deg: float) -> None</b>:
	Sets reference phase shift in degrees (_PHAS <phase_deg>_).

<b>get_phase() -> float</b>:
	Queries current phase shift setting (_PHAS?_) as a _float_.
- <b>Returns</b>: Phase shift of internal reference _float_.

<b>auto_phase() -> None</b>:
	Triggers automatic phase adjustment (_APHS_), waits $0.5\,\text{s}$, then blocks until status bit clears via _wait_until_ready()_.

<b>set_gain(gain_setting: int) -> None</b>:
	Sets input sensitivity / gain index (_SENS <gain_setting>_).

<b>auto_gain() -> None</b>:
	Triggers automatic gain adjustment (_AGAN_), waits $0.5\,\text{s}$, then blocks until status bit clears via _wait_until_ready()_.

<b>set_time_constant(tau_setting: int, wait_for_settle: bool = True) -> None</b>:
	Configures low-pass filter time constant (_OFLT <tau_setting>_). if _wait_for_settle=True_, delays execuution for $5\times\tau$ seconds to allow filter sabilization.

<b>read_ch1() -> float</b>:
	Queries present Channel 1 value ($X$) (_OUTP? 1_).
- <b>Returns</b>: $X$ _float_.

<b>read_ch2() -> float</b>:
	Queries present Channel 2 value ($Y$) (_OUTP? 2_).
- <b>Returns</b>: $Y$ _float_.

<b>read_magnitude() -> float</b>:
	Queries present magnitude ($R$) (_OUTP? 3_).
- <b>Returns</b>: $R$ _float_.

<b>get_snapshot() -> Dict[str, float]</b>:
	Executes _SNAP> 1,2,3,4_ to capture $X$, $Y$, $R$, and $\theta$ simultaniously.
- <b>Returns</b>: Dictionary with keys "X", "Y", "R", and "Theta". Returns zeros if query fails.

# Usage example
```
import asyncio
from LabControl.DeviceDrivers.SR830Control import SR830

async def measure_lockin():
    sr830 = AsyncSR830(port="/dev/ttyUSB0", baudrate=9600)

    if await sr830.connect():
        print("Connected:", await sr830.get_id())

        # Configure Reference Generator
        await sr830.set_ref_source(internal=True)
        await sr830.set_frequency(1000.0)  # 1 kHz
        await sr830.set_amplitude(1.0)      # 1.0 V RMS

        # Configure Time Constant (Index 10 = 1.0 second, waits 5s for settling)
        await sr830.set_time_constant(10, wait_for_settle=True)

        # Retrieve simultaneous snapshot
        data = await sr830.get_snapshot()
        print(f"X: {data['X']:.6f} V, Y: {data['Y']:.6f} V")
        print(f"R: {data['R']:.6f} V, Phase: {data['Theta']:.2f} deg")

        await sr830.disconnect()

asyncio.run(measure_lockin())
```