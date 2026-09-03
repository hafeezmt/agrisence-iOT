"""
AgriSense Sentinel MicroSD Black-Box Event Logger
Records environmental sensor history and critical threshold events to local SPI SD card.
"""

import os
import time
from machine import SPI, Pin


class SDLogger:
    def __init__(self, spi: SPI, cs_pin: int, mount_point: str = "/sd"):
        self.spi = spi
        self.cs = Pin(cs_pin, Pin.OUT)
        self.mount_point = mount_point
        self.is_mounted = False
        self._mount_sd()

    def _mount_sd(self):
        """Mount the SD card filesystem."""
        try:
            # Note: requires MicroPython sdcard.py driver in /lib/
            import sdcard
            self.sd = sdcard.SDCard(self.spi, self.cs)
            self.vfs = os.VfsFat(self.sd)
            os.mount(self.vfs, self.mount_point)
            self.is_mounted = True
            print(f"[SDLogger] MicroSD card mounted at {self.mount_point}")
            self._init_csv_headers()
        except Exception as e:
            print("[SDLogger] SD Card mount warning:", e)
            self.is_mounted = False

    def _init_csv_headers(self):
        """Ensure telemetry.csv has proper column headers."""
        path = f"{self.mount_point}/telemetry.csv"
        try:
            os.stat(path)
        except OSError:
            # File does not exist, write header
            try:
                with open(path, "w") as f:
                    f.write("timestamp_epoch,temp_c,humidity_rh,ammonia_ppm,battery_v,event_flag\n")
            except Exception as e:
                print("[SDLogger] Header creation error:", e)

    def log_telemetry(self, temp: float, hum: float, nh3: float, batt: float, event: str = "NORMAL"):
        """Append one row of sensor readings to the local SD black-box."""
        if not self.is_mounted:
            return False

        path = f"{self.mount_point}/telemetry.csv"
        now = time.time()
        row = f"{now},{temp},{hum},{nh3},{batt},{event}\n"
        try:
            with open(path, "a") as f:
                f.write(row)
            return True
        except Exception as e:
            print("[SDLogger] Write failure:", e)
            return False

    def log_critical_event(self, description: str):
        """Append high-priority alarm event to events.log."""
        if not self.is_mounted:
            return False
        path = f"{self.mount_point}/events.log"
        now = time.time()
        entry = f"[{now}] CRITICAL: {description}\n"
        try:
            with open(path, "a") as f:
                f.write(entry)
            return True
        except Exception as e:
            print("[SDLogger] Event log failure:", e)
            return False
