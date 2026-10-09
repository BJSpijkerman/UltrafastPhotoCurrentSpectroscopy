from LabControl.devices.SR830Control import SR830
import asyncio
import time

# Test and use example
async def main():
	lockIn = SR830(port="/dev/ttyUSB0", baudrate=19200, timeout=10.0)

	if await lockIn.connect():
		device_id = await lockIn.get_id()
		print(f"Connected Device ID: {device_id}")

		# Configure reference oscillator
		print("Setting internal reference to 1.0 kHz @ 0.5 Vrms")
		await lockIn.set_ref_source(internal=True)
		await lockIn.set_frequency(500.0)
		await lockIn.set_amplitude(1)
		await lockIn.auto_gain()
		await lockIn.auto_phase()
		await lockIn.set_time_constant(4) # 1ms

		# Allow time for filters/locks to settle
		time.sleep(1.0)


		data = await lockIn.read_magnitude()
		print(f"Magnitude: {data}")

		await lockIn.disconnect()

from LabControl.RS232Clients.AsyncRS232Client import AsyncRS232Client
async def test():
	client = AsyncRS232Client("/dev/ttyUSB0", baudrate=19200, timeout=5.0)

	if await client.connect():
		await client.send("OUTX 0\r", add_crlf=False)
		await client.send("SNAP? 1\r", add_crlf=False)
		data = await client.read_line()
		print(data)

	await client.close()

if __name__ == "__main__":
#	asyncio.run(main())
	asyncio.run(test())
