import asyncio
from RS232Clients.AsyncRS232Client import AsyncRS232Client, SerialLogger


async def run_stage_test():
	logger = SerialLogger(
			name="StageTest", log_file="stage_test.log", console_level=20
			)

	client = AsyncRS232Client(
			port = "/dev/ttyACM0",
			baudrate=115200,
			timeout=2.0,
			logger_instance=logger
			)

	if await client.connect():
		boot_msg = await client.read_line()
		logger.info("Pico Starup Message: %s", boot_msg)

		# Query ID
		await client.send("*IDN?")
		resp = await client.read_line()
		logger.info("Device ID: %s", resp)

		# Query initial position
		await client.send("POS?")
		resp = await client.read_line()
		logger.info("Current Position: %s", resp)

		# Command stage to move to 50.0mm
		await client.send("MOVE 50.0")
		resp = await client.read_line()
		logger.info("Move Result: %s", resp)

		await client.close()


if __name__ == "__main__":
	asyncio.run(run_stage_rest())
