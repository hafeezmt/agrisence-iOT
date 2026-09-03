"""
AgriSense Sentinel Actuator & Alarm Controller
Manages 110dB Piezo Siren, Exhaust Fan / Mister relay, and status LED.
"""

import time
from machine import Pin


class ActuatorController:
    def __init__(self, siren_pin: int, fan_pin: int, status_led_pin: int):
        self.siren = Pin(siren_pin, Pin.OUT)
        self.fan = Pin(fan_pin, Pin.OUT)
        self.led = Pin(status_led_pin, Pin.OUT)

        # Ensure all off at boot
        self.siren_off()
        self.fan_off()
        self.led_off()

        self.siren_triggered_time = 0
        self.is_siren_active = False
        self.is_fan_active = False

    def siren_on(self):
        """Engage the 110dB on-site strobe siren."""
        self.siren.value(1)
        self.is_siren_active = True
        self.siren_triggered_time = time.time()
        print("[Actuator] SIREN ALARM ENGAGED (110dB ON)")

    def siren_off(self):
        """Silence the siren."""
        self.siren.value(0)
        self.is_siren_active = False

    def fan_on(self):
        """Energize the ventilation fan relay."""
        self.fan.value(1)
        self.is_fan_active = True
        print("[Actuator] EXHAUST FAN / MISTER RELAY ACTIVATED")

    def fan_off(self):
        """De-energize the fan relay."""
        self.fan.value(0)
        self.is_fan_active = False

    def led_on(self):
        self.led.value(1)

    def led_off(self):
        self.led.value(0)

    def led_blink(self, times: int = 1, delay_ms: int = 80):
        for _ in range(times):
            self.led.value(1)
            time.sleep_ms(delay_ms)
            self.led.value(0)
            time.sleep_ms(delay_ms)

    def check_siren_timeout(self, max_duration_seconds: int = 30):
        """Auto-silence siren after max duration to protect acoustic coil."""
        if self.is_siren_active:
            elapsed = time.time() - self.siren_triggered_time
            if elapsed >= max_duration_seconds:
                print(f"[Actuator] Siren auto-silenced after {max_duration_seconds}s timeout")
                self.siren_off()
