from LabControl.RS232Clients.AsyncRS232Client import AsyncRS232Client, SerialLogger


class PicoStage:

	def __init__(self, stage_id: str, port_name: str, log_path: str, stage_cfg: dict):
		self.stage_cfg: dict = stage_cfg

		stage_logger = SerialLogger(name=stage_id, log_file=log_file_path)
		client = AsyncRS232Client(port=port_name, baudrate=9600, logger_instance=custom_logger)

		is_connected: bool = await client.connect()


	def move(move_arg: str) -> None:
		self.client.send("MOV " + str(move_arg))

	def moveHandler() -> None:


class ZaberStage:

	def __init__(self, port_name: str, log_path: str):

