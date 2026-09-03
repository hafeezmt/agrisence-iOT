# AgriSense Sentinel — Hardware Wiring Guide

This document details the exact electrical connections between the **ESP32-WROOM-32** controller, sensing probes, GSM modem, and power management modules.

---

## 1. Complete Pin Interconnect Table

| Peripheral | Module Pin | ESP32 GPIO | Electrical Level | Notes |
|------------|------------|------------|------------------|-------|
| **SHT31 Sensor** | VCC | 3.3V | 3.3V DC | Digital I2C power |
| | GND | GND | 0V Ground | Common Ground |
| | SDA | GPIO 21 | 3.3V Logic | 4.7kΩ pull-up to 3.3V |
| | SCL | GPIO 22 | 3.3V Logic | 4.7kΩ pull-up to 3.3V |
| **MQ-137 / 135** | VCC | 5V | 5.0V DC | Requires 5V for internal heater coil |
| | GND | GND | 0V Ground | Common Ground |
| | AOUT | GPIO 34 | 0.0 - 3.3V | ADC1_CH6 (Analog gas voltage) |
| **SIM800L GSM** | VCC / VBAT | LiPo (+) | 3.8V - 4.2V | Needs 2A burst current capability |
| | GND | GND | 0V Ground | Common Ground |
| | TXD | GPIO 16 (RX2) | 2.8V - 3.3V | Direct connection to ESP32 RX2 |
| | RXD | GPIO 17 (TX2) | 2.8V Logic | Use 1kΩ / 2kΩ divider from ESP32 3.3V TX |
| | RST | GPIO 4 | 3.3V Logic | Optional hardware reset line |
| **MicroSD SPI** | VCC | 3.3V | 3.3V DC | SPI power rail |
| | GND | GND | 0V Ground | Common Ground |
| | MOSI | GPIO 23 | 3.3V Logic | Hardware VSPI MOSI |
| | MISO | GPIO 19 | 3.3V Logic | Hardware VSPI MISO |
| | SCK | GPIO 18 | 3.3V Logic | Hardware VSPI CLK |
| | CS | GPIO 5 | 3.3V Logic | Chip Select |
| **Piezo Siren** | IN (+) | GPIO 26 | 3.3V / 5V | Transistor / Relay coil trigger |
| **Fan Relay** | IN (+) | GPIO 27 | 3.3V / 5V | Optocoupled 10A 250VAC Relay |
| **Battery Sense** | Divider | GPIO 35 | 0.0 - 3.3V | Resistor divider (100kΩ / 27kΩ) from LiPo |

---

## 2. Power Supply Rail Architecture

```
                 +-------------------+
                 | 10W Solar PV Panel|
                 +---------+---------+
                           | (18V DC)
                           v
              +-------------------------+
              | CN3791 MPPT Solar Board |
              +------------+------------+
                           | (4.2V Charge)
                           v
             +---------------------------+
             | 6000mAh 1S2P 18650 Li-ion |
             +-------------+-------------+
                           |
          +----------------+----------------+
          | (3.7V - 4.2V)                   |
          v                                 v
   +--------------+                 +---------------+
   | SIM800L VBAT |                 | ME6211 3.3V   |
   | (2A bursts)  |                 | LDO Regulator |
   +--------------+                 +-------+-------+
                                            |
                                 +----------+----------+
                                 | (3.3V Stable)       |
                                 v                     v
                           +-----------+         +-----------+
                           | ESP32 MCU |         | SHT31, SD |
                           +-----------+         +-----------+
```

---

## 3. Important Field Assembly Notes

1. **Ammonia Sensor Heater Isolation**: The MQ-137 heating element draws ~150mA at 5V. Ensure its power comes from the 5V boost rail and not the ESP32 3.3V output.
2. **Corrosion Resistance**: Pen air contains high concentrations of moisture and airborne ammonia gas ($NH_3$). Apply silicone conformal coating to both sides of the soldered PCB, leaving only the SHT31 membrane and MQ sensor opening exposed.
3. **Antenna Orientation**: Position the high-gain GSM omni antenna externally or near an enclosure rubber grommet away from the ESP32 crystal oscillator.
