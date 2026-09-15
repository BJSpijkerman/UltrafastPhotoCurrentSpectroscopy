import asyncio
import os
import pty
from AsyncRS232Client import AsyncRS232Client


# Mock hardware running on the master side of virtual port
async def run_mock_hardware(master_fd: int):
	loop = asyncio.get_running_loop()
	print("[Mock Device] Listening for incomming commands...")

	buffer = ""

	def handle_read():
		nonlocal buffer
		try:
			raw_data = os.read(master_fd, 1024)
			if not raw_data:
				return
			buffer += raw_data.decode("utf-8", errors="ignore")

			while "\n" in buffer:
				line, buffer = buffer.split("\n", 1)
				incoming_str = line.strip()
				print(f"[Mock Device] Got: {incoming_str}")

				if incoming_str == "*IDN?":
					response = b"VIRTUAL_DEVICE\r\n"
				else:
					response = f"ECHO: {incoming_str}\r\n".encode("utf-8")

				os.write(master_fd, response)
		except Exception as e:
			print(f"[Mock Device Error] {e}")

	loop.add_reader(master_fd, handle_read)


# Main loop test
async def main():
	# Create connected pair of virtual serial ports
	master_fd, slave_fd = pty.openpty()
	virtual_port_name = os.ttyname(slave_fd)
	print(f"[System] Virtual serial port created at: {virtual_port_name}")

	# Start mock device in background
	mock_task = asyncio.create_task(run_mock_hardware(master_fd))

	# Connect Async RS232 client to slave end
	client = AsyncRS232Client(port=virtual_port_name, baudrate=9600)

	if await client.connect():
		# Send test commands
		await client.send("*IDN?")
		reply = await client.read_line()
		print(f"[Client Test] Recieved response: '{reply}'")

		await client.send("TEST_PAYLOAD")
		reply = await client.read_line()
		print(f"[Client Test] Recieved response: '{reply}'")

		await client.close()

	loop = asyncio.get_running_loop()
	loop.remove_reader(master_fd)
	os.close(master_fd)
	os.close(slave_fd)


if __name__ == "__main__":
	asyncio.run(main())
