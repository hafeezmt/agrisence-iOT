"""
Sensirion SHT31 Digital Temperature & Humidity Sensor Driver
MicroPython Implementation with CRC8 Data Validation
"""

import time
from machine import I2C

SHT31_DEFAULT_ADDR = 0x44
CMD_MEASURE_HIGHREP = b'\x24\x00'
CMD_SOFT_RESET = b'\x30\xA2'
CMD_HEATER_ENABLE = b'\x30\x6D'
CMD_HEATER_DISABLE = b'\x30\x66'


class SHT31:
    def __init__(self, i2c: I2C, addr: int = SHT31_DEFAULT_ADDR):
        self.i2c = i2c
        self.addr = addr
        self._reset()

    def _crc8(self, data: bytes) -> int:
        """Calculate CRC-8 checksum for 2-byte sensor chunks (poly 0x31)."""
        crc = 0xFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ 0x31) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        return crc

    def _reset(self):
        """Soft-reset the SHT31 sensor."""
        try:
            self.i2c.writeto(self.addr, CMD_SOFT_RESET)
            time.sleep_ms(15)
        except Exception as e:
            print("[SHT31] Reset warning:", e)

    def read_temperature_humidity(self) -> tuple[float, float]:
        """
        Trigger single-shot measurement and return (temp_c, humidity_rh).
        Returns (None, None) if I2C bus error or CRC validation fails.
        """
        try:
            self.i2c.writeto(self.addr, CMD_MEASURE_HIGHREP)
            time.sleep_ms(20)  # Max duration for high repeatability is 15ms

            raw = self.i2c.readfrom(self.addr, 6)

            # Validate Temperature bytes [0, 1] against CRC [2]
            if self._crc8(raw[0:2]) != raw[2]:
                raise ValueError("SHT31 Temperature CRC verification failed")

            # Validate Humidity bytes [3, 4] against CRC [5]
            if self._crc8(raw[3:5]) != raw[5]:
                raise ValueError("SHT31 Humidity CRC verification failed")

            raw_temp = (raw[0] << 8) | raw[1]
            raw_hum = (raw[3] << 8) | raw[4]

            temp_c = -45.0 + (175.0 * raw_temp / 65535.0)
            hum_rh = 100.0 * raw_hum / 65535.0

            return round(temp_c, 2), round(hum_rh, 1)

        except Exception as err:
            print("[SHT31] Read Error:", err)
            return None, None
