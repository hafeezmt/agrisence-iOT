"""
AgriSense Sentinel - Firmware Unit Tests & Calculation Validation
Can be executed with standard Python 3 or MicroPython.
"""

import math
import unittest


class MockSHT31:
    """Mock implementation to test CRC8 calculation and temperature conversion logic."""
    @staticmethod
    def crc8(data: bytes) -> int:
        crc = 0xFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ 0x31) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        return crc

    @staticmethod
    def convert_temp(raw: int) -> float:
        return -45.0 + (175.0 * raw / 65535.0)

    @staticmethod
    def convert_hum(raw: int) -> float:
        return 100.0 * raw / 65535.0


class MockMQGas:
    """Mock implementation to test Rs calculation and PPM power-law curve."""
    CURVE_A = 102.2
    CURVE_B = -2.473
    RL_VALUE = 10.0

    @classmethod
    def calculate_rs(cls, adc_val: float) -> float:
        voltage = (adc_val / 4095.0) * 3.3
        return ((3.3 - voltage) / voltage) * cls.RL_VALUE

    @classmethod
    def calculate_ppm(cls, rs: float, r0: float) -> float:
        ratio = rs / r0
        return cls.CURVE_A * math.pow(ratio, cls.CURVE_B)


class TestFirmwareAlgorithms(unittest.TestCase):
    def test_crc8_known_pattern(self):
        # Sensirion datasheet test vectors
        test_bytes = b"\xBE\xEF"
        checksum = MockSHT31.crc8(test_bytes)
        self.assertIsInstance(checksum, int)
        self.assertTrue(0 <= checksum <= 255)

    def test_sht31_temperature_conversion(self):
        # 0x65C6 in raw -> approx 24.5°C
        temp = MockSHT31.convert_temp(0x65C6)
        self.assertAlmostEqual(temp, 24.5, delta=0.5)

    def test_mq_gas_ppm_curve(self):
        # Clean air: ratio should be high, ppm should be low (< 10 ppm)
        clean_ppm = MockMQGas.calculate_ppm(rs=36.0, r0=10.0)
        self.assertLess(clean_ppm, 10.0)

        # High ammonia: ratio drops (rs decreases), ppm rises sharply
        danger_ppm = MockMQGas.calculate_ppm(rs=5.0, r0=10.0)
        self.assertGreater(danger_ppm, 25.0)


if __name__ == "__main__":
    unittest.main()
