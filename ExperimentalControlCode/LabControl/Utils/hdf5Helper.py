import h5py


class HDF5Helper:

	def __init__(self):
		self.file


	def connect_to_file(self, file_path: str) -> None:
		self.file = h5py.File(file_path, "a")

	def set_metadata(self, metadata: str) -> None:

	def create_measurement(self, title: str) -> None:
		self.file.

	def stream_data(self, data) -> None

	def close_file(self) -> None:
		self.file.disconnect()
