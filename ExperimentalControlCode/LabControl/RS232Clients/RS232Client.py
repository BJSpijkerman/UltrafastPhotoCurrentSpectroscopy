import threading
import time
from typing import Callable, Optional
import serial

from LabControl.Utils.deviceLogger import DeviceLogger


class RS232Client:

    def __init__(
        self,
        port: str,
        baudrate: int = 9600,
        timeout: float = 2.0,
        logger_instance: Optional[DeviceLogger] = None,
        **kwargs,
    ):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.extra_kwargs = kwargs

        self.logger = logger_instance or DeviceLogger(name="RS232Client")

        self.ser: Optional[serial.Serial] = None
        self._listen_thread: Optional[threading.Thread] = None
        self._stop_listening = threading.Event()
        self._lock = threading.Lock()

    def connect(self) -> bool:
        """Open synchronous serial connection matching Async control line settings."""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                rtscts=False,
                dsrdtr=False,
                xonxoff=False,
                **self.extra_kwargs,
            )

            # DIFFERENCE FIX 1: Assert RTS and DTR high (identical to Async client)
            self.ser.dtr = True
            self.ser.rts = True
            time.sleep(0.1)

            self.logger.info("Connected to %s at %d baud.", self.port, self.baudrate)
            return True
        except Exception as e:
            self.logger.error("Failed to open port %s: %s", self.port, e)
            return False

    def send(self, data: str, add_crlf: bool = True) -> bool:
        """Write data to serial port."""
        if not self.ser or not self.ser.is_open:
            self.logger.error("Port %s is not connected.", self.port)
            return False

        if add_crlf and not data.endswith("\r"):
            data += "\r"

        with self._lock:
            try:
                self.ser.write(data.encode("utf-8"))
                self.ser.flush()
                self.logger.debug("Sent data on %s: %r", self.port, data)
                return True
            except Exception as e:
                self.logger.error("Write error on %s: %s", self.port, e)
                return False

    def read_line(self, terminator: bytes = b"\r") -> str:
        """Read single line up to terminator and consume any trailing newline bytes."""
        if not self.ser or not self.ser.is_open:
            self.logger.warning("Attempted to read on unconnected port %s.", self.port)
            return ""

        with self._lock:
            try:
                line = self.ser.read_until(expected=terminator)

                if not line:
                    self.logger.warning(
                        "Read timed out on %s after %.1fs", self.port, self.timeout
                    )
                    return ""

                # DIFFERENCE FIX 2: Consume leftover '\n' byte if SR830 sent '\r\n'
                if self.ser.in_waiting > 0:
                    peek_byte = self.ser.read(1)
                    if peek_byte != b"\n":
                        # If it wasn't a newline, put it back or leave buffer clean
                        pass

                decoded = line.decode("utf-8", errors="replace").strip()
                self.logger.debug("Received raw line on %s: %r", self.port, decoded)
                return decoded

            except Exception as e:
                self.logger.error("Read error on %s: %r", self.port, e)
                return ""

    def flush_buffer(self) -> None:
        """Clear input/output buffers."""
        if self.ser and self.ser.is_open:
            with self._lock:
                try:
                    self.ser.reset_input_buffer()
                    self.ser.reset_output_buffer()
                except Exception as e:
                    self.logger.error("Flush error on %s: %s", self.port, e)

    def close(self) -> None:
        if self._listen_thread and self._listen_thread.is_alive():
            self._stop_listening.set()
            self._listen_thread.join(timeout=2.0)

        with self._lock:
            if self.ser and self.ser.is_open:
                self.ser.close()

        self.logger.info("Connection on %s closed cleanly.", self.port)
