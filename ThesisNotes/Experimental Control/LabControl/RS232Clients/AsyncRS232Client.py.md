caThe AsyncRS232Client module provides an asynchronous communication interface for laboratory hardware over RS-232 serial interfaces. Built on top of _asyncio_ and _pyserial-asyncio_, it handles non-blocking serial read/write operations, configurable logging, line framing, buffering and background stream listening.

# Overview & Key Capabilities
- <b>Asynchronous I/O</b>: Prevents blocking the event loop while waiting for hardware responses.
- <b>Dual Communication Modes</b>:
	- <b>Request / Response</b>: Send commands ans wait for discrete line replies (e.g. standard SCPI query _*IDN?_).
	- <b>Streaming / Continuous</b>: Built-in dual-destination logging (formatted log files and read-time stdout streams).
- <b>Graceful Resource Management</b>: Handles cleanup of background listening loops and synchronous serial writer streams.

## AsyncRS232Client
```
class AsyncRS232Client(port: str,
						baudrate: int = 9600,
						timeout: float = 1.0,
						logger_instance: DeviceLogger | None = None,
						**kwargs)
```
Asynchronous client for interacting with serial instruments over RS-232.

| Parameter       | Type                 | Default    | Description                                                                                |
| --------------- | -------------------- | ---------- | ------------------------------------------------------------------------------------------ |
| port            | str                  | _Required_ | Device path or virtual COM port name (e.g. __/dev/ttyUSB0__ or __COM3__).                  |
| baudrate        | int                  | 9600       | Baud rate for serial communication                                                         |
| timeout         | float                | 1.0        | Read timeout threshold in seconds                                                          |
| logger_instance | DeviceLogger \| None | None       | Custom __DeviceLogger__ instance. Defaults to creating a new "RS232Client" instance.       |
| **kwargs        | dict                 | {}         | Additional keyword arguments passed directly to __serial_asyncio.open_serial_connection__. |


| Attributes   | Type                         | Description                                             |
| ------------ | ---------------------------- | ------------------------------------------------------- |
| reader       | asyncio.StreamReader \| None | Stream reader for incoming serial bytes.                |
| writer       | asyncio.StreamWriter \| None | Stream writer for outgoing serial bytes.                |
| _listen_task | asyncio.Task \| None         | Background task reference fo continous stream listening |
#### Methods
<b>connect() -> bool</b>:
	Opens the asynchronous serial connection and sets RTS/DTR pins to _True_ if supported by the transport.
- <b>Returns</b>: _True_ if connection succeeded, _False_ if an exception occurred.

<b>send(data: str, add_crlf: bool = True) -> bool</b>:
	Asynchonously encodes and writes string data to the connected port.
- <b>Parameters</b>:
	- <b>data (str)</b>: The command payload to transmit.
	- <b>add_crlf (bool)</b>: if _True_, appends a carriage return (_\r_) termination character if not already present.
- <b>Returns</b>: _True_ if transmitted successfully, _False_ if disconnected or failed.

<b>read_line() -> str</b>:
	Reads characters until a carriage return (_\r_) delimiter is encountered, bounded by _self.timeout_. Also consumes a trailing linefeed (_\n_) if present within a short sub-timeout window ($0.01\,\text{s}$).
- <b>Returns</b>: Decoded UTF-8 string with surrounding whitespace/newlines stripped. Returns _""_ on timeout error.

<b>start_listening(callback: Callable[[str], Awaitable[None]]) -> None</b>:
	Spawns an asynchronous background task (_\_listent_task_) that continuously reads lines from the buffer and passes each line to an async callback function.
- <b>Parameters</b>:
	- <b>callback</b>: Coroutine taking a single string argument representing the incomming stream line.

<b>flush_buffer() -> None</b>:
	Attempts a fast read ($\text{timeout}=0.05\,\text{s}$) of up to $1024$ bytes from the stream buffer to clear unread residual bytes.

<b>close() -> None</b>:
	Cancels any active continuous listening tasks and cleanly shuts down the stream writer.

#### Usage examples
- Pattern A: Standard Request / Response (SCPI-Style)
```
import asyncio
from LabControl.RS232Clients.AsyncRS232Client import AsyncRS232Client

async def run_query():
    client = AsyncRS232Client(port="/dev/ttyUSB0", baudrate=9600, timeout=2.0)

    if await client.connect():
        # Query device identity
        if await client.send("*IDN?"):
            response = await client.read_line()
            print(f"Device Identification: {response}")
            
        await client.close()

asyncio.run(run_query())
```
- Pattern B: Continuous Streaming with Custom Logger
```
import asyncio
import logging
from LabControl.RS232Clients.AsyncRS232Client import AsyncRS232Client
frim LabControl.Utils.DeviceLogger import DeviceLogger

async def handle_telemetry(data: str):
    print(f"[TELEMETRY]: {data}")

async def run_streaming():
    logger = DeviceLogger(
        name="TemperatureSensor",
        log_file="temp_sensor.log",
        console_level=logging.INFO,
        file_level=logging.DEBUG
    )

    client = AsyncRS232Client(
        port="/dev/ttyUSB1", 
        baudrate=115200, 
        logger_instance=logger
    )

    if await client.connect():
        # Start background listener
        await client.start_listening(handle_telemetry)
        
        # Continue executing other async tasks while listening
        await asyncio.sleep(10)
        
        await client.close()

asyncio.run(run_streaming())
```