# AgriSense Sentinel (Noma Vault IoT)

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-10B981?style=for-the-badge&logo=github)](https://hafeezmt.github.io/agrisence-iOT/)
[![MicroPython](https://img.shields.io/badge/Firmware-MicroPython%20v1.22-3884FF?style=for-the-badge&logo=python)](https://micropython.org/)
[![Hardware](https://img.shields.io/badge/Hardware-ESP32%20Dual--Core-E7352F?style=for-the-badge&logo=espressif)](https://www.espressif.com/)
[![Location](https://img.shields.io/badge/Engineered%20In-Gombe%20State%2C%20Nigeria-F59E0B?style=for-the-badge)](#team)

> **"The night watch, automated & offline."**  
> An autonomous, solar-powered, offline-first IoT environmental defense system protecting poultry and livestock pens in Northern Nigeria against nocturnal heat stress and toxic ammonia build-up.

---

## ⚡ The Problem: Nocturnal Pen Asphyxiation

In commercial poultry pens across Northern Nigeria (Gombe, Kano, Bauchi, Plateau), conditions turn lethal fastest between **midnight and 5:00 AM**:
- Power outages stall electric exhaust fans.
- Damp litter volatilizes into toxic ammonia gas ($NH_3$).
- Farmers sleeping in the compound only discover 20%–40% flock mortality at morning feed (₦150k–₦500k loss per incident).
- Foreign IoT monitors fail because they assume continuous 220V grid power and stable Wi-Fi.

---

## 🛡️ The Solution: AgriSense Sentinel

The AgriSense Sentinel is engineered around Sahel realities:
1. **Zero Grid Reliance**: 10W monocrystalline solar panel + MPPT controller with 72-hour 6000mAh battery reserve.
2. **Zero Cloud Dependency**: MicroPython edge firmware evaluates safety limits every 1,000ms.
3. **Instant On-Site Alarm**: 110dB Piezo Strobe Siren sounds immediately on-site to wake security and farm handlers.
4. **Direct 2G GSM Cellular SMS**: Sends critical text alerts over MTN, Airtel, or Glo to any basic mobile phone.
5. **Automated Fan Relay**: Energizes AC exhaust ventilation fans automatically before staff arrive.
6. **Local Black-Box Logging**: Records minute-by-minute CSV telemetry onto an industrial MicroSD card.

---

## 🗂️ Repository Architecture

```
agrisence-iOT/
├── assets/                    # Authentic local Nigerian farm and team photography
│   ├── hero_poultry.jpg       # Commercial poultry pen in operation
│   ├── danjuma_poultry.jpg    # Broiler flock in Gombe
│   ├── solar_farm.jpg         # Solar-powered roof installation
│   ├── nigerian_farmer.jpg    # Farmer inspecting pen
│   ├── hardware_lab.jpg       # Calibration bench
│   ├── abduljabbar.jpg        # Abduljabbar Bello Shariff (CEO)
│   └── jungudo.jpg            # Jungudo Muhammad Tukur (Operations)
├── docs/                      # Technical engineering documentation
│   ├── WIRING.md              # Complete pinout & electrical wiring guide
│   ├── BILL_OF_MATERIALS.md   # Component sourcing costs in Naira (₦)
│   ├── FIRMWARE_GUIDE.md      # Flashing MicroPython & deployment commands
│   └── PEN_MANAGEMENT_GUIDE.md# Veterinary ammonia & heat index parameters
├── firmware/                  # MicroPython ESP32 firmware source code
│   ├── boot.py                # Boot sequence & memory management
│   ├── main.py                # Core telemetry & threshold evaluation loop
│   ├── config.json            # Device parameters & phone alert list
│   ├── pins.py                # Hardware GPIO mapping
│   ├── watchdog.py            # Hardware watchdog timer manager
│   ├── drivers/               # Peripheral drivers
│   │   ├── sht31.py           # Sensirion SHT31 I2C driver with CRC8
│   │   ├── mq_gas.py          # Analog ammonia gas sensor ADC driver
│   │   ├── sim800l.py         # SIM800L GSM AT command SMS dispatcher
│   │   ├── sd_logger.py       # MicroSD SPI black-box CSV logger
│   │   ├── battery_monitor.py # Battery state-of-charge ADC monitor
│   │   └── actuators.py       # 110dB siren and relay controller
│   └── tests/
│       └── test_drivers.py    # Unit tests validating algorithms
├── index.html                 # High-tech interactive web dashboard & simulator
└── package.json               # Vite development server configuration
```

---

## 🚀 Quick Start (Local Web Simulator)

To preview the interactive telemetry simulator and financial calculator:

```bash
git clone https://github.com/hafeezmt/agrisence-iOT.git
cd agrisence-iOT
npm install
npm run dev
```

Open your browser to `http://localhost:5173`.

---

## 👥 Leadership & Engineering Team

- **Abduljabbar Bello Shariff** — *CEO & Co-Founder*  
  Background in cybersecurity and physics with over 5 years leading IT and IoT infrastructure.
- **Jungudo Muhammad Tukur** — *Operations Lead & Co-Founder*  
  Software developer studying Statistics at Gombe State University and Computer Science at UoPeople.

**Location**: Gombe State, Northern Nigeria  
**Contact**: `+234 901 548 7928` / `+234 802 874 2753`  
**Email**: `abduljabbarbello5@gmail.com` | `jungudomuhammadtukur@gmail.com`
