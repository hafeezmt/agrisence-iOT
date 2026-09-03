"""
AgriSense Sentinel - MicroPython Boot Sequence (boot.py)
Executed immediately on MCU power-on before main application logic.
"""

import gc
import esp
import machine

# Disable low-level OS debug print spam
esp.osdebug(None)

# Configure garbage collector threshold for predictable memory allocation
gc.enable()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

print("==================================================")
print("     AgriSense IoT - Sentinel Edge Node Boot      ")
print("           Noma Vault · Gombe State               ")
print("==================================================")
print(f"[Boot] CPU Clock Speed: {machine.freq() // 1000000} MHz")
print(f"[Boot] Initial Free RAM: {gc.mem_free()} bytes")
