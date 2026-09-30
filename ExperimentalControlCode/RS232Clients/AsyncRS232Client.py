import asyncio
import sys
import serial_asyncio


class AsyncRS232Client:

	def __init__(
			self,
			port: str,
			baudrate: int = 9600,
			timeout: float = 1.0,
			**kwargs
			):
		# Initialize serial connection parameters
		self.port = port
		self.baudrate = baudrate
		self.timeout = timeout
		self.extra_kwargs = kwargs
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
			print(f"[+] Connected to {self.port} at {self.baudrate} baud.")
			return True
		except Exception as e:
			print(f"[-] Failed to open port {self.port}: {e}", file=sys.stderr)
			return False


	async def send(self, data: str, add_crlf: bool = True) -> bool:
		# Async write data to serial port
		if not self.writer:
			print("[-] Port is not connected.", file=sys.stderr)
			return False

		# Add end characters
		if add_crlf and not data.endswith("\r\n"):
			data += "\r\n"

		# Try to write to serial
		try:
			self.writer.write(data.encode("utf-8"))
			await self.writer.drain()
			print(f"[>] Sent: {repr(data)}")
			return True
		except Exception as e:
			print(f"[-] Write error: {e}", file=sys.stderr)
			return False


	async def read_line(self) -> str:
		# Read single line from buffer
		if not self.reader:
			return ""

		try:
			# Apply asyncio.timeout to prevent hanging
			async with asyncio.timeout(self.timeout):
				line = await self.reader.readline()
				return line.decode("utf-8", errors="replace").strip()
		except TimeoutError:
			print("[-] Read timed out waiting for line response.")
			return ""
		except Exception as e:
			print(f"[-] Read error: {e}", file=sys.stderr)
			return ""


	async def start_listening(self, callback):
		# Background loop for continuout streaming devices

		async def _loop():
			while self.reader:
				try:
					line = await self.reader.readline()
					if line:
						text = line.decode("utf-8", errors="ignore").strip()
						await callback(text)
				except asyncio.CanceledError:
					break
				except Exception as e:
					print(f"[-] Stream read error: {e}", file=sys.stderr)
					await asyncio.sleep(0.1)

		self._listen_task = asyncio.create_task(_loop())


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
			print(f"[+] Connection on {self.port} closed.")


""" Some usage examples """
# Request/ response example
async def main_request_response():
	client = AsyncRS232Client(port="/dev/ttyUSB0", baudrate=9600, timeout=2.0)

	if await client.connect():
		await client.send("*IDN?")
		response = await client.read_line()
		print(f"[<] Revieved: {response}")

		await client.close()



async def main_streaming():
	client - AsyncRS232Client(port="/dev/ttyUSB0", baudrate=9600, timeout=2.0)

	async def handle_stream_data(data: str):
		print(f"[STREAM EVENT] Got data: {data}")

	if await client.connect():
		await client.start_listening(handle_stream_data)

		print("[+] Doing other async work while listening...")
		await asyncio.sleep(5)

		await client.close()


if __name__ == "__main__":
	asyncio.run(main_request_response())
