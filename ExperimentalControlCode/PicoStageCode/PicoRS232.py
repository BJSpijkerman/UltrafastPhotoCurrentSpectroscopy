import uasyncio as asyncio
import sys
import uselect


# Implement async task queue
class Queue:

	def __init__(self):
		self.items = []


	# Append onto queue
	async def put(self, item) -> None:
		self.items.append(item)


	# Get items from queue
	async def get(self):
		while not self.items:
			await asyncio.sleep(0.01)
		return self.items.pop(0)


# Async RS232 protocol
class PicoRS232:

	def __init__(self):
		self.command_queue = Queue()
		self.handlers = {}
		self.is_running = False
		self.poll = uselect.poll()
		self.poll.register(sys.stdin, uselect.POLLIN)


	# Register command handler
	def register_handler(self, command: str, handler_coro) -> None:
		self.handlers[command] = handler_coro


	# Send response
	async def send(self, message: str) -> None:
		if not message.endswith("\r\n"):
			message += "\r\n"
		sys.stdout.write(message)


	# Async read loop
	async def _read_line_async(self) -> str:
		buffer = ""
		while self.is_running:
			# Check if stdin has bytes ready
			if self.poll.poll(0):
				char = sys.stdin.read(1)
				if char:
					if char == "\n" or char == "\r":
						if buffer.strip():
							return buffer.strip()
						buffer = ""
					else:
						buffer += char
			await asyncio.sleep(0.005)
		return ""


	# Background listener
	async def _stdin_listner(self) -> None:
		while self.is_running:
			command_line = await self._read_line_async()
			if command_line:
				# Push command onto queue
				await self.command_queue.put(command_line)


	# Excecutor for the command queue
	async def _command_processor(self) -> None:
		while self.is_running:
			raw_cmd = await self.command_queue.get()

			# Parse command and comma seperated arguments
			parts = raw_cmd.split(" ", 1)
			cmd_name = parts[0].upper()
			args = parts[1] if len(parts) > 1 else ""

			if cmd_name in self.handlers:
				try:
					# Call registered async handler
					result = await self.handlers[cmd_name](args)
					if result is not None:
						await self.send(str(result))
				except Exception as e:
					await self.send(f"ERR: Error in excecuting command '{cmd_name}'")
			else:
				await self.send(f"ERR: Unknown command name '{cmd_name}'")


	# Start serial listner and command processor tasks
	async def start(self) -> None:
		self.is_running = True
		asyncio.create_task(self._stdin_listner())
		asyncio.create_task(self._command_processor())
		await self.send("SYS: Pico RS232 procotol online")
