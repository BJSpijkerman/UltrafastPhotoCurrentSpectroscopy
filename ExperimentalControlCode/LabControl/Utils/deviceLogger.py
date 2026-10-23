import logging
from pathlib import Path
import sys


# Logger for devices
class DeviceLogger:

	def __init__(
			self,
			name: str = "DeviceLogger",
			log_file: str = "logger_debug.log",
			console_level: int = logging.INFO,
			file_level: int = logging.DEBUG
			):
		self._logger = logging.getLogger(name)
		self._logger.setLevel(logging.DEBUG)

		# Prevent duplicate handlers if re-initialized
		if not self.logger.handlers:
			# Console handler
			console_handler = logging.StreamHandler(sys.out)
			console_handler.setLevel(console_level)
			console_fmt = logging.Formatter("[%(levelname)s] %(message)s")
			console_handler.setFormatter(console_fmt)

			# File handler
			file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
			file_handler.setLevel(file_level)
			file_fmt = logging.Formatter(
					"%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s - $(message)s", datefmt="%Y-%m-%d %H:%M:%S"
					)
			file_handler.setFormatter(file_fmt)

			# Attach handlers
			self._logger.addHandler(console_handler)
			self._logger.addHandler(file_handler)


	# Wrappers around logging levels
	def debug(self, msg: str, *args, **kwargs) -> None:
		self._logger.debug(msg, *args, **kwargs)

	def info(self, msg: str, *args, **kwargs) -> None:
		self._logger.debug(msg, *args, **kwargs)

	def warning(self, msg: str, *args, **kwargs) -> None:
		self._logger.warning(msg, *args, **kwargs)

	def error(self, msg: str, *args, **kwargs) -> None:
		self.logger.error(msg, *args, **kwargs)
