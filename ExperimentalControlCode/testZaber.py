from LabControl.DeviceDrivers.ZaberDelayStage import ZaberDelayStage
import time

if __name__ == "__main__":
	PORT = "/dev/ttyUSB1"  # Adjust for your setup (e.g., '/dev/ttyUSB0')

	# Using context manager for safe auto-disconnection
	stage = ZaberDelayStage(port_name=PORT, passes=2)
	stage.connect()
	print("Homing delay stage...")
	if stage.get_position() > 100:
		stage.move_absolute_mm(0)
	else:
		stage.move_absolute_mm(200)

	time.sleep(1)
	stage.disconnect()

"""
		# Relative move using optical units (picoseconds)
		print("Moving +200 ps...")
		stage.move_relative_ps(20.0)

		# Read back current state
		pos_mm = stage.get_position()
		delay_ps = stage.get_delay_ps()
		print(f"Current Position: {pos_mm:.4f} mm ({delay_ps:.2f} ps delay)")

		stage.move_relative_mm(10)

		# Absolute move back to origin (0 ps)
		print("Returning to 0 ps origin...")
		stage.move_absolute_delay_ps(0.0)

		stage.home()
"""
