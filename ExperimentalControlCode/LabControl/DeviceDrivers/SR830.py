import time
from typing import Dict
from LabControl.RS232Clients.RS232Client import RS232Client


class SR830: 

	OFLT_MAP = {
			0: 10e-6, 1: 30e-6, 2: 100e-6, 3: 300e-6,
			4: 1e-3, 5: 3e-3, 6: 10e-3, 7: 30e-3,
			8: 100e-3, 9: 300e-3, 10: 1.0, 11: 3.0,
			12: 10.0, 13: 30.0, 14: 100.0, 15: 300.0,
			16: 1000.0, 17: 3000.0, 18: 10000.0, 19: 30000.0
			}

	def __init__(self, port: str, baudrate: int = 9600, timeout: float = 2.0):
		self.client = self.RS232Client(port=port, baudrate=baudrate, timeout=timeout)

	def _send_cmd(self, command: str) -> bool:
		return self.client.send(f"{command.strip()}\r", add_crlf=False)

	def _query(self, command: str) -> str:
		if self._send_cmd(command):
			return self.client.read_line()
		return ""

	def connect(self) -> bool:
		if self.client.connect():
			self._send_cmd("OUTX 0")
			time.sleep(0.1)
			return True
		return False

	def disconnect(self) -> bool:
		self.client.close()

	def wait_until_ready(
			self, poll_interval: float = 0.2, max_timeout: float = 15.0
			) -> bool:
		start_time = time.time()
		while (time.time() - start_time) < max_timeout:
			res = self._query("LIAS? 1")
			if res:
				try:
					status = int(res)
					if not (status & 2):
						return True
				except ValueError:
					pass
			time.sleep(poll_interval)
		return False

	def get_id(self) -> str:
		return self._query("*IDN?")

	def set_ref_source(self, internal: bool = True) -> None:
		val = 1 if internal else 0
		self._send_cmd(f"FMOD {val}")

	def set_frequency(self, freq_hz: float) -> None:
		self._send_cmd(f"FREQ {freq_hz}")

	def get_frequency(self) -> float:
		res = self._query("FREQ?")
		return float(res) if res else 0.0

	def set_amplitude(self, volts_rms: float) -> None:
		self._send_cmd(f"SLVL {volts_rms}")

	def set_phase(self, phase_deg: float) -> None:
		self._send_cmd(f"PHAS {phase_deg}")

	def get_phase(self) -> float:
		res = self._query("PHAS?")
		return float(res) if res else 0.0

	def auto_phase(self) -> None:
		self._send_cmd("APHS")
		time.sleep(0.5)
		self.wait_until_ready()

	def auto_gain(self) -> None:
		self._send_cmd("AGAN")
		time.sleep(0.5)
		self.wait_until_ready()

	def set_time_constant(
			self, tau_setting: int, wait_for_settle: bool = True
			) -> None:
		self._send_cmd(f"OFLT {tau_setting}")
		if wait_for_settle and tau_setting in self.OFLT_MAP:
			tau = self.OFLT_MAP[tau_setting]
			settle_time = 5.0 * tau
			if settle_time > 0.01:
				time.sleep(settle_time)

	def read_ch1(self) -> float:
		res = self._query("OUTP? 1")
		return float(res) if res else 0.0

	def read_ch2(self) -> float:
		res = self._query("OUTP? 2")
		return float(res) if res else 0.0

	def read_magnitude(self) -> float:
		res = self._query("OUTP? 3")
		return float(res) if res else 0.0

	def get_snapshot(self) -> Dict[str, float]:
		res = self._query("SNAP? 1,2,3,4")
		if not res:
			return {"X": 0.0, "Y": 0.0, "R": 0.0, "Theta": 0.0}

		try:
			parts = [float(x) for x in res.split(",")]
			return {
					"X": parts[0],
					"Y": parts[1],
					"R": parts[2],
					"Theta": parts[3]
					}
		except (ValueError, IndexError):
			return {"X": 0.0, "Y": 0.0, "R": 0.0, "Theta": 0.0}
