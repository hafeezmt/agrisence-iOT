# ========================================================
# AGRISENSE IOT - GSM SMS ALERT DISPATCHER (SIM800L 2G)
# Target: SIMCom SIM800L AT Commands / Cellular Retry Queue
# Author: AgriSense Engineering (Gombe State, Nigeria)
# ========================================================

class GSMAlertDispatcher:
    def __init__(self, primary_phone="+2348000000000"):
        self.primary_phone = primary_phone
        self.retry_limit = 3

    def format_alert_sms(self, pen_name, alert_type, nh3_ppm, temp_c):
        """Format high-priority alert text message for Nigerian farmers"""
        return (
            f"🚨 AGRISENSE EMERGENCY [{pen_name}]: "
            f"{alert_type} Spike detected! "
            f"Ammonia: {nh3_ppm} PPM | Temp: {temp_c}°C. "
            f"110dB Siren triggered on-site. Check ventilation immediately!"
        )

    def dispatch_sms(self, phone_number, message_text):
        """Simulate SIM800L AT Command SMS Dispatch Routine"""
        # AT+CMGF=1 (Text Mode)
        # AT+CMGS="+234..."
        return {
            "recipient": phone_number,
            "length_bytes": len(message_text),
            "command": f'AT+CMGS="{phone_number}"',
            "status": "SENT_SUCCESS_SMS_GATEWAY_2G",
            "retry_attempts": 0
        }

if __name__ == "__main__":
    dispatcher = GSMAlertDispatcher()
    msg = dispatcher.format_alert_sms("Dadinkowa Pen #4", "AMMONIA GAS", 33.2, 31.5)
    result = dispatcher.dispatch_sms("+2348012345678", msg)
    print(f"[GSM DISPATCH] Sent to {result['recipient']} | Command: {result['command']} | Status: {result['status']}")
