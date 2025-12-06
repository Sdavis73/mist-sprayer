# \# CMAP2551 Automatic Mist Sprayer

# 

# This project uses an ESP32 microcontroller and a DHT22 humidity sensor to automatically activate a misting pump when humidity drops below a threshold. It includes MicroPython firmware for the ESP32 and a host-side Python script for telemetry and logging.

# 

# ---

# 

# \## 🛠 Hardware List

# 

# \- ESP32-S3 development board (Freenove breakout)

# \- DHT22 humidity sensor

# \- 1-channel 5V relay module

# \- 12V DC misting pump

# \- Flyback diode (e.g., 1N4007)

# \- Breadboard and jumper wires

# \- USB cable (for ESP32 programming)

# \- Optional: 12V power supply for pump

# 

# ---

# 

# \## 🔌 Wiring Instructions

# 

# \### DHT22 Sensor

# 

# | DHT22 Pin | ESP32 Pin |

# |-----------|-----------|

# | `+`       | 3V3       |

# | `–`       | GND       |

# | `S`       | GPIO 4    |

# 

# > Add a 10kΩ pull-up resistor between `S` and `+` if using raw sensor.

# 

# \### Relay Module

# 

# | Relay Pin | ESP32 Pin |

# |-----------|-----------|

# | `IN`      | GPIO 16   |

# | `VCC`     | 5V        |

# | `GND`     | GND       |

# 

# \### Misting Pump

# 

# \- COM → 12V +

# \- NO → Pump +

# \- Pump – → 12V –

# 

# > Add flyback diode across pump terminals (stripe to +, non-stripe to –)

# 

# ---

# 

# \## ⚙️ Setup Instructions

# 

# \### 1. Flash ESP32 with MicroPython

# \- Download latest MicroPython firmware from \[micropython.org](https://micropython.org/download/esp32/)

# \- Use \[Thonny](https://thonny.org/) or `esptool.py` to flash:

# &nbsp; ```bash

# &nbsp; esptool.py --port COMx erase\_flash

# &nbsp; esptool.py --port COMx write\_flash -z 0x1000 firmware.bin

# 

# Upload  to ESP32

# • 	Open Thonny

# • 	Connect to ESP32 via USB

# • 	Paste and save  to device

# 3\. Run host script

# • 	Install Python 3.x

# • 	Install :

# pip install pyserial

# python host/serial\_controller.py

# 🎬 Demo Instructions

# 1\. 	Power ESP32 via USB

# 2\. 	Run host script to monitor humidity

# 3\. 	When humidity < threshold (e.g., 45%), relay activates misting pump

# 4\. 	Pump runs for 3–6 seconds

# 5\. 	Humidity rises, pump stops

# 6\. 	Log file () records timestamp and humidity

# File Structure

# CMAP2551 Automatic Mist Sprayer/

# ├── firmware/

# │   └── main.py

# ├── host/

# │   └── serial\_controller.py

# ├── docs/

# │   └── circuit-diagram.png

# ├── logs/

# │   └── mist\_log.csv

# ├── README.md

# └── .gitignore

# &nbsp;.gitignore

# \_\_pycache\_\_/

# logs/\*.csv

# Example Run

# \[2025-12-06 12:15:03] Humidity: 42.3% → MIST ON

# \[2025-12-06 12:15:09] Humidity: 46.1% → MIST OFF



