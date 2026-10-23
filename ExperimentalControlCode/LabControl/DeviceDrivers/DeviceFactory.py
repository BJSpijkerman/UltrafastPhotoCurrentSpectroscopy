import logging
from types import SimpleNamespace
from typing import Dict, Any, Type, Union
from LabControl.devices.SR830Control import SR830
from LabControl.devices.StageControl import ZaberDelayStage
from LabControl.devices.AsyncSR830Control import AsyncSR830


class DeviceFactory:

	_DRIVER_MAP: Dict[str, Type] = {
			"sr830": SR830,
			"lockin": SR830,
			"async_sr830": AsyncSR830,
			"async_lockin": AsyncSR830,
			"zaber": ZaberDelayStage,
			"delay_stage": ZaberDelayStage
			}

	@classmethod
	def register_driver(cls, name: str, driver_cls: Type) -> None:
		cls._DRIVER_MAP[name.lower()] = driver_cls

	@classmethod
	def create_device(cls, device_type: str, **kwargs) -> Any:
		key = device_type.lower()
		if key not in cls._DRIVER_MAP:
			raise ValueError(
					f"Unknown device type '{device_type}'. Registered drivers: {list(cls._DRIVER_MAP.keys())}"
					)

		driver_cls = cls._DRIVER_MAP[key]
		return driver_cls(**kwargs)

	@classmethod
	def create_devices(cls, config: Dict[str, Dict[str, Any]]) -> SimpleNamespace:
		namespace_dict = {}

		for device_name, params in config.items():
			params_copy = params.copy()
			device_type = params_copy.pop("type", None)

			if not device_type:
				raise ValueError(
						f"Device configuration for '{device_name}' is missing required 'type' field."
						)

			instance = cls.create_device(device_type, **params_copy)
			namespace_dict[device_name] = instance

		return SimpleNamespace(**namespace_dict)
