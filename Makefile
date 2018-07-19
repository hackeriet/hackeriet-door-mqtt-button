upload:
		env AMPY_PORT=/dev/ttyUSB0 ampy put config.json config.json
		env AMPY_PORT=/dev/ttyUSB0 ampy put main.py main.py
