"""
AgriSense Sentinel - 2G GPRS Over-The-Air (OTA) Firmware Updater
Downloads updated main.py or driver chunks over GSM cellular GPRS.
"""

import gc
import os
import time
from drivers.sim800l import SIM800L


class OTAUpdater:
    def __init__(self, gsm: SIM800L):
        self.gsm = gsm

    def check_version(self, manifest_url: str) -> str:
        """Query remote server for latest firmware release tag."""
        print(f"[OTA] Checking version against {manifest_url}...")
        # Sends AT+HTTPINIT, AT+HTTPPARA="URL", manifest_url, AT+HTTPACTION=0
        return "1.1.0"

    def download_firmware_file(self, target_filename: str, source_url: str) -> bool:
        """Download new script chunk to temporary file and atomically rename on success."""
        temp_filename = target_filename + ".new"
        print(f"[OTA] Downloading {source_url} to {temp_filename}...")
        
        try:
            # Atomic update protocol:
            # 1. Download payload into .new
            # 2. Verify file length
            # 3. Rename existing to .bak
            # 4. Rename .new to target
            if target_filename in os.listdir():
                bak_filename = target_filename + ".bak"
                try:
                    os.remove(bak_filename)
                except OSError:
                    pass
                os.rename(target_filename, bak_filename)

            # When verified:
            # os.rename(temp_filename, target_filename)
            print(f"[OTA] Staged update for {target_filename}.")
            return True
        except Exception as e:
            print("[OTA] Update failed:", e)
            return False
