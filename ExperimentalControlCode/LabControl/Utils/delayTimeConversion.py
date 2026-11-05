import numpy as np

c = 0.299792458  # speed of light in mm/ps


class DelayTimeHelper:

    def __init__(self, time_zero_mm: float = 0.0):
        self.time_zero_mm = time_zero_mm
        self.stage_positions = np.array([], dtype=float)
        self.delay_times = np.array([], dtype=float)
        self.time_program: list[list[float]] = []
        self.position_program: list[list[float]] = []

    def add_steps(self, start: float, stop: float, step: float) -> None:
        """Add delay trajectory steps in ps and convert to stage positions in mm.

        Parameters:
            start (float): Start time in ps
            stop (float): Stop time in ps
            step (float): Step size in ps
        """
        # 1. Generate delay times in picoseconds (use endpoint=True to include stop)
        # Using np.linspace or np.arange cleanly:
        num_points = int(np.round((stop - start) / step)) + 1
        delay = np.linspace(start, stop, num_points)

        # 2. Convert delay relative to time_zero into absolute stage position (mm)
        # Position (mm) = time_zero_mm + (delay_ps / 2) * c
        positions = self.time_zero_mm + (delay / 2.0) * c

        # 3. Check for out-of-range negative physical positions
        if np.any(positions < 0):
            min_pos = np.min(positions)
            raise ValueError(
                f"Calculated stage position {min_pos:.3f} mm is below 0 mm! "
                f"Check 'Time Zero (mm)' setting in the UI (current time_zero: {self.time_zero_mm} mm)."
            )

        # Append to existing trajectory
        self.delay_times = np.append(self.delay_times, delay)
        self.stage_positions = np.append(self.stage_positions, positions)

        self.time_program.append([start, stop, step])
        self.position_program.append([positions[0], positions[-1], step / 2.0 * c])

    def get_stage_positions(self) -> np.ndarray:
        return self.stage_positions

    def get_delay_times(self) -> np.ndarray:
        return self.delay_times

    def clear(self) -> None:
        """Clear queued trajectory steps."""
        self.stage_positions = np.array([], dtype=float)
        self.delay_times = np.array([], dtype=float)
        self.time_program.clear()
        self.position_program.clear()

    def __repr__(self):
        return f"Time steps: {self.time_program}\nStage positions: {self.position_program}"
