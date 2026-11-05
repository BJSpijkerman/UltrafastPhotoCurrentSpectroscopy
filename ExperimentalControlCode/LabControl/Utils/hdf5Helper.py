import json
from typing import Any, Dict, Optional, Union
import h5py
import numpy as np


class HDF5Helper:

    def __init__(self, file_path: Optional[str] = None, mode: str = "a"):
        self.file: Optional[h5py.File] = None
        self.groups: set[str] = set()
        self.datasets: set[str] = set()

        if file_path:
            self.connect_to_file(file_path, mode=mode)

    def connect_to_file(self, file_path: str, mode: str = "a") -> None:
        """Connect to an HDF5 file. Mode 'a' opens/creates for read/write."""
        try:
            self.file = h5py.File(file_path, mode)
        except Exception as e:
            print(f"Error opening file {file_path}: {e}")
            self.file = None


    def set_metadata(self, param_dict: Dict[str, Any]) -> None:
        """Set key-value attributes at the root level safely."""
        if not self.file:
            print("Error: No HDF5 file connected.")
            return

        for key, value in param_dict.items():
            # Skip None values as HDF5 has no native None type
            if value is None:
                continue

            try:
                # 1. Standard supported types: numbers, strings, bools, numpy arrays
                if isinstance(value, (int, float, str, bool, np.number, np.ndarray)):
                    self.file.attrs[key] = value

                # 2. Convert lists/dicts to JSON strings so structured params are preserved
                elif isinstance(value, (dict, list, tuple)):
                    try:
                        self.file.attrs[key] = json.dumps(value)
                    except (TypeError, ValueError):
                        # Fallback to string representation if non-JSON serializable
                        self.file.attrs[key] = str(value)

                # 3. Fallback for any other custom Python objects
                else:
                    self.file.attrs[key] = str(value)

            except Exception as e:
                print(f"Warning: Could not set metadata key '{key}' (value: {value}): {e}")

    def add_group(self, group_name: str) -> None:
        """Create and register a group."""
        if not self.file:
            print("Error: No HDF5 file connected.")
            return

        if group_name not in self.file:
            self.file.create_group(group_name)

        self.groups.add(group_name)

    def create_dataset(
        self,
        group_name: str,
        dataset_name: str,
        dtype: Union[str, type] = "f8",  # 'f8' for float64, str / 'string' for text
        shape: tuple = (0,),
        maxshape: tuple = (None,),
    ) -> None:
        """Create a resizable dataset for floats, strings, or integers."""
        if not self.file:
            print("Error: No HDF5 file connected.")
            return

        if group_name not in self.groups:
            print(f"Error: Group '{group_name}' not registered.")
            return

        # Resolve string type to HDF5 variable-length UTF-8
        if dtype in (str, "string", "str"):
            resolved_dtype = h5py.string_dtype(encoding="utf-8")
        else:
            resolved_dtype = dtype

        dataset_path = f"{group_name}/{dataset_name}"
        if dataset_path not in self.file:
            self.file[group_name].create_dataset(
                dataset_name, shape=shape, maxshape=maxshape, dtype=resolved_dtype
            )

        self.datasets.add(dataset_path)

    def append_data(self, group_name: str, dataset_name: str, data: Any) -> None:
        """Append a single numerical value or string to a 1D dataset."""
        if not self.file:
            print("Error: No HDF5 file connected.")
            return

        dataset_path = f"{group_name}/{dataset_name}"
        if dataset_path not in self.datasets:
            print(f"Error: Dataset '{dataset_path}' not registered.")
            return

        dset = self.file[group_name][dataset_name]

        current_size = dset.shape[0]
        dset.resize((current_size + 1,))
        dset[current_size] = data

    def close_file(self) -> None:
        if self.file:
            self.file.close()
            self.file = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_file()
