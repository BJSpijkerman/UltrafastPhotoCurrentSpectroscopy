

class GlazAPIException(Exception):
	def __init(self, code: int, message: str=""):
		self.code = code
		self.message = message
		full_msg = f"Glaz API Error [{code}]"
		if message:
			full_msg += f": {message}"
		super().__init__(full_msg)
