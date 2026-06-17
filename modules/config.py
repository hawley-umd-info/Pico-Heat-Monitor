"""
Author: dev.slife
Date Created: 2/19/26
Date Updated: 6/17/26
Description: Holds configuration values for Pico Heat Monitor.
"""

# ------------------------- HARDWARE CONFIG ------------------------- #

CLOCK_SPEED = 1
UPDATE_THRESHOLD = 60
TIMEOUT_THRESHOLD = 10
TIMEOUT_DELAY = 1
WIFI_DELAY = 30
TEMP_OFFSET = -2
HUM_OFFSET = 8


# ------------------------- DEVICE INFO ------------------------- #

PICO_NAME = "Pico<#1>"
PICO_ROOM = "Unassigned"


# ------------------------- PIN CONFIG ------------------------- #

BME_SDA_PIN = 4
BME_SCL_PIN = 5
OLED_SDA_PIN = 6
OLED_SCL_PIN = 7


# ------------------------- NETWORK CONFIG ------------------------- #

WIFI_SSID = ""
WIFI_PASSWORD = ""
CSV_FILE = "PICO_DATA.csv"
SERVER_URL = ""
FORM_MAP = {
    "Unique ID": "",
    "Assigned Room": "",
    "Time Recorded": "",
    "Date Recorded": "",
    "Hour Recorded": "",
    "Minute Recorded": "",
    "Year Recorded": "",
    "Month Recorded": "",
    "Day Recorded": "",
    "Raw Temperature": "",
    "Temperature": "",
    "Raw Humidity": "",
    "Humidity": ""
}

REPORTING_TIMES = [
   "10:30:00", # 10:30am 
   "13:30:00", # 1:30am
   "16:30:00"  # 4:30am
]