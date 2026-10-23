import asyncio
from typing import Dict, Tuple
from LabControl.RS232Clients.AsyncRS232Client import AsyncRS232Client


class AsyncSR830:

	OFLT_MAP = {
			0: 10e-6, 1: 30e-6, 2: 100e-6, 3: 300e-6,
			4: 1e-3, 5: 3e-3, 6: 10e-3, 7: 30e-3,
			8: 100e-3, 9: 300e-3, 10: 1.0, 11: 3.0,
			12: 10.0, 13: 30.0, 14: 100.0, 15: 300.0,
			16: 1000.0, 17: 3000.0, 18: 10000.0, 19: 30000.0
			}


	def __init__(self, port: str, baudrate: int=9600, timeout: float=2.0):
		self.client = AsyncRS232Client(port=port, baudrate=baudrate, timeout=timeout)


	async def _send_cmd(self, command: str) -> bool:
		return await self.client.send(f"{command.strip()}\r", add_crlf=False)

	async def _query(self, command: str) -> str:
		if await self._send_cmd(command):
			return await self.client.read_line()
		return ""

	async def connect(self) -> None:
		if await self.client.connect():
			await self._send_cmd("OUTX 0")
			await asyncio.sleep(0.1)
			return True
		return False

	async def disconnect(self) -> None:
		await self.client.close()

	async def wait_until_ready(self, poll_interval: float=0.2, max_timeout: float=15.0) -> bool:
		start_time = asyncio.get_running_loop().time()
		while (asyncio.get_running_loop().time() - start_time) < max_timeout:
			res = await self._query("LIAS? 1")
			if res:
				status = int(res)
				if not (status & 2):
					return True
			await asyncio.sleep(poll_interval)
		return False

	async def get_id(self) -> str:
		return await self._query("*IDN?")

	async def set_ref_source(self, internal: bool=True) -> None:
		val = 1 if internal else 0
		await self._send_cmd(f"FMOD {val}")

	async def set_frequency(self, freq_hz: float) -> None:
		await self._send_cmd(f"FREQ {freq_hz}")

	async def get_frequency(self) -> float:
		res = await self._query("FREQ?")
		return float(res) if res else 0.0

	async def set_amplitude(self, volts_rms: float) -> None:
		await self._send_cmd(f"SLVL {volts_rms}")

	async def set_phase(self, phase_deg: float) -> None:
		await self._send_cmd(f"PHAS {phase_deg}")

	async def get_phase(self) -> float:
		res = await self._query("PHAS?")
		return float(res) if res else 0.0

	async def auto_phase(self) -> None:
		await self._send_cmd("APHS")
		await asyncio.sleep(0.5)
		await self.wait_until_ready()

	async def auto_gain(self) -> None:
		await self._send_cmd("AGAN")
		await asyncio.sleep(0.5)
		await self.wait_until_ready()

	async def set_gain(self, gain_setting: int) -> None:
		await self._send_cmd(f"SENS {gain_setting}")

	async def set_time_constant(self, tau_setting: int, wait_for_settle: bool=True) -> None:
		await self._send_cmd(f"OFLT {tau_setting}")
		if wait_for_settle and tau_setting in self.OFLT_MAP:
			tau = self.OFLT_MAP[tau_setting]
			settle_time = 5.0 * tau
			if settle_time > 0.01:
				await asyncio.sleep(settle_time)

	async def read_ch1(self) -> float:
		res = await self._query("OUTP? 1")
		return float(res) if res else 0.0

	async def read_ch2(self) -> float:
		res = await self._query("OUTP? 2")
		return float(res) if res else 0.0

	async def read_magnitude(self) -> float:
		res = await self._query("OUTP? 3")
		return float(res) if res else 0.0

	async def get_snapshot(self) -> Dict[str, float]:
		res = await self._query("SNAP? 1,2,3,4")
		if not res:
			return {"X": 0.0, "Y": 0.0, "R": 0.0, "Theta": 0.0}

		parts = [float(x) for x in res.split(",")]
		return {
				"X": parts[0],
				"Y": parts[1],
				"R": parts[2],
				"Theta": parts[3]
				}
