import numpy as np
c = 2.99....... # mm/ps

class DelayTimeHelper:

	def __init__(time_zero_mm: float):
		self.time_zero = time_zero_mm
		self.stage_positions = np.array([])
		self.delay_times = np.array([])
		self.time_program: list[list[float]]
		self.position_program: list[list[float]]

	def add_steps(start: float, stop:float, step:float) -> None
		delay = np.arange(start, stop, step)
		self.delay_times = np.append(self.delay_times, delay)

		start_mm = (start - self.time_zero) / 2 * c
		stop_mm = (stop - self.time_zero) / 2 * c
		step_mm = step / 2 * c
		positions = np.arange(start, stop, step)
		self.stage_positions = np.append(self.stage_positions, positions[:-1])

		self.time_program.append([start, stop, step])
		self.position_program.append([start_mm, stop_mm, step_mm])

	def get_stage_positions(self):
		return self.stage_positions

	def get_delay_times(self):
		return self.delay_times

	def __repr__(self):
		return f"Time steps: {self.time_program}\nStage positions: {self.position_program}"
