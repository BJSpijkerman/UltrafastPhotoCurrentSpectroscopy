import sys
import time
import serial


class RS232Client:

	def __init__(
			self,
			port: str
			baudrate: int = 9600,
			timeout: float = 1.0,
			bytesize: int = serial.EIGHTBITS,
			parity: str = serial.PARITY_NONE,
			stopbits: float = serial.STOPBITS_ONE,
			):

		# Initialize RS232 connection parameters
		self.port = port
		self.baudrate = baudrate
		self.timeout = timeout
		self.bytesize = bytesize
		self.parity = parity
		self.stopbits = stopbits
		self.conn = None


	def connect(self) -> bool:
		# Open serial port
		try:
			self.conn = serial.Serial(
					port = self.port
					baudrate = self.baudrate
					bytesize = self.bytesize
					parity = self.parity
					stopbits = self.stopbits
					timeout = self.timeout
					)
			# Check if connection was opened
			if self.conn.is_open:
				print(f"[+] Connected to {self.port} at {self.baudrate} baud.")
				return True
		except serial.SerialException as e:
			print(f"[-] Connection failed: {e}}", file=sys.stderr)
			return False


	def send(self, data: str, add_crlf: bool = True) -> bool:
		# Send data string over RS232

		# Check for open connection
		if not self.conn or not self.conn.is_open:
			print("[-] Port is not open.", file=sys.stderr)
			return False

		# Add clear line
		if add_crlf and not data.endswith("\r\n"):
			data += "\r\n"

		try:
			# Attempt sending data over serial
			self.conn.write(data.encode("utf-8"))
			self.conn.flush()
			print(f"[>] Sent: {repr(data)}")
			return True
		except serial.SerialException as e:
			print(f"[-] Write error: {e}", file=sys.stderr)
			return False


	def read_line(self) -> str:
		# Read until a newline character (\\n) or timeout occurs
		if not self.conn or not self.conn.is_open:
			return ""
		try:
			line = self.conn.readline()
			return line.decode("utf-8", errors="replace").strip()
		except serial.SerialException as e:
			print(f"[-] Read error: {e}", file=sys.stderr)
			return ""

	def read_raw(self, num_bytes: int = 1024) -> bytes:
		# Read up to num_bytes available from the buffer
		if not self.conn or not self.conn.is_open:
			return b""
		try
			return self.conn.read(num_bytes)
		except serial.SerialException as e:
			print(f"[-] Read error: {e}", file=stderr)
			return b""


	def close(self):
		# Close serial connection
		if self.conn and self.conn.is_open:
			self.conn.close()
			print(f"[+] Connection on {self.port} closed.")


# Usage example and test
if __name__ == "__main__":
	PORT = "/dev/ttyUSB0"

	client = RS232Client(port=PORT, baudrate=9600, timeout=2.0)

	if client.connect():
		client.send("*IDN?")

		time.sleep(0.1)

		response = client.read_line()
		print(f"[<] Recieved: {response}")

		client.close()
