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
        timeout: float = 1.0,
        logger_instance: Optional[DeviceLogger] = None,
        **kwargs,
    ):
        # Initialize serial connection parameters
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.extra_kwargs = kwargs

        # Default to generic DeviceLogger instance if none provided
        self.logger = logger_instance or DeviceLogger(name="RS232Client")

        self.ser: Optional[serial.Serial] = None
        self._listen_thread: Optional[threading.Thread] = None
        self._stop_listening = threading.Event()

        # Thread lock for concurrent read/write operations
        self._lock = threading.Lock()

    def connect(self) -> bool:
        """Open synchronous serial connection."""
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

        # Add end characters
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
        """Read a single line from the serial buffer up to the terminator."""
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

                decoded = line.decode("utf-8", errors="replace").strip()
                self.logger.debug("Received raw line on %s: %r", self.port, decoded)
                return decoded

            except Exception as e:
                self.logger.error("Read error on %s: %r", self.port, e)
                return ""

    def start_listening(self, callback: Callable[[str], None]) -> None:
        """Start a background thread for continuous streaming devices."""
        self._stop_listening.clear()

        def _loop():
            while not self._stop_listening.is_set() and self.ser and self.ser.is_open:
                try:
                    with self._lock:
                        line = self.ser.readline()

                    if line:
                        text = line.decode("utf-8", errors="ignore").strip()
                        self.logger.debug("Stream received on %s: %r", self.port, text)
                        callback(text)
                except Exception as e:
                    if not self._stop_listening.is_set():
                        self.logger.error("Stream read error on %s: %s", self.port, e)
                        time.sleep(0.1)

        self._listen_thread = threading.Thread(target=_loop, daemon=True)
        self._listen_thread.start()
        self.logger.info("Started listening task on %s.", self.port)

    def flush_buffer(self) -> None:
        """Clear hardware input/output buffers."""
        if self.ser and self.ser.is_open:
            with self._lock:
                try:
                    self.ser.reset_input_buffer()
                    self.ser.reset_output_buffer()
                except Exception as e:
                    self.logger.error("Flush error on %s: %s", self.port, e)

    def close(self) -> None:
        """Close background listener thread and serial connection cleanly."""
        if self._listen_thread and self._listen_thread.is_alive():
            self._stop_listening.set()
            self._listen_thread.join(timeout=2.0)

        with self._lock:
            if self.ser and self.ser.is_open:
                self.ser.close()

        self.logger.info("Connection on %s closed cleanly.", self.port)
