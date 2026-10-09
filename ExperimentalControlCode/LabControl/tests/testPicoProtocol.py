import asyncio
import time
import os
from LabControl.RS232Clients.AsyncRS232Client import AsyncRS232Client, SerialLogger

PORT = "/dev/ttyACM0"

async def main():
	custom_logger = SerialLogger(name="RS232_device_1", log_file="RS232_debug_pico.log")
	client = AsyncRS232Client(port=PORT, baudrate=9600, timeout=5.0, logger_instance=custom_logger)

	if await client.connect():
		# Send test commands
		await client.send("*IDN?")
		reply = await client.read_line()
		print(f"[Pico Response] Device id: {reply}")

		time.sleep(0.05)

		await client.send("PING")
		reply = await client.read_line()
		print(f"[Pico Response] PING: {reply}")

		time.sleep(0.05)

		await client.send("LED ON")
		reply = await client.read_line()
		print(f"[Pico Response] LED: {reply}")

		time.sleep(1)

		await client.send("LED OFF")
		reply = await client.read_line()
		print(f"[Pico Response] LED: {reply}")

		time.sleep(0.05)

		await client.send("SCAN")
		reply = await client.read_line()
		print(f"[Pico Response] SCAN: {reply}")

		time.sleep(3)

		await client.close()
		print("Serial connection closed")


if __name__ == "__main__":
	asyncio.run(main())
