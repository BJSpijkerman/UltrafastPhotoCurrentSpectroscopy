import sys
import uasyncio as asyncio
from PicoRS232 import PicoRS232

from machine import Pin

""" Remove when protocol testing done """
# Test hardware setup
led = Pin("LED", Pin.OUT)
pico_serial = PicoRS232()


# --- Test command handlers ---
async def handle_idn(args: str) -> str:
	""" Handle standard SCPI query *IDN? """
	return "PICO_TEST"


async def handle_ping(args: str) -> str:
	return "PONG"


async def handle_led(args: str) -> str:
	""" Control on board LED """
	state = args.upper().strip()
	if state == "ON":
		led.value(1)
		return "ACK: LED ON"
	elif state == "OFF":
		led.value(0)
		return "ACK: LED OFF"
	return "ERR: Use 'LED ON' or 'LED OFF'"


async def handle_scan(args: str) -> str:
	""" Simulate stage move delay """
	await asyncio.sleep(2) # Simulate motor delay
	return "ACK: Stage moved to new pos"


# --- Application setup ---
async def main() -> None:
	# Register handler callbacks
	pico_serial.register_handler("*IDN?", handle_idn)
	pico_serial.register_handler("PING", handle_ping)
	pico_serial.register_handler("LED", handle_led)
	pico_serial.register_handler("SCAN", handle_scan)

	# Start async loops
	await pico_serial.start()

	# Main hardware loop
	while True:
		await asyncio.sleep(1)


if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print("Stopped.")
