LOAD_FREEDOM = True    # syncs data to device on freedomrobotics.ai; requires credentials.json with freedom device credentials
LOAD_WATCHDOG = True   # initiates a watchdog so the uc resets if any blocking call hangs for more than 30 seconds
LOAD_DISPLAY = True    # 128x32 OLED display: https://www.adafruit.com/product/4440
LOAD_BME680 = True     # pressure, humidity, temperature, voc: https://www.adafruit.com/product/3660
LOAD_SGP30 = True      # voc (better than bme680): https://www.adafruit.com/product/3709
LOAD_SCD30 = True      # co2, humidity, temp: https://www.seeedstudio.com/Grove-CO2-Temperature-Humidity-Sensor-SCD30-p-2911.html
LOAD_MCGASV2 = True    # multi-channel gas sensor: https://www.seeedstudio.com/Grove-Multichannel-Gas-Sensor-v2-p-4569.html
LOAD_SEN0321 = True    # ozone sensor: https://www.dfrobot.com/product-2005.html
LOAD_BNO08X = True     # imu: https://www.adafruit.com/product/4754
LOAD_PMSA003I = True   # air quality particulate matter sensor: https://www.adafruit.com/product/4632

