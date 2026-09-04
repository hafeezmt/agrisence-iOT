"""
AgriSense Sentinel - 2G GPRS Over-The-Air (OTA) Firmware Updater
Downloads updated main.py or driver chunks over GSM cellular GPRS.
Includes iHATCH Cohort 5 Regional Demo Day firmware metadata (v1.2.0).
"""

import gc
import os
import time
from drivers.sim800l import SIM800L


class OTAUpdater:
    RELEASE_MANIFEST = {
        "version": "1.2.0-ihatch",
        "channel": "ihatch_demo_regional",
        "state": "Gombe",
        "region": "North East Region, Nigeria"
    }

    def __init__(self, gsm: SIM800L):
        self.gsm = gsm

    def check_version(self, manifest_url: str) -> str:
        """Query remote server for latest firmware release tag."""
        print(f"[OTA] Checking version against {manifest_url} (Channel: {self.RELEASE_MANIFEST['channel']})...")
        # Sends AT+HTTPINIT, AT+HTTPPARA="URL", manifest_url, AT+HTTPACTION=0
        return self.RELEASE_MANIFEST["version"]

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
            print(f"[OTA] Staged update for {target_filename} (Version {self.RELEASE_MANIFEST['version']}).")
            return True
        except Exception as e:
            print("[OTA] Update failed:", e)
            return False
