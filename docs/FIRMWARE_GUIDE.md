# AgriSense Sentinel — Firmware Flashing Guide

Complete guide for flashing MicroPython firmware and deploying AgriSense Sentinel code onto the ESP32 hardware.

---

## 1. Prerequisites

Install the official Espressif flashing tool and MicroPython remote helper:

```bash
pip install esptool mpremote
```

Download the official MicroPython ESP32 firmware binary (v1.20+ with generic SPIRAM or non-SPIRAM support):
- [https://micropython.org/download/esp32/](https://micropython.org/download/esp32/)

---

## 2. Erase Flash and Write MicroPython

Connect the ESP32 to your computer via USB (e.g. `COM3` on Windows or `/dev/ttyUSB0` on Linux):

```bash
# 1. Erase existing flash memory
esptool.py --chip esp32 --port COM3 erase_flash

# 2. Flash MicroPython firmware at offset 0x1000
esptool.py --chip esp32 --port COM3 --baud 460800 write_flash -z 0x1000 esp32-20240105-v1.22.1.bin
```

---

## 3. Uploading AgriSense Firmware Files

Clone or navigate to the repository directory:

```bash
cd agrisence-iOT/firmware
```

Use `mpremote` to copy the driver files and core runtime to the ESP32 filesystem:

```bash
# Create drivers directory on the board
mpremote connect COM3 fs mkdir :drivers

# Upload configuration and drivers
mpremote connect COM3 fs cp config.json :config.json
mpremote connect COM3 fs cp pins.py :pins.py
mpremote connect COM3 fs cp watchdog.py :watchdog.py
mpremote connect COM3 fs cp drivers/sht31.py :drivers/sht31.py
mpremote connect COM3 fs cp drivers/mq_gas.py :drivers/mq_gas.py
mpremote connect COM3 fs cp drivers/sim800l.py :drivers/sim800l.py
mpremote connect COM3 fs cp drivers/sd_logger.py :drivers/sd_logger.py
mpremote connect COM3 fs cp drivers/battery_monitor.py :drivers/battery_monitor.py
mpremote connect COM3 fs cp drivers/actuators.py :drivers/actuators.py

# Upload boot and main scripts
mpremote connect COM3 fs cp boot.py :boot.py
mpremote connect COM3 fs cp main.py :main.py
```

---

## 4. Live REPL Verification

Open the interactive serial monitor:

```bash
mpremote connect COM3 repl
```

To reset the board and watch the boot sequence:
- Press `Ctrl + D` on your keyboard for a soft reset.
- You should observe:
  ```text
  [Boot] CPU Clock Speed: 240 MHz
  [SIM800L] Initializing modem...
  [SIM800L] Registered to cellular network.
  [SDLogger] MicroSD card mounted at /sd
  [Main] All peripherals initialized. Entering telemetry loop.
  [Telemetry] Temp: 29.4°C | Hum: 68.0% | NH3: 14.2 ppm | Batt: 3.95V
  ```
