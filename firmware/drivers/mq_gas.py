"""
AgriSense MQ-137 / MQ-135 Ammonia (NH3) Gas Sensor Driver
MicroPython ADC driver with baseline calibration and PPM conversion
"""

import math
import time
from machine import ADC, Pin


class MQGasSensor:
    # Calibration coefficients for Ammonia (NH3) in poultry pens
    # Equation: ppm = a * (Rs / R0) ^ b
    # Derived from MQ-137 log-log sensitivity curve for NH3:
    CURVE_A = 102.2
    CURVE_B = -2.473

    # Load resistor on breakout board (typically 10k or 20k Ohms)
    RL_VALUE = 10.0  # kOhms

    def __init__(self, pin_num: int, r0_baseline: float = 18.5):
        self.adc = ADC(Pin(pin_num))
        self.adc.atten(ADC.ATTN_11DB)  # Full range ~3.3V (0 - 4095)
        self.adc.width(ADC.WIDTH_12BIT)
        self.r0 = r0_baseline  # Sensor resistance in clean air

    def read_raw_adc(self, samples: int = 10) -> float:
        """Collect multiple ADC samples and calculate trimmed average."""
        readings = []
        for _ in range(samples):
            readings.append(self.adc.read())
            time.sleep_ms(5)
        readings.sort()
        # Drop highest and lowest for noise rejection
        trimmed = readings[2:-2] if samples >= 6 else readings
        return sum(trimmed) / len(trimmed)

    def calculate_rs(self, adc_val: float) -> float:
        """Calculate sensor resistance Rs from raw 12-bit ADC value."""
        if adc_val <= 0:
            return 999.0
        voltage = (adc_val / 4095.0) * 3.3
        if voltage >= 3.25:
            return 0.1  # Saturated
        # Rs = (Vc - Vrl) / Vrl * RL
        rs = ((3.3 - voltage) / voltage) * self.RL_VALUE
        return max(rs, 0.05)

    def read_ammonia_ppm(self) -> float:
        """
        Calculate current Ammonia (NH3) concentration in parts-per-million (PPM).
        Returns PPM float or 0.0 if baseline is invalid.
        """
        try:
            raw_adc = self.read_raw_adc()
            rs = self.calculate_rs(raw_adc)
            ratio = rs / self.r0

            # Power law: ppm = a * ratio^b
            ppm = self.CURVE_A * math.pow(ratio, self.CURVE_B)
            return round(max(ppm, 0.0), 1)
        except Exception as e:
            print("[MQGas] Measurement error:", e)
            return 0.0

    def calibrate_clean_air(self, samples: int = 40) -> float:
        """Run clean air baseline calibration to calculate sensor R0."""
        print("[MQGas] Calibrating clean-air baseline (takes 4 seconds)...")
        rs_sum = 0.0
        for _ in range(samples):
            raw = self.adc.read()
            rs_sum += self.calculate_rs(raw)
            time.sleep_ms(100)
        rs_avg = rs_sum / samples
        # Clean air Rs/R0 ratio for MQ-137 is approximately 3.6
        self.r0 = rs_avg / 3.6
        print(f"[MQGas] Calibration complete. New R0 = {self.r0:.2f} kOhm")
        return self.r0
