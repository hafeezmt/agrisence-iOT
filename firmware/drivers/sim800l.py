"""
SIMCom SIM800L Industrial GSM Engine Driver
Handles AT command handshake, network registration, and SMS transmission.
Tested on MTN Nigeria, Airtel Nigeria, and Globacom networks.
"""

import time
from machine import UART, Pin


class SIM800L:
    def __init__(self, uart_id: int, tx_pin: int, rx_pin: int, rst_pin: int = None, baudrate: int = 9600):
        self.uart = UART(uart_id, baudrate=baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin), timeout=1000)
        self.rst = Pin(rst_pin, Pin.OUT) if rst_pin else None
        self.is_initialized = False

    def hardware_reset(self):
        """Pull RST low for 100ms to reboot the GSM baseband."""
        if self.rst:
            print("[SIM800L] Triggering hardware reset...")
            self.rst.value(0)
            time.sleep_ms(100)
            self.rst.value(1)
            time.sleep(3)

    def send_cmd(self, cmd: str, expected_reply: str = "OK", timeout_ms: int = 3000) -> bool:
        """Send an AT command and check for expected response substring."""
        # Flush any incoming noise
        while self.uart.any():
            self.uart.read()

        full_cmd = (cmd + "\r\n").encode()
        self.uart.write(full_cmd)

        start = time.ticks_ms()
        buf = b""
        while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
            if self.uart.any():
                buf += self.uart.read()
                if expected_reply.encode() in buf:
                    return True
                if b"ERROR" in buf:
                    return False
            time.sleep_ms(20)
        return False

    def init_module(self) -> bool:
        """Initialize the modem and verify SIM readiness and network registration."""
        print("[SIM800L] Initializing modem...")
        # Send autobaud sync
        for _ in range(3):
            if self.send_cmd("AT", "OK", 1000):
                break
            time.sleep_ms(500)

        # Disable command echo to reduce UART noise
        self.send_cmd("ATE0", "OK")

        # Check SIM card pin status
        if not self.send_cmd("AT+CPIN?", "READY", 3000):
            print("[SIM800L] ERROR: SIM card not inserted or locked!")
            return False

        # Set SMS to plain Text Mode (ASCII)
        if not self.send_cmd("AT+CMGF=1", "OK", 2000):
            print("[SIM800L] ERROR: Failed to set SMS text mode")
            return False

        # Verify network registration (MTN/Airtel/Glo)
        # +CREG: 0,1 (Home) or 0,5 (Roaming)
        reg_ok = False
        for _ in range(10):
            if self.send_cmd("AT+CREG?", "+CREG: 0,1", 1000) or self.send_cmd("AT+CREG?", "+CREG: 0,5", 1000):
                reg_ok = True
                break
            time.sleep(1)

        if not reg_ok:
            print("[SIM800L] Warning: Network registration pending or low coverage")
        else:
            print("[SIM800L] Registered to cellular network.")

        self.is_initialized = True
        return True

    def get_signal_rssi(self) -> int:
        """Query signal quality (0-31 CSQ value, or 99 if unknown)."""
        self.uart.write(b"AT+CSQ\r\n")
        time.sleep_ms(200)
        if self.uart.any():
            reply = self.uart.read().decode('utf-8', 'ignore')
            if "+CSQ:" in reply:
                try:
                    csq = int(reply.split("+CSQ:")[1].split(",")[0].strip())
                    return csq
                except:
                    pass
        return 0

    def send_sms(self, phone_number: str, message: str) -> bool:
        """Send an urgent SMS dispatch to a Nigerian phone number."""
        print(f"[SIM800L] Dispatching SMS to {phone_number}...")
        
        # Ensure text mode
        self.send_cmd("AT+CMGF=1", "OK", 1000)

        cmd = f'AT+CMGS="{phone_number}"\r\n'
        self.uart.write(cmd.encode())

        # Wait for prompt '>'
        start = time.ticks_ms()
        got_prompt = False
        while time.ticks_diff(time.ticks_ms(), start) < 3000:
            if self.uart.any() and b">" in self.uart.read():
                got_prompt = True
                break
            time.sleep_ms(20)

        if not got_prompt:
            print("[SIM800L] SMS error: No '>' prompt received")
            self.uart.write(b"\x1B")  # ESC to cancel
            return False

        # Write message payload followed by ASCII 26 (Ctrl+Z)
        payload = message.encode() + b"\x1A"
        self.uart.write(payload)

        # Wait for delivery acknowledgment (+CMGS: <mr> and OK)
        start = time.ticks_ms()
        delivered = False
        while time.ticks_diff(time.ticks_ms(), start) < 15000:
            if self.uart.any():
                res = self.uart.read()
                if b"+CMGS:" in res or b"OK" in res:
                    delivered = True
                    break
                if b"ERROR" in res:
                    break
            time.sleep_ms(100)

        if delivered:
            print(f"[SIM800L] SMS successfully dispatched to {phone_number}")
            return True
        else:
            print(f"[SIM800L] SMS delivery failed to {phone_number}")
            return False
