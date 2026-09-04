# ========================================================
# AGRISENSE IOT - IHATCH COHORT 5 DEMO DAY HARDWARE RUNNER
# Target: ESP32 MicroPython (FreeRTOS)
# Author: AgriSense Engineering (Gombe State, Nigeria)
# ========================================================

import time
import math

class IHatchDemoRunner:
    def __init__(self, pen_id="Gombe-Pen-04"):
        self.pen_id = pen_id
        self.temp_baseline = 28.5  # Celsius
        self.hum_baseline = 62.0   # Relative Humidity %
        self.ammonia_baseline = 11.5 # PPM
        self.step_index = 0

    def read_telemetry_tick(self, simulate_spike=False):
        """Simulate real-time sensor reading pipeline for iHATCH judges"""
        self.step_index += 1
        noise = math.sin(self.step_index * 0.1) * 0.4
        
        if simulate_spike:
            # Midnight fan failure simulation
            current_temp = self.temp_baseline + (self.step_index * 0.8)
            current_hum = self.hum_baseline + (self.step_index * 1.1)
            current_nh3 = self.ammonia_baseline + (self.step_index * 2.5)
        else:
            current_temp = self.temp_baseline + noise
            current_hum = self.hum_baseline + noise
            current_nh3 = self.ammonia_baseline + (noise * 0.5)

        is_critical = current_nh3 >= 25.0 or current_temp >= 35.0

        return {
            "pen_id": self.pen_id,
            "tick": self.step_index,
            "temperature_c": round(current_temp, 2),
            "humidity_pct": round(current_hum, 2),
            "ammonia_ppm": round(current_nh3, 2),
            "siren_active": is_critical,
            "sms_triggered": is_critical,
            "status": "CRITICAL_ALERT" if is_critical else "NORMAL"
        }

if __name__ == "__main__":
    runner = IHatchDemoRunner()
    print("=== iHATCH Cohort 5 Regional Demo Mode Initialized ===")
    for i in range(5):
        data = runner.read_telemetry_tick(simulate_spike=(i >= 3))
        print(f"[TICK {data['tick']}] Pen: {data['pen_id']} | Temp: {data['temperature_c']}°C | NH3: {data['ammonia_ppm']} PPM | Siren: {data['siren_active']} | Status: {data['status']}")
        time.sleep(0.5)
