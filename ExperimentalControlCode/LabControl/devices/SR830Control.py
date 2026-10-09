import asyncio
from typing import Dict, Tuple
from LabControl.RS232Clients.AsyncRS232Client import AsyncRS232Client



class SR830:

	def __init__(self, port: str, baudrate: int=9600, timeout: float=2.0):
		self.client = AsyncRS232Client(port=port, baudrate=baudrate, timeout=timeout)


	# Establish connection with SR830 and direct it to RS232
	async def connect(self) -> bool:
		# OUTX 0 forces all output queries to the RS232 port
		if await self.client.connect():
			await self.client.send("OUTX0")
			return True
		return False


	# Close connection
	async def disconnect(self):
		await self.client.close()


	# Query wrapper
	async def _query(self, command: str) -> str:
		if await self.client.send(command):
			return await self.client.read_line()
		return ""


	# --- System Commands ---

	async def get_id(self) -> str:
		return await self._query("*IDN?")


	# --- Reference & Oscillator commands ---

	async def set_ref_source(self, internal: bool=True) -> None:
		val = 1 if internal else 0
		await self.client.send(f"FMOD {val}")

	async def set_frequency(self, freq_hz: float) -> None:
		await self.client.send(f"FREQ {freq_hz}")

	async def get_frequency(self) -> float:
		res = await self._query("FREQ?")
		return float(res) if res else 0.0

	async def set_amplitude(self, volts_rms: float) -> None:
		await self.client.send(f"SLVL {volts_rms}")

	async def set_phase(self, phase_deg: float) -> None:
		await self.client.send(f"PHAS {phase_deg}")


	# --- Auto functions ---

	async def auto_gain(self) -> None:
		await self.client.send("AGAN")

	async def auto_phase(self) -> None:
		await self.client.send("APHS")


	# --- Gain & time constants ---

	async def set_gain(self, gain_setting: int) -> None:
		await self.client.send(f"SENS {gain_setting}")

	async def set_time_constant(self, tau_setting: int) -> None:
		await self.client.send(f"OFLT {tau_setting}")

	async def set_reserve(self, reserve_setting: int) -> None:
		await self.client.send(f"RMOD {reserve_setting}")

	async def set_lp_sloper(self, lp_slope_setting: int) -> None:
		await self.client.send(f"OFSL {lp_slope_setting}")


	# --- Data retrrieval ---

	async def read_ch1(self) -> float:
		res = await self._query("OUTP? 1")
		return float(res) if res else 0.0

	async def read_ch2(self) -> float:
		res = await self._query("OUTP? 2")
		return float(res) if res else 0.0

	async def read_magnitude(self) -> float:
		res = await self._query("SNAP? 3")
		return float(res) if res else 0.0

	async def read_phase(self) -> float:
		res = await self._query("OUTP? 4")
		return float(res) if res else 0.0

	async def get_snapshot(self) -> Dict[str, float]:
		res = await self._query("SNAP? 1,2,3,4")
		if not res:
			return {"X": 0.0, "Y": 0.0, "R": 0.0, "Theta": 0.0}

		parts = [float(x) for x in res.split(",")]
		return {"X": parts[0], "Y": parts[1], "R": parts[2], "Theta": parts[3]}



# Test and use example
async def main():
	lockIn = SR830(port="/dev/ttyUSB0", baudrate=9600)

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
		await asyncio.sleep(1.0)

		data = await lockIn.get_snapshot()
		print("\n--- SR830 Measurements ---")
		print(f"X Output      : {data["X"]:.6e} V")
		print(f"Y Output      : {data["Y"]:.6e} V")
		print(f"Magnitude (R) : {data["R"]:.6e} V")
		print(f"Phase (θ)     : {data["Theta"]:.2f}°")

		await lockIn.disconnect()

if __name__ == "__main__":
	asyncio.run(main())
