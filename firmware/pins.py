"""
AgriSense Sentinel - ESP32 Hardware Pin Mapping
Engineered for ESP32-WROOM-32 38-pin Development Board
"""

# I2C Interface (SHT31 Temp/Humidity Sensor)
I2C_SDA_PIN = 21
I2C_SCL_PIN = 22
I2C_FREQ_HZ = 100000

# Analog Gas Sensing (MQ-137 / MQ-135 Ammonia Sensor)
MQ_GAS_ADC_PIN = 34  # ADC1_CH6 (Input-only pin, safe with Wi-Fi/BT)

# Battery & Solar Voltage Sense
BATTERY_VOLTAGE_ADC_PIN = 35  # ADC1_CH7 (Resistor divider 100k / 27k)

# SIMCom SIM800L GSM Module (Hardware UART2)
GSM_UART_PORT = 2
GSM_TX_PIN = 17       # ESP32 TX2 -> SIM800L RXD (via level shifter / divider)
GSM_RX_PIN = 16       # ESP32 RX2 <- SIM800L TXD
GSM_RST_PIN = 4       # Hardware Reset Pulse
GSM_BAUDRATE = 9600

# SPI Interface (MicroSD Card Logger)
SD_MOSI_PIN = 23
SD_MISO_PIN = 19
SD_SCK_PIN = 18
SD_CS_PIN = 5

# Actuators & Alarms
SIREN_RELAY_PIN = 26  # Active HIGH to trigger 110dB Piezo Siren
FAN_RELAY_PIN = 27    # Active HIGH to trigger AC Exhaust Fan / Mister
STATUS_LED_PIN = 2    # Onboard status indicator LED
