The __RS232Client__ module provides synchronous communication for laboratory hardware over the RS232 protocol serial interfaces. Built on top of _pyserial_ and standard threading, it handles blocking serial read/write operations, configurable logging, line framing, buffering, and background thread stream listening.

# Overview & Capabilities
- __Synchronous I/O__: Provides a straightforward, thread-safe interface for serial communicaition.
- __Dual communication mode__:
	- __Request/ Response__: Send commands and wait for discrete line replies (e.g. standard SCPI query _\*IDN?_).
	- __Streaming/ Continuous__: Background thread execution for continuous device streaming.
- __Gracefull Resource Management__: Automatically handles cleanup of background listener threads and synchronous serial port handles.

# RS232Client
```
class RS232Client(
    port: str,
    baudrate: int = 9600,
    timeout: float = 1.0,
    logger_instance: DeviceLogger | None = None,
    **kwargs
)
```

| Parameter       | Type                 | Default    | Description                                                                          |
| --------------- | -------------------- | ---------- | ------------------------------------------------------------------------------------ |
| port            | str                  | _Required_ | Device path or virtual COM port name (e.g. _/dev/ttyUSB0_ or _COM3_).                |
| baudrate        | int                  | 9600       | Baudrate for serial communication.                                                   |
| timeout         | float                | 1.0        | Read timeout threshold in seconds.                                                   |
| logger_instance | DeviceLogger \| None | None       | Custon __DeviceLogger__ instance. Default to creating a new "deviceLogger" instance. |
| \*\*kwargs      | dict                 | {}         | Additional keyword arguments passed directly to _serial.Serial_.                     |
# Methods
__connect() -> bool__:
	Opens the synchronous serial connection and sets RTS/DTR pins to __True__ if supported by the transport.
- __Returns__: _True_ if connection succeeded, _False_ if an exception occurred.

__send(data: str, add_crlf: bool = True) -> bool__:
	Synchronously encodes and writes string data to the connected port.
- __Parameters__:
	- __data (str)__: The command payload to transmit.
	- __add\_crlf (bool)__: If _True_, appends a carriage return (_\r_) termination character if not already present.
- __Returns__: _True_ if transmitted successfully, _False_ if disconnected or failed.

__read\_line() -> str__:
	Reads characters until a carriage return (_\r_) delimiter is encountered, bounded by _self.timeout_. Also consumes a trailing linefeed (_\n_) if present within a short sub-timeout window ($0.01\,\text{s}$).
- __Returns__: Decoded _UTF-8_ string with surrounding whitespace/ newlines stripped. Returns _""_ on timeout or error.

__start\_listening(callback: Callable\[\[str], None])__ => None:
	Sets up a synchronous background thread (_\_listen_thread_) that continuously reads lines from the buffer and passes each line to a callback function
- __Parameters__:
	- _callback_: Function taking a single string argument representing the incoming stream line.

__flush\_buffer() -> None__:
	Clears both input and output hardware buffers and to discard residual bytes.

__close() -> None__:
	Signals any active continuous listening thread to stop. waits for thread join, and cleanly closes the serial port.

# Usage example
__Pattern A: Standard Request/ Response (SCPI-style)__
```
from LabControl.RS232Clients.RS232Client import RS232Client

def run_query():
    client = RS232Client(port="/dev/ttyUSB0", baudrate=9600, timeout=2.0)

    if client.connect():
        # Query device identity
        if client.send("*IDN?"):
            response = client.read_line()
            print(f"Device Identification: {response}")
            
        client.close()

run_query()
```

__Pattern B: Continuous Streaming with Custom Logger__:
```
import time
import logging
from LabControl.RS232Clients.RS232Client import RS232Client

def handle_telemetry(data: str):
    print(f"[TELEMETRY]: {data}")

def run_streaming():
    logger = DeviceLogger(
        name="TemperatureSensor",
        log_file="temp_sensor.log",
        console_level=logging.INFO,
        file_level=logging.DEBUG
    )

    client = RS232Client(
        port="/dev/ttyUSB1", 
        baudrate=115200, 
        logger_instance=logger
    )

    if client.connect():
        # Start background listener thread
        client.start_listening(handle_telemetry)
        
        # Continue executing other main thread tasks while listening
        time.sleep(10)
        
        client.close()

run_streaming()
```