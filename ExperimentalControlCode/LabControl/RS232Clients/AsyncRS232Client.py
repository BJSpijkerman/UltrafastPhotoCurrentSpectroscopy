import asyncio
import sys
import serial_asyncio
import logging
from pathlib import Path


# Logger for serial client
class SerialLogger:

	def __init__(
			self,
			name: str = "RS232Logger",
			log_file: str = "logger_debug.log",
			console_level: int = logging.INFO,
			file_level: int = logging.DEBUG
			):
		self.logger = logging.getLogger(name)
		self.logger.setLevel(logging.DEBUG)

		# Prevent duplicate handlers if re-initialized
		if not self.logger.handlers:
			# Console handler
			console_handler = logging.StreamHandler(sys.stdout)
			console_handler.setLevel(console_level)
			console_fmt = logging.Formatter("[%(levelname)s] %(message)s")
			console_handler.setFormatter(console_fmt)

			# File handler
			file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
			file_handler.setLevel(file_level)
			file_fmt = logging.Formatter(
					"%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
					)
			file_handler.setFormatter(file_fmt)

			# Attach handlers
			self.logger.addHandler(console_handler)
			self.logger.addHandler(file_handler)


	# Wrappers around standard logger levels
	def debug(self, msg: str, *args, **kwargs):
		self.logger.debug(msg, *args, **kwargs)

	def info(self, msg: str, *args, **kwargs):
		self.logger.info(msg, *args, **kwargs)

	def warning(self, msg: str, *args, **kwargs):
		self.logger.warning(msg, *args, **kwargs)

	def error(self, msg: str, *args, **kwargs):
		self.logger.error(msg, *args, **kwargs)


# RS232 client
class AsyncRS232Client:

	def __init__(
			self,
			port: str,
			baudrate: int = 9600,
			timeout: float = 1.0,
			logger_instance: SerialLogger | None = None,
			**kwargs
			):
		# Initialize serial connection parameters
		self.port = port
		self.baudrate = baudrate
		self.timeout = timeout
		self.extra_kwargs = kwargs

		# Default to generic SerialLogger instance if none provided
		self.logger = logger_instance or SerialLogger(name="RS232Client")

		self.reader: asyncio.StreamReader | None = None
		self.writer: asyncio.StreamWriter | None = None
		self._listen_task: asyncio.Task | None = None


	async def connect(self) -> bool:
		# Open an async serial connection
		try:
			self.reader, self.writer = (
					await serial_asyncio.open_serial_connection(
						url=self.port, baudrate=self.baudrate, **self.extra_kwargs
						)
					)
			self.logger.info("Connected to %s at %d baud.", self.port, self.baudrate)
			return True
		except Exception as e:
			self.logger.error("Failed to open port %s: %s", self.port, e)
			return False


	async def send(self, data: str, add_crlf: bool = True) -> bool:
		# Async write data to serial port
		if not self.writer:
			self.logger.error("Port %s is not connected.", self.port)
			return False

		# Add end characters
		if add_crlf and not data.endswith("\r\n"):
			data += "\r\n"

		# Try to write to serial
		try:
			self.writer.write(data.encode("utf-8"))
			await self.writer.drain()
			self.logger.debug("Sent data on %s: %r", self.port, data)
			return True
		except Exception as e:
			self.logger.error("Write error on %s: %s", self.port, e)
			return False


	async def read_line(self) -> str:
		# Read single line from buffer
		if not self.reader:
			self.logger.warning("Attempted to write on unconnected port %s.", self.port)
			return ""

		try:
			# Apply asyncio.timeout to prevent hanging
			async with asyncio.timeout(self.timeout):
				line = await self.reader.readuntil(separator=b"\r")
				decoded = line.decode("utf-8", errors="replace").strip()
				self.logger.debug("Recieved raw line on %s: %r", self.port, decoded)
				return decoded
		except TimeoutError:
			self.logger.warning("Read timed out on %s after %.1fs.", self.port, self.timeout)
			return ""
		except Exception as e:
			self.logger.error("Read error on %s: %s", self.port, e)
			return ""


	async def start_listening(self, callback):
		# Background loop for continuout streaming devices

		async def _loop():
			while self.reader:
				try:
					line = await self.reader.readline()
					if line:
						text = line.decode("utf-8", errors="ignore").strip()
						self.logger.debug("Stream recieved on %s: %r", self.port, text)
						await callback(text)
				except asyncio.CancelledError:
					break
				except Exception as e:
					self.logger.error("Stream read error on %s: %s", self.port, e)
					await asyncio.sleep(0.1)

		self._listen_task = asyncio.create_task(_loop())
		self.logger.info("Started listening task on %s.", self.port)


	async def close(self):
		# Close streams and cancel background tasks cleanly
		if self._listen_task:
			self._listen_task.cancel()
			try:
				await self._listen_task
			except asyncio.CancelledError:
				pass

		if self.writer:
			self.writer.close()
			await self.writer.wait_closed()
		
		self.logger.info("Connection on %s closed cleanly.", self.port)


""" Some usage examples """
# Request/ response example
async def main_request_response():
	client = AsyncRS232Client(port="/dev/ttyUSB0", baudrate=9600, timeout=2.0)

	if await client.connect():
		await client.send("*IDN?")
		response = await client.read_line()
		print(f"[<] Revieved: {response}")

		await client.close()


# Request/ response example with logger
async def main_request_response():
	custom_logger = SerialLogger(
			name = "RS232_device_1",
			log_file="rs232_debug.log",
			console_level=logging.INFO,
			file_level=logging.DEBUG
			)

	client = AsyncRS232Client(port="/dev/ttyUSB0", baudrate=9600, timeout=2.0, logger_instance=custom_logger)

	if await client.connect():
		await client.send("*IDN?")
		response = await client.read_line()
		print(f"[<] Revieved: {response}")

		await client.close()


async def main_streaming():
	client = AsyncRS232Client(port="/dev/ttyUSB0", baudrate=9600, timeout=20.0)

	async def handle_stream_data(data: str):
		print(f"[STREAM EVENT] Got data: {data}")

	if await client.connect():
		await client.start_listening(handle_stream_data)

		print("[+] Doing other async work while listening...")
		await asyncio.sleep(5)





if __name__ == "__main__":
	asyncio.run(main_streaming())
