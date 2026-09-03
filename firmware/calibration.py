"""
AgriSense Sentinel - Sensor Calibration & Baseline Zeroing Utility
Interactive terminal routine for field technicians calibrating the MQ-137 probe.
"""

import json
import time
from machine import Pin
import pins
from drivers.mq_gas import MQGasSensor


def run_sensor_calibration():
    print("==================================================")
    print("      AgriSense MQ-137 Calibration Wizard         ")
    print("==================================================")
    print("[1/3] Ensure the sensor probe is placed in fresh, clean air.")
    print("[2/3] Sensor heating coil must be preheated for >= 3 minutes.")
    
    confirm = input("Are you ready to calibrate? (y/n): ")
    if confirm.lower() != 'y':
        print("Calibration aborted.")
        return

    gas = MQGasSensor(pins.MQ_GAS_ADC_PIN)
    print("Sampling raw ADC values (40 iterations)...")
    new_r0 = gas.calibrate_clean_air(samples=40)

    # Persist calibrated R0 into config.json
    try:
        with open("config.json", "r") as f:
            cfg = json.load(f)
        
        cfg["calibration"] = {
            "mq_r0_baseline_kohm": round(new_r0, 2),
            "calibrated_timestamp_epoch": time.time()
        }

        with open("config.json", "w") as f:
            json.dump(cfg, f)

        print(f"[Success] New R0 ({new_r0:.2f} kOhm) saved to config.json.")
    except Exception as e:
        print("[Error] Failed to save calibration config:", e)


if __name__ == "__main__":
    run_sensor_calibration()
