"""
AgriSense Sentinel Hardware Watchdog & System Recovery
Ensures unattended 24/7 reliability in remote rural pens.
"""

import machine
import time


class SystemWatchdog:
    # Hardware watchdog timeout in milliseconds (ESP32 max typically ~8000ms - 10000ms)
    WDT_TIMEOUT_MS = 8000

    def __init__(self):
        self.wdt = None
        self._check_reset_reason()

    def _check_reset_reason(self):
        """Inspect and log ESP32 hardware reset reason."""
        reason = machine.reset_cause()
        reasons_map = {
            machine.PWRON_RESET: "Power-on Reset (Normal)",
            machine.HARD_RESET: "Hard Pin Reset",
            machine.WDT_RESET: "Hardware Watchdog Timer Reset (Crash Recovery)",
            machine.DEEPSLEEP_RESET: "Woke from Deep Sleep",
            machine.SOFT_RESET: "Software Reset"
        }
        name = reasons_map.get(reason, f"Unknown code: {reason}")
        print(f"[Watchdog] Last reset cause: {name}")

    def enable(self):
        """Arm the hardware watchdog timer."""
        try:
            self.wdt = machine.WDT(timeout=self.WDT_TIMEOUT_MS)
            print(f"[Watchdog] Hardware WDT armed ({self.WDT_TIMEOUT_MS}ms window)")
        except Exception as e:
            print("[Watchdog] Warning: Could not initialize hardware WDT:", e)

    def feed(self):
        """Pet/feed the watchdog to prevent hardware reboot."""
        if self.wdt:
            self.wdt.feed()
