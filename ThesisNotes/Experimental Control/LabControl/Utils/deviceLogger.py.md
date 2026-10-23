This class is meant to stream logs from device actions to the console and to a .log file. This is done to keep tabs on the devices functioning and so that issues can be traced back to a specific device and time. It does this by defining a pre-specified format around Python's logging.logger class and incorporated stream handlers for console and file logging with configurable levels.

# Key features
- __log file__: The logger has for each named instance a configurable log file path where the logs are written.
- __Logging levels__: The logger has configurable console and file logging levels.
- __Timestamp logging__: Each log in the .log file has the timestamp of the log attached.

# Documentation
```
DeviceLogger(name: str = "DeviceLogger", log_file: str = "logger_debug.log", console_level: int = logging.INFO, file_level: int = logging.DEBUG)
```

| Parameter     | Type | Default            | Description                                                      |
| ------------- | ---- | ------------------ | ---------------------------------------------------------------- |
| name          | str  | "DeviceLogger"     | Name of the logger instance.                                     |
| log_file      | str  | "logger_debug.log" | Path to .log file created by the logger instance                 |
| console_level | int  | logging.INFO       | All logs of this level and higher are reported to the console.   |
| file_level    | int  | logging.DEBUG      | All logs of this level and higher are reported to the .log file. |

#### Methods
__debug(msg: str, \*args, **kwargs) -> None__:
	Sends a log of level debug to the log handlers.
- __Returns__: None

__info(msg: str, \*args, **kwargs) -> None__:
	Sends a log of level info to the log handlers
- __Returns__: None

__error(msg: str, \*args, **kwargs) -> None__:
	Sends a log of level error to the log handlers
- __Returns__: None

# Usage example
```
from LabControl.Utils.DeviceLogger import DeviceLogger

logger = DeviceLogger(
					name = "testLogger",
					log_file = "logger_debug.log"
					)

logger.info("Testing info level")
logger.debug("Testing debug level")
logger.warning("Testing warning %d", 5)
logger.error("Testing error %s", "test")
```