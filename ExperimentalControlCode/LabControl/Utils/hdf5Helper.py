import h5py


class HDF5Helper:

	def __init__(self):
		self.file = None
		self.datasets = []
		self.groups = []


	def connect_to_file(self, file_path: str) -> None:
		try:
			self.file = h5py.File(file_path, "w")
		except Exception as e:
			print(f"Error: in opening file {file_path} with {e}")

		for group in sub_groups:
			group = self.file.create_subgroup(group)
			self.datasets.append(group)


	def set_metadata(self, param_dict: dict) -> None:
		if not self.file:
			print("No h5 file connected to writer")
			return

		for key in param_dict.keys:
			self.file.attrs[key] = param_dict["keys"]


	def add_group(group_name: str) -> None:
		self.groups.append(group_name)


	def create_measurement(self, group: str, title: str) -> None:
		if !(group in self.groups):
			print("Error: group was not registered. Register with HDF5Helper.add_group(\"group_name\")."
			return

		dataset = self.file[group].create_dataset(title)
		self.datasets.append(dataset)


	def stream_data(self, group: str, dataset: str, data) -> None:
		if not ((group in self.groups) and (dataset in self.datasets)):
			print("Error: group or dataset was not registered.")
			return

		self.file[group][dataset][i] = data


	def close_file(self) -> None:
		self.file.close()
