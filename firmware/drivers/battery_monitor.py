"""
AgriSense Battery & Solar Power Management Driver
Measures DC rail voltage via ADC resistor divider and estimates State-of-Charge (SoC).
"""

from machine import ADC, Pin


class BatteryMonitor:
    # Voltage divider resistors: R1=100k, R2=27k
    # Divider ratio: (100 + 27) / 27 = 4.7037
    DIVIDER_RATIO = 4.7037

    # 1S Lithium-Ion / LiPo thresholds
    V_FULL = 4.18
    V_NOMINAL = 3.70
    V_LOW = 3.45
    V_CUTOFF = 3.20

    def __init__(self, adc_pin: int):
        self.adc = ADC(Pin(adc_pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)

    def read_voltage(self, samples: int = 10) -> float:
        """Read average ADC voltage and compute actual battery pack DC voltage."""
        raw_sum = 0
        for _ in range(samples):
            raw_sum += self.adc.read()
        raw_avg = raw_sum / samples

        # ESP32 pin voltage (0 - 3.3V)
        pin_voltage = (raw_avg / 4095.0) * 3.3
        # Battery voltage before divider
        batt_voltage = pin_voltage * self.DIVIDER_RATIO
        return round(batt_voltage, 2)

    def get_soc_percentage(self) -> int:
        """Estimate State-of-Charge percentage (0 - 100%)."""
        v = self.read_voltage()
        if v >= self.V_FULL:
            return 100
        elif v <= self.V_CUTOFF:
            return 0
        else:
            pct = ((v - self.V_CUTOFF) / (self.V_FULL - self.V_CUTOFF)) * 100.0
            return max(0, min(100, int(pct)))

    def is_low_power(self) -> bool:
        """Return True if battery voltage has dropped below the safe warning threshold."""
        return self.read_voltage() < self.V_LOW
