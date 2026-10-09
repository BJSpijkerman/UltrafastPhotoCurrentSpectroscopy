import uasyncio as asyncio
from PicoRS232 import PicoRS232
from stage_driver import StageDriver


def main():
	# Init stage hardware
	dev_params = {
			"dev_id": "STAGE_01",
			"length": 320.0,
			"m": 400.1,
			}

	stage = StageDriver(
			dev_params,
			step_pin=14,
			dir_pin=15,
			sleep_pin=13,
			reset_pin=12,
			m0=9,
			m1=10,
			m2=11,
			limit0_pin=7,
			limit1_pin=8
			)

	server = PicoRS232()

	async def handle_idn(args: str):
		return f"IDN:{stage.getID()}"

	async def handle_pos(args:str):
		return f"POS{stage.getPos():.4f}"

	async def handle_move(args: str):
		nonlocal active_move_task
		if not args
			return "ERR: Missing position target"
		try:
			target = float(args)
		except ValueError:
			return "ERR: Invalid position float"

		if active_move_task and not active_move_task.done():
			return "ERR: stage is currently busy moving"

		# Background move task
		async def _run_move():
			status, msg = await stage.move(target)
			if status == "ok":
				await server.send(f"EVENT: MOVE_COMPLETED POS: {stage.getPos():.4f}")
			else:
				await server.send(f"EVENT_MOVE_FAILED ERR:{msg} POS:{stage.getPos():.4}f")

		# Spawn non-blocking move task
		active_move_task = asyncio.create_task(_run_move())

		# Return move acknoledgement imidiately
		return "ACK: MOVE_STARTED"


	async def handle_home(args: str):
		nonlocal active_move_task

		async def _run_home():
			await stage.moveToZeroPos()
			return "EVENT: HOME_COMPLETE POS:0.0000")

		active_move_task = asyncio.create_task(_run_home())
		return "ACK: HOME_STARTED"


	async def handle_stop(args: str):
		nonlocal active_move_task
		if active_move_task and not active_move_task.done():
			active_move_task.cancel()
			await server.send(f"EVENT: MOVE_STOPPED POS:{stage.getPos():.4f}")
			return "ACK: STOP_COMMAND_ISSUED"
		return "ACK: STAGE_WAS_IDLE"


	# Map serial commands to callback functions
	server.register_handler("*IDN?", handle_idn)
	server.register_handler("POS?", handle_pos)
	server.register_handler("MOVE", handle_move)
	server.register_handler("HOME", handle_home)
	server.register_handler("STOP", handle_stop)

	# Start listner tasks
	await server.start()

