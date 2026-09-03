"""
AgriSense Sentinel - Main Edge Telemetry Daemon (main.py)
Continuous autonomous sensor monitoring, threshold alerting, and offline logging.
"""

import gc
import json
import time
from machine import I2C, SPI, Pin

import pins
from watchdog import SystemWatchdog
from drivers.sht31 import SHT31
from drivers.mq_gas import MQGasSensor
from drivers.sim800l import SIM800L
from drivers.sd_logger import SDLogger
from drivers.battery_monitor import BatteryMonitor
from drivers.actuators import ActuatorController


def load_configuration():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print("[Main] Config load fallback:", e)
        return {
            "thresholds": {"temperature_critical_c": 32.5, "ammonia_critical_ppm": 25.0},
            "alerting": {"alert_phone_numbers": ["+2349015487928"]}
        }


def main():
    print("[Main] Starting AgriSense Sentinel Edge Engine...")
    config = load_configuration()
    thresholds = config.get("thresholds", {})
    alert_cfg = config.get("alerting", {})

    # 1. Initialize Hardware Watchdog
    wdt = SystemWatchdog()
    wdt.enable()

    # 2. Initialize Actuators (Siren, Fan, LED)
    actuators = ActuatorController(pins.SIREN_RELAY_PIN, pins.FAN_RELAY_PIN, pins.STATUS_LED_PIN)
    actuators.led_blink(times=3)

    # 3. Initialize I2C Bus & SHT31
    try:
        i2c = I2C(0, scl=Pin(pins.I2C_SCL_PIN), sda=Pin(pins.I2C_SDA_PIN), freq=pins.I2C_FREQ_HZ)
        sht = SHT31(i2c)
    except Exception as e:
        print("[Main] I2C SHT31 init error:", e)
        sht = None

    # 4. Initialize MQ Ammonia Gas Sensor
    gas = MQGasSensor(pins.MQ_GAS_ADC_PIN)

    # 5. Initialize Battery Monitor
    batt = BatteryMonitor(pins.BATTERY_VOLTAGE_ADC_PIN)

    # 6. Initialize SD Card Logger
    try:
        spi = SPI(1, baudrate=10000000, polarity=0, phase=0,
                  sck=Pin(pins.SD_SCK_PIN), mosi=Pin(pins.SD_MOSI_PIN), miso=Pin(pins.SD_MISO_PIN))
        logger = SDLogger(spi, pins.SD_CS_PIN)
    except Exception as e:
        print("[Main] SD Logger init error:", e)
        logger = None

    # 7. Initialize SIM800L GSM Modem
    gsm = SIM800L(pins.GSM_UART_PORT, pins.GSM_TX_PIN, pins.GSM_RX_PIN, pins.GSM_RST_PIN, pins.GSM_BAUDRATE)
    gsm.init_module()

    print("[Main] All peripherals initialized. Entering telemetry loop.")

    last_sd_log = 0
    last_sms_sent = 0
    sms_cooldown = alert_cfg.get("sms_cooldown_seconds", 300)
    sd_log_interval = config.get("sampling", {}).get("sd_log_interval_seconds", 60)

    # Main Autonomous Loop
    while True:
        wdt.feed()  # Feed the hardware watchdog

        # --- Sensor Acquisition ---
        temp, hum = sht.read_temperature_humidity() if sht else (None, None)
        nh3 = gas.read_ammonia_ppm()
        v_batt = batt.read_voltage()

        actuators.led_blink(times=1, delay_ms=40)

        # Fallback values if sensor unplugged
        temp = temp if temp is not None else 28.0
        hum = hum if hum is not None else 65.0

        print(f"[Telemetry] Temp: {temp}°C | Hum: {hum}% | NH3: {nh3} ppm | Batt: {v_batt}V")

        # --- Threshold Evaluation ---
        is_temp_critical = temp >= thresholds.get("temperature_critical_c", 32.5)
        is_nh3_critical = nh3 >= thresholds.get("ammonia_critical_ppm", 25.0)

        if is_temp_critical or is_nh3_critical:
            reasons = []
            if is_nh3_critical:
                reasons.append(f"Ammonia spike: {nh3}ppm")
            if is_temp_critical:
                reasons.append(f"Severe heat: {temp}C")
            reason_str = ", ".join(reasons)

            print(f"[CRITICAL HAZARD] {reason_str}")

            # 1. Engage on-site siren & automated fan relay immediately
            actuators.siren_on()
            actuators.fan_on()

            # 2. Dispatch SMS alert if cooldown expired
            now = time.time()
            if (now - last_sms_sent) >= sms_cooldown:
                alert_msg = (
                    f"AGRISENSE ALERT [{config.get('device_id')}]: DANGER THRESHOLD EXCEEDED! "
                    f"{reason_str}. Siren sounding on-site. Check pen immediately!"
                )
                for number in alert_cfg.get("alert_phone_numbers", []):
                    gsm.send_sms(number, alert_msg)
                last_sms_sent = now

            # 3. Log to SD
            if logger:
                logger.log_critical_event(reason_str)
                logger.log_telemetry(temp, hum, nh3, v_batt, event="CRITICAL")
        else:
            # Nominal conditions
            actuators.siren_off()
            # (Fan can remain off or stay on cooldown)

        # Check siren auto-silence timeout (protects siren hardware after 30s)
        actuators.check_siren_timeout(alert_cfg.get("siren_duration_seconds", 30))

        # Periodic SD logging
        now = time.time()
        if logger and (now - last_sd_log) >= sd_log_interval:
            logger.log_telemetry(temp, hum, nh3, v_batt, event="NORMAL")
            last_sd_log = now

        # Memory hygiene
        gc.collect()

        time.sleep(config.get("sampling", {}).get("sensor_poll_interval_seconds", 2))


if __name__ == "__main__":
    main()
