import numpy as np
c = 0.299792458 # mm/ps

class DelayTimeHelper:

	def __init__(self, time_zero_mm: float):
		self.time_zero = time_zero_mm
		self.stage_positions = np.array([])
		self.delay_times = np.array([])
		self.time_program: list[list[float]] = []
		self.position_program: list[list[float]] = []

	def add_steps(self, start: float, stop: float, step:float) -> None:
		delay = np.arange(start, stop, step)
		self.delay_times = np.append(self.delay_times, delay[:-1])

		start_mm = self.time_zero + (start) / 2 * c
		stop_mm = selt.time_zero + (stop) / 2 * c
		step_mm = step / 2 * c
		positions = np.arange(start_mm, stop_mm, step_mm)
		self.stage_positions = np.append(self.stage_positions, positions[:-1])

		self.time_program.append([start, stop, step])
		self.position_program.append([start_mm, stop_mm, step_mm])

	def get_stage_positions(self):
		return self.stage_positions

	def get_delay_times(self):
		return self.delay_times

	def __repr__(self):
		return f"Time steps: {self.time_program}\nStage positions: {self.position_program}"
