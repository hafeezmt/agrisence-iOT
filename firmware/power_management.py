# ========================================================
# AGRISENSE IOT - SOLAR MPPT POWER & BATTERY TELEMETRY
# Target: ESP32 ADC & TP4056 / MPPT Controller
# Author: AgriSense Engineering (Gombe State, Nigeria)
# ========================================================

class PowerManager:
    def __init__(self, adc_pin=34, divider_ratio=2.0):
        self.adc_pin = adc_pin
        self.divider_ratio = divider_ratio
        self.nominal_voltage = 3.7 # Li-Ion Cell
        self.max_voltage = 4.2
        self.cutoff_voltage = 3.3

    def get_battery_level(self, raw_voltage=3.95):
        """Calculate state of charge % and operating mode"""
        percentage = max(0.0, min(100.0, ((raw_voltage - self.cutoff_voltage) / (self.max_voltage - self.cutoff_voltage)) * 100))
        
        if percentage > 80:
            mode = "OPTIMAL_SOLAR_BOOST"
        elif percentage > 30:
            mode = "BALANCED_TELEMETRY"
        else:
            mode = "POWER_SAVER_CRITICAL"

        return {
            "battery_voltage_v": round(raw_voltage, 2),
            "state_of_charge_pct": round(percentage, 1),
            "operating_mode": mode,
            "is_charging": raw_voltage > 3.85
        }

if __name__ == "__main__":
    pm = PowerManager()
    status = pm.get_battery_level(4.10)
    print(f"[POWER] Solar MPPT Voltage: {status['battery_voltage_v']}V | Charge: {status['state_of_charge_pct']}% | Mode: {status['operating_mode']}")
